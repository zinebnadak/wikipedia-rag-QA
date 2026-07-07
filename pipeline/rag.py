# Ties retrieve() and generate() together 

# FOR RERANKING
from pipeline.retrieval import retrieve
from pipeline.reranking import rerank


from pipeline.llm import generate_messages

def answer_question(user_query: str , article_title: str) -> dict:
    text_metadata_distances = retrieve(user_query, article_title) # retrieves the top 5 most relevant chunks 
    context = "\n\n".join([c["text"] for c in text_metadata_distances])

    system_prompt = f"""You are a knowledgeable and helpful assistant. 
    You must answer the user's question using only the provided retrieved information.
    If the answer cannot be found within the retrieved text, output exactly: "I cannot answer this question based on the provided information." 
    Do not provide any other information or guess.
    Retrieved Context:{context}
    User Query:{user_query}
    """


    #rerank between retrieve() and generate()

    messages = [{"role": "system", "content": system_prompt}]
    answer = generate_messages(messages)

    '''
    conversation_history = []
    messages += conversation_history
    messages.append({"role": "user", "content": user_query})
    '''

    return {"llm_answer": answer, "chunks": [f'{c["text"]}' for c in text_metadata_distances]}    #returning the chunks for RAGAS later


# print(answer_question("What is computer science?", "Computer science"))