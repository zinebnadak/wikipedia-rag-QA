# RAGAS Evaluation Scorecard

Article: Madrid 
Eval set: golden_set.json (30 questions)
Model: llama-3.1-8b-instant (Groq) 
Embeddings Model : text-embedding-3-small

| Technique | Faithfulness | Context Precision | Context Recall | Factual Correctness | Comment
|---|---|---|---|---|
| Baseline (dense only) | 0.89 | 0.95 | 0.90 | 0.63 | gpt-4o
| + Contextual embeddings | 0.79 | 0.92 | 0.91 | 0.73 | gpt-4o, Contextual embeddings made factual correctness better (+0.10) but hurt faithfulness (-0.10). Means that the LLM is now generating answers that are more factually accurate against ground truth, but occasionally draws on knowledge slightly beyond what the retrieved chunks strictly state. The context summaries are giving the LLM more "awareness" of the topic, which cuts both ways. Context precision dropped slightly (-0.03), means the contsextualized embeddings are pulling in slightly less precise chunks in some cases, possibly because the context summaries introduce vocabulary that matches questions about different sections.
| + Hybrid search | 0.90 | 0.94 | 0.95 | 0.96  | gpt-4o
| + Reranking | 0.94 | 0.89 | 0.94 | 0.76 |

## Notes
- AnswerRelevancy (*ResponseRelevancy) gives nan throughout, needs embeddings to compute.
- golden_set_2.json baseline: faithfulness 0.96 | cp 0.95 | cr 0.96 | fc 0.77
- Timeout errors on golden_set_2 run — switched evaluator to gpt-4o for subsequent runs

**Known limitations:**
- Some eval runs had OpenAI rate limit / timeout errors causing certain samples to return `nan` — scores are averages over completed samples only, not always the full 30. For example in this case reranking eval had partial timeouts — faithfulness and factual correctness from ~17-25 successful samples.


## Production take on the different evaluation methods 
- Contextual embeddings are a net positive for factual correctness (the metric users care most about "is the answer right?") but come with a faithfulness tradeoff.

**My take on eval infrastructure reliability:**
My eval had OpenAI rate limits and timeouts causing some samples to drop — scores
are directional, not perfectly comparable across runs. In production I'd fix this
with a dedicated OpenAI org with higher TPM limits, async eval calls, and chunk
truncation at eval time only. I know exactly what needs to change.