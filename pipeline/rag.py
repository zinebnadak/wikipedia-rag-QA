# Ties retrieve() and generate() together 

# FOR RERANKING retrieve(5 candidates) → rerank(top 3) → build context → generate → return
#from pipeline.reranking import rerank
from pipeline.retrieval import retrieve
from pipeline.llm import generate_messages
from langfuse import observe

@observe()
def answer_question(user_query: str, article_title: str) -> dict:
    retrieved_chunks = retrieve(user_query, article_title, n_results=5)
    context = "\n\n".join([c["text"] for c in retrieved_chunks])
    #reranked_chunks = rerank(user_query, retrieved_chunks, top_n=3) #reranking disabeled

    system_prompt = f"""
    You are a knowledgeable and helpful assistant.
    Answer the user's question using only the provided retrieved information.
    If the answer cannot be found, say: "I cannot answer this question based on the provided information."
    Retrieved Context:{context}
    User Query:{user_query}
    """

    messages = [{"role": "system", "content": system_prompt}]
    answer = generate_messages(messages)

    return {
        "llm_answer": answer,
        "chunks": [c["text"] for c in retrieved_chunks]
    }

if __name__ == "__main__":
    print(answer_question("What is the significance of Madrid as capital?", "Madrid"))
    