'''
After whatever list of chunks retrieval gave you - not all *5 are equally useful for answering the specific question asked. 
Reranking takes a list of (question, chunk_text) pairs and returns a score per pair. 
Higher score = more relevant to the question. 
Reranking works best with more candidates to choose from. (increasing n_results)

In my case: hybrid search gives me the candidates, reranking refines the order. 
They complement each other well, but neither requires the other.
'''

from sentence_transformers import CrossEncoder
from pipeline.retrieval import retrieve
model = CrossEncoder("BAAI/bge-reranker-base") 

def rerank(question: str, chunks: list[dict], top_n: int = 3) -> list[dict]: # scores all 5 from retrieve() and returns the best 3
    pairs = [(question, chunk["text"]) for chunk in chunks]
    scores = model.predict(pairs)
    ranked = sorted(zip(chunks, scores), key = lambda x: x[1], reverse=True) #lambda is sorted()´s way to  know what to compare when ordering the tuples. "for each item, use the second element (the score) as the comparison value."
    #return [chunk for chunk, score in ranked[:top_n]]

    return scores



chunks = retrieve("What is the significance of Madrid as capital?", "Madrid")
print(rerank("What is the significance of Madrid as capital?", chunks))



