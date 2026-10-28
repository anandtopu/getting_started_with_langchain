# Phase 8 cross-file integration review

## Scope

Trace actual user and data paths across the capstone entry points, shared helpers, persistent state, model factory, evaluation labels and deployment configuration.

## Findings and boundary checks

| Boundary | Evidence | Result / limit |
|---|---|---|
| PDF upload -> page metadata -> chunking -> hybrid retrieval -> answer -> UI | DocuMind UI interaction/session isolation and PDF boundary tests; three independent cases. | Provenance preserved; own-document input supported. Self-contained questions required. No hostile-parser isolation or OCR claim. |
| UI -> FastAPI -> authenticated principal -> owned history/tools | Existing module 18 UI tests plus capstone API ownership and reopen tests. | Shared UI and actual copilot factory compatible. Tokens never come from model-controlled identity fields. |
| Copilot policy tool -> nested model -> call ledger | Five-call reservation and two-policy-call test, with retries zero. | Three outer calls plus at most two nested calls fit the reservation. Count ceilings are not monetary invoice caps. |
| Customer return -> trusted warehouse facts -> manager decision -> ledger | Approval/rejection contract rerun with copilot factory; existing stale/changed/replay tests retained. | No write on rejection; ownership/quote checks survive review. Local synthetic notification only. |
| Analyst proposal -> SQLite authorizer -> measured rows -> chart | Private-column/write/function denials; totals 200, 470 and 7,978,950 cents. | Staff analytics only. Model prose remains independently ungraded. |
| Planner -> Send workers -> reducer -> writer/critic -> file | Accepted and exhausted evaluation cases, known source/exact quote gate. | Bounded revisions; rejected drafts never become finished reports. Scripted critic does not prove relevance. |
| Host approval -> wrapper -> MCP server -> SQLite transaction | Memory and real stdio evals, owner/altered receipt tests, repeat application and task completion. | Permission enforced at server even if wrapper bypassed; local host is trusted. |
| Container -> configured factory -> runtime volume -> saved policy trace | Actual built image, UID 10001, read-only source, authenticated SSE and persisted tool history. | Verified locally with explicit Podman context/VM loopback. No registry/cloud deployment. |
| Answer function -> independent expected labels -> release flag | 19 cases: 17 complete passes; two known policy misses. | Default evaluation completion is distinct from strict release success. |
| Minimal install -> optional-test gating; full install -> all capstones | Separate environments and complete suites. | Minimal optional skips are labelled; full suite only skips explicit live tests. |
| Notebook runner -> kernel -> installed packages | All notebooks use a temporary kernel spec naming the current interpreter; regression test captures command and environment. | Avoids unrelated global Jupyter installations. |

## Validation

All seed data remain unchanged. Every model is constructed through common.models; evaluated paths use temperature zero. Root and tier tests deny network by default. The legacy scanner permits old teaching fragments only in the migration guide. See [completion checklist](../DEFINITION_OF_DONE.md) for observed final counts and unresolved live/CI evidence.

## Open questions

Single-process admission and SQLite are not a distributed deployment. A Postgres checkpoint probe is not a full migration. Real-model accuracy, live search, cloud tracing/Studio, production identity, malicious-PDF isolation and broad DLP are not asserted.
