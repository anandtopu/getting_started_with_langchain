# 2 | Retrieval and grounding

## Start with provenance

A Document contains page_content and metadata. Establish source, page and stable ID before splitting. Chunk overlap preserves context but increases indexing cost.

## Search choices

BM25 scores shared words. Embeddings encode similarity; fake embeddings only test interfaces. InMemoryVectorStore is temporary; Chroma persists a collection. Keep embedding model, dimensions and collection identity consistent.

## RAG flow

Load -> split -> embed/index -> retrieve -> prompt -> answer -> validate. Context is untrusted evidence, never a higher-priority instruction. Allow an explicit unknown answer.

## Improve retrieval

Compare BM25, vectors and reciprocal-rank fusion on held-out questions. Reranking changes order; compression removes irrelevant text. Parent retrieval returns larger context around a small matching child.

## Citations and evaluation

Validate source IDs, page numbers and exact quotes against retrieved text. Measure retrieval hit rate, quote support and answer correctness separately. A faithful quote can answer the wrong question.

## Conversation

Rewrite a follow-up using bounded history before searching. Rewriting can drift; retain the original question and test follow-ups. DocuMind initially asks self-contained questions.

## Try it

```text
uv sync --extra apps
uv run --no-sync python capstones/01_documind/solution.py --offline
uv run --no-sync pytest capstones/01_documind
```

[Print the one-page PDF](tier_2_rag.pdf). Commands run from the repository root.
