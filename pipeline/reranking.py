'''
After whatever list of chunks retrieval gave you - not all *5 are equally useful for answering the specific question asked. 
Reranking takes a list of (question, chunk_text) pairs and returns a score per pair. 
Higher score = more relevant to the question. 
Reranking works best with more candidates to choose from. (increasing n_results)

In my case: hybrid search gives me the candidates, reranking refines the order. 
They complement each other well, but neither requires the other.
'''

from pipeline.retrieval import retrieve

model = None

def rerank(question: str, chunks: list[dict], top_n: int = 3) -> list[dict]: # scores all 5 from retrieve() and returns the best 3
    global model
    if model is None:   #lazy loading, eg load only when this function (rerank) is called for the first time, to prevent timeout error on render
        from sentence_transformers import CrossEncoder
        model = CrossEncoder("BAAI/bge-reranker-base") #downloading the BGE-Reranker model (1.11GB) from HuggingFace- downloads once and caches in ~/.cache/huggingface/hub/
    
    pairs = [(question, chunk["text"]) for chunk in chunks]
    scores = model.predict(pairs)
    ranked = sorted(zip(chunks, scores), key = lambda x: x[1], reverse=True) #lambda is sorted()´s way to  know what to compare when ordering the tuples. "for each item, use the second element (the score) as the comparison value."
    return [chunk for chunk, score in ranked[:top_n]]


if __name__ == "__main__":
    chunks = retrieve("What is the significance of Madrid as capital?", "Madrid")
    results = rerank("What is the significance of Madrid as capital?", chunks)
    print(f"Got {len(results)} chunks after reranking")
    print(results[0]["metadata"])

