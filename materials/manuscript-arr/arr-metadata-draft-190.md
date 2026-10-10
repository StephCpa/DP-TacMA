# ARR October 2026 metadata draft

Status: anonymous, author-fillable metadata sheet. The author list, affiliations, ORCID records, conflicts, and service-contributor fields are intentionally omitted.

## Title

Before Candidate Selection in Test-Time LLM Agents: A Scope-Limited Audit of Exposure, Score Interventions, and Realized Candidate Support

## Abstract

Test-time LLM agents retain natural-language state, score intermediate responses, and revise their outputs while solving tasks. Before adding a candidate selector or a privacy mechanism, one should check three preconditions: whether protected content enters persistent state, whether changing the score has downstream consequences, and whether the generator exposes executable alternatives worth selecting. We apply this audit order to one configuration of a released multi-agent runtime, TacoMAS with a fixed three-agent topology and structural edits disabled, on the PlanCraft benchmark. In a three-arm canary study with 120 instances per arm (360 runs), no exact or five-token partial canary was recovered from post-input persistent state under our canary family, injection route, observer, and five-round horizon (evolve-arm one-sided 95\% upper bound 2.5\%). Removing the fast-round length term, which carries 85\% of the heuristic score weight, sharply lowers recorded scores for DeepSeek and Qwen, but exactness effects in the primary cohorts are heterogeneous and inconclusive. In four frozen cohorts, 43 of 46 failed runs contain no parser-accepted executable candidate in the recorded pool, so selectors restricted to that pool could have gained only 0--8.3 percentage points. Adding four independent stochastic restarts raises the offline executable oracle from 0.60 to 0.80 at roughly three times the token cost. These results scope where selection and privacy mechanisms could matter in this runtime; they do not provide end-to-end privacy or a general prevalence estimate.

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
- Scope statement: scope-limited empirical audit of persistent state, score interventions, and realized candidate support in a fixed-topology TacoMAS--PlanCraft configuration; not an end-to-end privacy method

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
