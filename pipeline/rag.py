# Ties retrieve() and generate() together 

# FOR RERANKING retrieve(5 candidates) → rerank(top 3) → build context → generate → return
from pipeline.retrieval import retrieve
from pipeline.reranking import rerank


from pipeline.llm import generate_messages

def answer_question(user_query: str , article_title: str) -> dict:
    retrieved_chunks = retrieve(user_query, article_title, n_results=5)
    reranked_chunks = rerank(user_query, retrieved_chunks, top_n=3)
    context = "\n\n".join([c["text"] for c in reranked_chunks])

    system_prompt = f"""
    You are a knowledgeable and helpful assistant.
    Answer the user's question using only the provided retrieved information.
    Provide a complete and detailed answer — don't truncate information that's available in the context.
    If the answer cannot be found, say: "I cannot answer this question based on the provided information.
    Do not provide any other information or guess.
    Retrieved Context:{context}
    User Query:{user_query}
    """

    messages = [{"role": "system", "content": system_prompt}]
    answer = generate_messages(messages)

    '''
    conversation_history = []
    messages += conversation_history
    messages.append({"role": "user", "content": user_query})
    '''

    return {
    "llm_answer": answer,
    "chunks": [c["text"] for c in reranked_chunks]
    }


if __name__ == "__main__":
    print(answer_question("What is the significance of Madrid as capital?", "Madrid")) # returns top three chunks and llm answer using *top three chunks as context