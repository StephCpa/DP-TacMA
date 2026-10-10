"""Parser variants for the candidate-support audit (protocol 234).

P1 is a format-robust normalizer applied before the unchanged P0 parser.
P2 is an independent parser written without access to P0's code. Neither
infers missing content, rewrites actions, interprets prose, consults a
reference, or calls a model.

Answer schema assumed by P2: a PlanCraft answer is either IMPOSSIBLE or an
ordered list of item identifiers to craft, e.g. ["dark_oak_planks", "pink_bed"].
Confirm this against the benchmark answer format before freezing protocol 234.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re

IMPOSSIBLE = "IMPOSSIBLE"
_FENCE = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n?(.*?)```", re.S)
_IDENT = re.compile(r"^[a-z0-9_]+$")
_PUNCT = str.maketrans({
    "“": '"', "”": '"', "„": '"', "‘": "'", "’": "'",
    "［": "[", "］": "]", "，": ",", "、": ",", "：": ":",
    " ": " ", " ": " ", "​": "",
})


@dataclass(frozen=True)
class ParseResult:
    plan: tuple[str, ...] | str | None  # tuple of item ids, IMPOSSIBLE, or None
    reason: str  # "ok" or the rejection reason

    @property
    def accepted(self) -> bool:
        return self.plan is not None


def _strip_fences(text: str) -> str:
    blocks = _FENCE.findall(text)
    return "\n".join(blocks) if blocks else text


def p1_normalize(text: str) -> str:
    """Remove formatting that cannot change meaning; P0 parses the result."""

    out = _strip_fences(text).translate(_PUNCT).replace("\r\n", "\n").strip()
    try:
        value = json.loads(out)
    except (json.JSONDecodeError, ValueError):
        return out
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        value = [v.strip().lower() for v in value]
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _normalize_item(item: str) -> str:
    item = item.strip().lower()
    return item[len("minecraft:"):] if item.startswith("minecraft:") else item


def _string_arrays(text: str) -> list[list[str]]:
    decoder = json.JSONDecoder()
    arrays = []
    for match in re.finditer(r"\[", text):
        try:
            value, _ = decoder.raw_decode(text[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, list) and value and all(isinstance(v, str) for v in value):
            arrays.append(value)
    return arrays


def p2_parse(text: str | None) -> ParseResult:
    """Independent canonical parser: IMPOSSIBLE or exactly one distinct item list."""

    if text is None or not text.strip():
        return ParseResult(None, "empty")
    body = _strip_fences(text).translate(_PUNCT).strip()
    if re.fullmatch(r'["\']?\s*impossible\s*["\']?\s*\.?', body, re.I):
        return ParseResult(IMPOSSIBLE, "ok")
    arrays = _string_arrays(body)
    if not arrays:
        return ParseResult(None, "no_string_array")
    plans: set[tuple[str, ...] | str] = set()
    bad_items = False
    for array in arrays:
        items = tuple(_normalize_item(v) for v in array)
        if items == ("impossible",):
            plans.add(IMPOSSIBLE)
        elif all(_IDENT.match(i) for i in items):
            plans.add(items)
        else:
            bad_items = True
    if len(plans) > 1:
        return ParseResult(None, "ambiguous_multiple_plans")
    if not plans:
        return ParseResult(None, "non_identifier_item" if bad_items else "no_string_array")
    return ParseResult(plans.pop(), "ok")
