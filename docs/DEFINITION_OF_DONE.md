# Completion checklist

All eight implementation phases are present. Final verification is being recorded here; unchecked items are not claims of success. The customer-support application remains below its release quality bar (4/6 complete scripted contracts).

- [x] Final full offline suite: 621 passed, two explicit live skips. Fresh minimal install: 240 passed, 349 optional/live skips. All five untouched capstone starters intentionally fail their learning assertions.
- [x] Ruff lint/format, legacy scanner, strict inventory and local/external links passed with zero violations and zero deferred targets.
- [ ] Remote CI across Ubuntu/Windows Python 3.12-3.14: pending publication.
- [x] All 21 modules have the required lesson sections, examples, use case, exercises/solutions, quiz and notebook.
- [x] Five capstone specs, starters, reference solutions, tests, evaluation sets and rubrics are implemented.
- [x] Five one-page PDF cheatsheets were rendered and visually inspected.
- [x] All 141 smoke targets and all 21 notebooks passed; minimal smoke passed 38 targets with 103 explicit optional skips.
- [x] The capstone container passed authenticated policy chat/history as UID 10001 with read-only source and writable runtime.
- [ ] Every example on Ollama and a hosted provider: no configured provider keys or Ollama runtime on this host. Offline fixture runs do not satisfy this requirement.
- [ ] A real model call within ten minutes from a fresh clone: not measured; model/dependency downloads and provider access vary.
- [ ] Final public publication and clean-clone check: pending.

The API/Streamlit/MCP paths are checked with synthetic identities and network-denied fixtures. Live provider reasoning, hosted tracing, Studio/cloud deployment and real customer operations are not claimed verified. The known return/shipping misses are retained as regression evidence; do not lower the release threshold to hide them.
