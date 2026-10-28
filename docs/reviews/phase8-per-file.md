# Phase 8 per-file review

## Scope

Review against Phase 7 commit a4aaf9a: five capstones, five new shared helpers, service/release extension points, evaluation and inventory scripts, root regression tests, final documentation, dependency metadata and CI. Synthetic seed files are unchanged. Notebook sources are unchanged and their executable paths are rerun. Generated PDFs were checked as rendered pages; ignored runtime output is not published.

## Findings

| ID | Severity | File | Line | Finding | Impact | Recommended fix / status |
|---|---|---|---:|---|---|---|
| R1 | P2 | common/personal_ops.py | 316 | Personal notes could enter raw trace spans when global tracing is enabled. | Unnecessary personal-data export. | Fixed: disable raw tracing around agent execution; server subprocesses disable tracing too. |
| R2 | P2 | common/personal_ops.py | 218 | Discovery initially checked tool names but not their input fields. | A changed server could expose unreviewed arguments. | Fixed: check exact properties and required fields before use. The server still independently checks receipts. |
| R3 | P3 | capstones/02_support_copilot/tests/test_api.py | 27 | Test assumed every valid citation was a policy Markdown path. | Valid handbook evidence incorrectly failed the API test. | Fixed: inspect actual tool citations and require those exact sources in the response. |
| R4 | P2 | docs/DEFINITION_OF_DONE.md | 1 | Live model and cross-platform evidence must not be inferred from offline tests. | Overstated readiness. | Keep unchecked evidence explicit and update only from observed runs. |
| R5 | P1 for customer launch | capstones/02_support_copilot/eval.jsonl | 3 | Returns/shipping miss independently required facts. | Customers could receive an unhelpful policy answer despite valid quotes. | Open: improve retrieval/answer relevance and obtain live/human evidence; strict release remains blocked. |

The final documentation pass also removed stale Phase 2 completion wording from the root FAQ and redirected the older completion page to the current evidence checklist. Capstone time estimates now match the learning-path table.

The nested-call review initially overestimated each policy search as two model calls. Reading common/rag.py confirmed one call per search and retries disabled by the copilot. The five-call reservation is correct (three agent calls plus two nested calls); a two-policy-tool regression test verifies it. No budget defect is claimed.

## File-level observations

| File or repeated family | Review result |
|---|---|
| common/document_chat.py | Size/page/text limits, provenance before chunking, private session index, explicit live consent, quote checks and no raw tracing. Parser isolation is documented as absent. |
| common/copilot.py | SQL ownership remains host-bound; actual retrieval tool and complete HTTP evaluation path; conservative five-call reservation. |
| common/analyst.py | Engine-enforced read-only allowlist, no private columns, statement/function/instruction/row limits, finite repair, chart from measured rows. Staff-only scope is explicit. |
| common/research_crew.py | Distinct bounded plan, read-only workers, reducer merge, finite revisions, exact-source gate before report rendering. Synthetic critic is not semantic validation. |
| common/personal_ops.py | Owner-scoped database, canonical redacted approvals, transaction/replay protection, no approval tool, reviewed schemas, managed subprocess/file lifetimes. Local host trust is explicit. |
| common/service.py; common/release.py | Small extension points preserve authenticated history/review behavior. Explicit temperature zero for evaluated chat. Existing API contracts rerun against both services. |
| Each capstone solution.py and starter.py | Typed finite entry points, central model helper, separate request generation and expected-label scoring, runtime-only writes. Starters intentionally fail their learning targets. |
| DocuMind app.py; Support app.py/api.py | UI versus finite CLI entry points are distinct; no hanging smoke target. Shared UI binds to configured API URL. |
| Personal Ops notes_server.py/tasks_server.py | Host chooses owner/path; stdio stdout reserved for protocol; context managers close clients before diagnostic files. |
| All capstone tests and eval.jsonl files | Actual reference paths exercised; fixed independent expected facts; rejection/exhaustion cases are successful safety outcomes. Known policy quality failures stay visible. |
| New root budget/security/tools/examples/notebooks/evaluation tests | Cover nested calls, private SQL denial, exact approval and owner rejection, actual completion, all finite entry points, active Jupyter interpreter and held-out labels. |
| scripts/evaluate.py | Per-case temporary state, network denial in offline mode, persisted detailed report, nonzero strict release result. Default success means evaluation completed. |
| scripts/check_coverage.py; scripts/check_links.py | Final capstone registration and file gates; strict paths/anchors; UTF-8 manifest read. |
| Dockerfile and ignore files; langgraph.json | Non-root single-worker API; secrets excluded from build context. Studio config intentionally targets a separately documented read-only graph. |
| pyproject.toml; uv.lock; CI workflow | Only project version changes to 1.0.0; locked dependency baseline retained. Strict final checks and full capstone evaluation added to CI. |
| Capstone guides/rubrics/reports; cheatsheets; migration and root docs | Commands use root-relative paths and cross-platform uv syntax. No live/production success implied. Legacy snippets restricted to the migration guide. Five PDFs visually checked. |

## Validation

See [verification notes](../VERIFICATION_NOTES.md) and the [completion checklist](../DEFINITION_OF_DONE.md) for final measured counts. Per-file review is followed by [cross-file integration review](phase8-integration.md).

## Open questions

No hosted keys or Ollama runtime are available for actual provider evaluation. Customer release also requires the two policy cases to pass without weakened assertions.
