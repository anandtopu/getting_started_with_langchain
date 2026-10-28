# Measured retrieval comparison

Executed offline on 2026-10-28 against the committed synthetic policies and handbook. The [full report](before_after.json) records the corpus hash, all retrieved sources/pages, answers and per-question scores. Eight developer-visible regression questions are used; seven are answerable and one is unknown. Gold labels are read only for scoring.

| Measurement | Baseline | Candidate |
|---|---:|---:|
| Chunk size (characters) | 160 | 450 |
| Target overlap (characters) | 0 | 80 |
| Indexed chunks | 138 | 44 |
| Source/page hit rate at 3 | 0.7142857142857143 | 0.7142857142857143 |
| Keyword correctness proxy | 0.625 | 0.625 |
| Exact-extract support | 1.0 | 1.0 |

Both systems retrieve at most three chunks. The baseline uses 160-character chunks with no overlap and one BM25 query. The candidate uses 450-character chunks, target overlap 80, generic synonym expansion and reciprocal-rank fusion. Multiple settings change together, so this comparison cannot isolate the effect of any one technique. The candidate has 68.1% fewer chunks; this is an index-footprint result, not a measured storage-byte or latency saving.

Source/page misses: baseline ['rag-05', 'rag-08']; candidate ['rag-05', 'rag-08']. Read those rows before tuning. The observed hit-rate difference is +0.0000; there is no demonstrated retrieval-accuracy improvement. Keeping the original simpler approach is reasonable when the larger chunks add context without improving your target metric. A larger held-out set is needed before generalising.

Offline generation is a generic word-overlap extractive fixture, not a language model. Keyword correctness can pass an incorrect statement containing the expected words. Exact-extract support only shows that the answer is copied from a citation; an irrelevant copied sentence can pass. Neither is semantic correctness or faithfulness, and no offline LLM-judge scores are included. The unknown case is scored for abstention separately and excluded from source-hit rate.

Reproduce from the repository root:

```text
uv run --extra rag python modules/09_advanced_rag/use_case/rag_benchmark.py --offline
uv run --extra rag pytest tests/test_rag_contracts.py -k benchmark
```

The command writes `.runtime/rag_benchmark.json`; the test compares a fresh run with the committed report exactly. Live mode adds real vector retrieval to the candidate and actual model generation, so it is a different experiment. Budget up to 16 generations plus embeddings, retain its report separately, and inspect numeric boundaries and unsupported claims manually. No hosted or Ollama quality result is claimed here.
