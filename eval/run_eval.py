# RAGAS harness

'''
Note: Running this script will take some time! Count with 10-15 minutes :)
Each answer_question() call = scrape + embed + retrieve + Groq LLM call
Then RAGAS makes its own LLM calls during evaluation...
30 questions × 4 metrics × 1 LLM call each = ~120 OpenAI API calls + time.sleep(10) between each question adds 30 × 10 = 5 minutes of deliberate waiting before even starting eval. 
'''

'''
#ingest your article and make sure it is in Chromadb
from pipeline.ingestion import ingest_article
print(ingest_article("https://en.wikipedia.org/wiki/Madrid"))
'''

from dotenv import load_dotenv

import json

from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness, ContextPrecision, ContextRecall, FactualCorrectness #,ResponseRelevancy             ragas.metrics.collections
from openai import OpenAI
from ragas.llms import llm_factory # RAGAS uses an LLM internally to compute faithfulness and answer relevance scores. Telling it which LLM to use.

load_dotenv()

pipeline_outputs_file = "golden_set_2_outputs.json"
# Reading cached data for eval 
with open(f"eval/{pipeline_outputs_file}", "r") as file:
    pipeline_outputs = json.load(file)

samples_list = []

for entry in pipeline_outputs:
    samples_list.append(SingleTurnSample(
        user_input=entry["user_input"],
        retrieved_contexts=entry["retrieved_contexts"],
        response=entry["response"],
        reference=entry["reference"]
    ))

# Evaluation
dataset = EvaluationDataset(samples=samples_list) 
client = OpenAI(timeout=30.0)
evaluator_llm = llm_factory("gpt-4o", client=client, max_tokens=2000)

# All metrics must be initialised metric objects
metrics = [
    Faithfulness(),
    #ResponseRelevancy(),
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