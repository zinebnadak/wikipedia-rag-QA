# Retrieval strategies: dense (used for RAGAS baseline), then +BM25 (Best Matching 25), then hybrid search (combine dense with BM25), then +rerank

import chromadb
from pipeline.embeddings import embed
from rank_bm25 import BM25Okapi 
import numpy as np

chroma_client = chromadb.PersistentClient(path="chroma_db")   # persistent Client and collection 
collection = chroma_client.get_or_create_collection(name="wiki-rag")  

def retrieve(question: str , article_title: str , n_results: int=3) -> list[dict]:
    all_chunks = collection.get(where={"article_title": article_title})
    
    # BM25 sparse retrieval
    tokenized = [doc.lower().split() for doc in all_chunks["documents"]] #BM25 works only on individual words (tokens) so it can count word frequencies
    bm25 = BM25Okapi(tokenized) # rank_bm25.BM25Okapi object
    bm25_scores = bm25.get_scores(question.lower().split()) # Numpy array. Returns a score per document ranging from 0 (no matching words) to 28.8 (strong keyword match) BUT  RRF only cares about rank position (1st, 2nd, 3rd...), not the actual score values
    sorted_score_indicies = np.argsort(bm25_scores)[::-1] #indicies (positions), best scores position first
    #sorted_scores = bm25_scores[sorted_score_indicies]
    #rank_bm25 = [f"Document {index}: {score:.4f}" for index, score in zip(sorted_score_indicies, sorted_scores)] # first item: 'Document 0: 28.8495'
    
    # Dense retrieval
    dense_results = collection.query(
        query_embeddings=[embed([question])[0]], # embed the question (1536.. numbers)
        n_results=len(all_chunks["documents"]),  # return all chunks ranked by similarity to the question. Index 0 is the best semantic match, last index is the worst.
        where={"article_title": article_title}
    )

    # RRF merge. Combines both rankings into one: Chunk that ranks high in both keyword match AND semantic similarity rise to the top
    k = 60
    RRF_scores = {}

    for rank, document_index in enumerate(sorted_score_indicies):
        document_id = all_chunks["ids"][document_index]
        RRF_scores[document_id] = RRF_scores.get(document_id, 0) +1 /(k + rank +1)

    for rank, document_id in enumerate(dense_results["ids"][0]):
        RRF_scores[document_id] = RRF_scores.get(document_id, 0) +1 /(k + rank + 1)

    sorted_ids = sorted(RRF_scores, key=RRF_scores.get, reverse=True)[:n_results]
    id_to_index = {doc_id: index for index, doc_id in enumerate(all_chunks["ids"])}
    
    return [
        {
            "text": all_chunks["documents"][id_to_index[doc_id]],
            "metadata": all_chunks["metadatas"][id_to_index[doc_id]]
        }
        for doc_id in sorted_ids
    ]  
    
'''
Test gets top results (of n_results) metadata:

if __name__ == "__main__":
    results = retrieve("What is the significance of Madrid as capital?", "Madrid")
    print(len(results))
    for r in results:
        print(r["metadata"]) 
'''

