# ARR October 2026 metadata draft

Status: anonymous, author-fillable metadata sheet. The author list, affiliations, ORCID records, conflicts, and service-contributor fields are intentionally omitted.

## Title

Before Selecting Evolving LLM Agents: Auditing Exposure, Score Validity, and Candidate Support

## Abstract

Test-time LLM agents retain natural-language state, score responses, and revise workflows while solving tasks. Before adding a selector or privacy mechanism, we need to know whether state carries sensitive content, whether scores track executable utility, and whether generation exposes useful alternatives. We introduce a persistence-aware executable audit and apply it to a released multi-agent runtime on PlanCraft. A complete three-arm replication detects no post-input canary exposure in 120 instances, with a one-sided 95\% upper bound of 2.5\%. Removing a score term assigning 85\% weight to output length changes the score scale across DeepSeek and Qwen, while a secondary synthesis of 42 paired runs changes exactness by only $+0.024$ (95\% interval $[-0.095,0.143]$). Across four frozen cohorts, selectors restricted to recorded candidates have at most 0--8.3 percentage points of headroom. Five independent Qwen trajectories raise executable-oracle accuracy from 0.60 to 0.80 at triple the token cost. A frozen same-task public-only control reverses our initial explanation on two selected DeepSeek failures: one invalid endpoint remains concentrated under both repair-conditioned and public-only prompts. These results define an audit order for evolving LLM-agent selection and its limits; they do not provide end-to-end privacy or a general prevalence estimate.

## Keywords

- language-model agents
- test-time adaptation
- agent evaluation
- privacy auditing
- reproducibility

## Suggested ARR routing

- Preferred venue at ARR submission: NAACL 2027
- Secondary commitment option: COLING 2027
- Paper type: long research paper
- Scope statement: empirical audit of test-time LLM-agent state, scoring, candidate support, and the limits of privacy-oriented selection claims

## Submission invariants

- Keep the author list and all identity-bearing metadata out of the anonymous source archive.
- Copy the title and abstract from `manuscript-arr/main.tex`; this file is a form aid, not an independent manuscript source.
- Do not describe the canary null result as a privacy guarantee, the Qwen result as a causal multi-agent advantage, or the selector calculation as end-to-end DP.
- Use the manuscript-only archive by default. The optional code supplement remains excluded until the license gate is cleared.

## Author-only fields to complete in OpenReview

- Author names, affiliations, emails, and ORCID-linked profiles
- Conflicts of interest and reciprocal-review eligibility
- Service-contributor registration
- ARR/NAACL preferred venue selection
- Responsible NLP checklist and generative-AI assistance disclosure
