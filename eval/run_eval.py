# RAGAS harness
import json 
from pipeline.rag import answer_question
import time # because of groqs rate limits. Spreads token usage over time so it does not hit the per-minute limit + n_resutls in retrieve to 3 instead

'''
#ingest your article and make sure it is in Chromadb
from pipeline.ingestion import ingest_article
print(ingest_article("https://en.wikipedia.org/wiki/Madrid"))
'''

with open ("eval/golden_set.json", "r") as file:
    golden_set = json.load(file)


for entry in golden_set[:3]:
    llm_answer = answer_question(entry["question"], entry["source_article"])
    print(llm_answer)
    time.sleep(10)