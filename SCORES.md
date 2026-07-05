# RAGAS Evaluation Scorecard

Article: Madrid 
Eval set: golden_set.json (30 questions)
Model: llama-3.1-8b-instant (Groq) 
Embeddings Model : text-embedding-3-small

| Technique | Faithfulness | Context Precision | Context Recall | Factual Correctness | Comment
|---|---|---|---|---|
| Baseline (dense only) | 0.89 | 0.95 | 0.90 | 0.63 |
| + Contextual embeddings | 0.79 | 0.92 | 0.91 | 0.73 | Contextual embeddings made factual correctness better (+0.10) but hurt faithfulness (-0.10). Means that the LLM is now generating answers that are more factually accurate against ground truth, but occasionally draws on knowledge slightly beyond what the retrieved chunks strictly state. The context summaries are giving the LLM more "awareness" of the topic, which cuts both ways. Context precision dropped slightly (-0.03), means the contextualized embeddings are pulling in slightly less precise chunks in some cases, possibly because the context summaries introduce vocabulary that matches questions about different sections.
| + Hybrid search | ? | ? | ? | ? |
| + Reranking | ? | ? | ? | ? |

## Notes
- AnswerRelevancy (*ResponseRelevancy) gives nan throughout, needs embeddings to compute.
- golden_set_2.json baseline: faithfulness 0.96 | cp 0.95 | cr 0.96 | fc 0.77
- Timeout errors on golden_set_2 run — switched evaluator to gpt-4o for subsequent runs

## Production take on the different evaluation methods 
- Contextual embeddings are a net positive for factual correctness (the metric users care most about "is the answer right?") but come with a faithfulness tradeoff.
