# RAGAS harness
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness, ResponseRelevancy, ContextPrecision, ContextRecall, FactualCorrectness # ragas.metrics.collections

from openai import OpenAI
from ragas.llms import llm_factory # RAGAS uses an LLM internally to compute faithfulness and answer relevance scores. Telling it which LLM to use.

import json 
from pipeline.rag import answer_question
import time # because of groqs rate limits. Spreads token usage over time so it does not hit the per-minute limit + n_resutls in retrieve to 3 instead of 5
from dotenv import load_dotenv

'''
#ingest your article and make sure it is in Chromadb
from pipeline.ingestion import ingest_article
print(ingest_article("https://en.wikipedia.org/wiki/Madrid"))
'''

load_dotenv()

with open ("eval/golden_set.json", "r") as file:
    golden_set = json.load(file)

samples_list = []

for entry in golden_set:
    llm_answer = answer_question(entry["question"], entry["source_article"])
    # anser_question() returns a dict with 3 chunks (n_results) - {"llm_answer": answer, "chunks": [f'{c["text"]}' for c in text_metadata_distances]}
    samples_list.append(SingleTurnSample(
        user_input = entry["question"],
        retrieved_contexts = llm_answer["chunks"],
        response = llm_answer["llm_answer"],
        reference = entry["ground_truth"]
        ))
    
    #print(llm_answer)
    time.sleep(10)

# Evaluation
dataset = EvaluationDataset(samples=samples_list) 
evaluator_llm = llm_factory("gpt-4o-mini", client=OpenAI())

# All metrics must be initialised metric objects
metrics = [
    Faithfulness(),
    ResponseRelevancy(),
    ContextPrecision(),
    ContextRecall(), 
    FactualCorrectness()
]

evaluation_results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=evaluator_llm
)

print(evaluation_results)