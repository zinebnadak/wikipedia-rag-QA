# This file is made so that you dont have to rerun the whole pipeline (answer_question() call = scrape + embed + retrieve + Groq LLM call) for each eval testing. Use the answers stored in eval/pipeline_outputs.json

'''
#ingest your article and make sure it is in Chromadb
from pipeline.ingestion import ingest_article
print(ingest_article("https://en.wikipedia.org/wiki/Madrid"))
'''

import json 
from dotenv import load_dotenv
from pipeline.rag import answer_question
import time # because of groqs rate limits. Spreads token usage over time so it does not hit the per-minute limit + n_resutls in retrieve to 3 instead of 5

load_dotenv()

golden_set_file = "golden_set_outputs_baseline"   # CHANGE THIS FOR EVAL to the targeted question set inside eval/ folder without the ".json"
technique_name = "reranking"                  # CHANGE THIS to the current technique 

with open (f"eval/{golden_set_file}.json", "r") as file:
    golden_set = json.load(file)
    
samples_list = []

for entry in golden_set:
    llm_answer = answer_question(entry["question"], entry["source_article"]) # anser_question() returns a dict with 3 chunks (n_results) - {"llm_answer": answer, "chunks": [f'{c["text"]}' for c in text_metadata_distances]}
    samples_list.append({
        "user_input" : entry["question"],
        "retrieved_contexts" : llm_answer["chunks"], #??? # chunks truncated to 1500 chars for RAGAS compatibility, only for the evaluator's judgment not the answer,  risk if the answer references something only mentioned in the second half of a long chunk
        "response" : llm_answer["llm_answer"],
        "reference" : entry["ground_truth"],
        "source_article" : entry["source_article"] # but not valid in SingleTurnSample
        })
    
    time.sleep(10)

with open(f"eval/{golden_set_file}_outputs_{technique_name}.json", "w") as results_file: 
    json.dump(samples_list, results_file, indent=2)

print(len(samples_list))

