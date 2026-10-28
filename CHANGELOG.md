# Changelog

## 0.4.0 — 2026-10-28

- Added modules 06–09: 27 retrieval examples, four applications, 12 exercise starters and solutions, quizzes and four source-matched notebooks.
- Added Handbook Q&A with page-aware retrieval, validated quotes, six evaluation cases, a committed offline report and acceptance tests.
- Added current loader adapters, chunk provenance, embedding cache isolation, persistent Chroma manifests, hybrid ranking, exact-extract compression and bounded query rewriting.
- Recorded a reproducible before/after benchmark: 138 to 44 chunks with unchanged source/page hit rate of 5/7. No live quality improvement is claimed.
- Removed the sunset community integration package; PDF/CSV/JSON/text ingestion now uses the core loader interface, pypdf and standard-library readers.
- Extended the glossary and troubleshooting guide, and made basic-installation tests explicitly skip unavailable retrieval extras.
- Eleven modules remain planned. Live provider generation and remote CI remain unverified.

## 0.3.0 — 2026-10-28

- Added six foundation modules: 36 examples, six applications, 18 exercises and solutions, quizzes, diagrams and six executable notebooks.
- Added Smart Ticket Desk with a runnable starter, scoped read-only order loop, reference solution, six acceptance cases and review rubric.
- Added validated triage CSV export, review analysis, structured-output fixtures and narrowly scoped fallback behavior.
- Added deterministic SVG/PNG tent diagrams, a 52-term foundation glossary and reproduced troubleshooting examples.
- Extended offline network/tracing protection to all lesson CLIs and moved test protection to the repository root.
- Updated langchain-core to the newly verified 1.7.1 patch; added notebook execution and source-parity checks.
- Later tiers remain planned. Live provider generation and remote CI have not been verified.

## 0.2.0 — 2026-10-28

- Added the installable `common` package, bounded dependency ranges, tier extras and uv lockfile.
- Added provider-neutral chat/embedding helpers, explicit fakes, secret-safe output and optional tracing.
- Added setup, first-call, smoke, coverage, API and link-check commands.
- Generated the synthetic Brightwave datasets and ten-page handbook with source Markdown and checksums.
- Added offline tests, CI configuration, contribution guidance and issue templates.
- Teaching modules and capstones remain scheduled for later phases; this release is the foundation.

## Phase 1 plan — 2026-10-27

- Verified package releases and drafted the 21-module, 139-example coverage contract.
- Added the repository inventory, learning path and upstream compatibility decisions.
