# RAGAS Evaluation Scorecard

Article: Madrid 
Eval set: golden_set.json (30 questions)
Model: llama-3.1-8b-instant (Groq) 
Embeddings Model : text-embedding-3-small

| Technique | Faithfulness | Context Precision | Context Recall | Factual Correctness |
|---|---|---|---|---|
| Baseline (dense only) | 0.89 | 0.95 | 0.90 | 0.63 |
| + Contextual embeddings | ? | ? | ? | ? |
| + Hybrid search | ? | ? | ? | ? |
| + Reranking | ? | ? | ? | ? |

## Notes
- AnswerRelevancy (*ResponseRelevancy) gives nan throughout, needs embeddings to compute.
- golden_set_2.json baseline: faithfulness 0.96 | cp 0.95 | cr 0.96 | fc 0.77
- Timeout errors on golden_set_2 run — switched evaluator to gpt-4o for subsequent runs