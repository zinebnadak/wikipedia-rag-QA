# FUTURE.md

Techniques considered and deferred. Add only when evals show
a specific failure they would fix, or a client requires them.

## Retrieval
- Query rewriting — reframe user question before retrieval
- HyDE — embed a hypothetical answer, retrieve against that
- Multi-query expansion — generate N query variants, merge results
- Parent-document retrieval — retrieve small chunks, return larger parent
- Adaptive routing — classify query type, pick retrieval strategy
- Precision@k per-query logging — with a Langfuse 

## Chunking
- Semantic chunking — split on embedding similarity shifts
- Sliding window with overlap — reduce context loss at chunk boundaries
- Late chunking — embed full document, slice vectors after

## Architecture
- Graph RAG — build entity relationship graph over corpus
- Multi-hop reasoning — chain retrievals for complex questions
- Caching layer — skip re-embedding unchanged chunks on re-ingest
- Async context generation — batch Groq calls concurrently (production gap noted in commit)

## Eval
- Per-query Precision@k logging — via Langfuse
- Adversarial eval set — questions designed to break retrieval
- Cross-article retrieval eval — multi-article knowledge base

