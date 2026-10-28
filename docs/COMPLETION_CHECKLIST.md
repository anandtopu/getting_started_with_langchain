# Completion evidence

This checklist distinguishes the implemented foundations tier from the complete course. Final acceptance requires the entire original scope; phased checks do not waive it.

## Phase 3 scope

- [x] Modules 00–05: 36 examples, six realistic applications, 18 runnable exercises and complete solutions.
- [x] Required README sections, per-example analogies/diagrams, quizzes and reproduced error/fix explanations.
- [x] Six notebooks execute offline, mirror the script source and retain cleared committed outputs.
- [x] Smart Ticket Desk starter, solution, rubric, six evaluation cases and acceptance tests.
- [x] Structured extraction, customer-scoped reads, bounded loops, unknown-tool handling and source-parity tests.
- [x] Dependency refresh, lint/format, legacy scan and phase-aware coverage/link checks.
- [ ] Actual hosted and Ollama generation (explicitly deferred; fake outputs are not quality evidence).

## Phase 2 scope

- [x] Installable shared package, bounded dependency groups/extras and uv lockfile.
- [x] Four chat providers and independent embedding configuration through central factories.
- [x] Explicit fake chat/embeddings, friendly CLI errors and credential-redacted output.
- [x] Synthetic dataset generator, generated files, manifest and ten-page handbook.
- [x] Setup, first-call, environment, smoke, coverage, link and legacy-API scripts.
- [x] Root README, learning path, contributing/conduct/license/changelog and CI configuration.
- [x] Meaningful offline tests and opt-in live marker.

The dated [verification notes](VERIFICATION_NOTES.md) record executed checks and limitations. Presence of CI configuration does not mean remote CI has run.

## Complete repository acceptance — pending later phases

- [ ] All 21 modules have every required teaching component and complete feature coverage.
- [ ] All five checkpoints and capstones have runnable starters, solutions, tests and evaluation evidence.
- [ ] Every notebook runs top to bottom with outputs cleared.
- [ ] Each applicable example has an actual Ollama and hosted-provider run recorded.
- [ ] All planned links resolve to implemented files; strict local and external link checks pass.
- [ ] CI passes on Ubuntu and Windows for Python 3.12–3.14, with macOS smoke verification.
- [ ] Measured retrieval and agent evaluation reports distinguish offline fixtures from live quality.
- [ ] Production API/UI, human approval, security controls, Docker and deployment paths are verified.
- [ ] Five printable cheatsheets, 60-term glossary and full troubleshooting/migration guides are complete.
- [ ] Public GitHub repository is published and a clean-clone quick start is verified.

At final acceptance run `uv run python scripts/check_coverage.py --require-complete` and `uv run python scripts/check_links.py` without planned-file allowances. Both are expected to fail while construction is incomplete.
