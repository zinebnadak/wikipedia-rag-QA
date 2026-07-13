# Streamlit Frontend
# also run app/main.py (backend) simultaniously

import streamlit as st
import requests 

st.title("Chat with Wikipedia")

# Ingest
url = st.text_input("Enter a valid Wikipdia URL and have a chat!") #requests sends url to FastAPI endpoint

if st.button("Ingest"): #runs only when the user clicks  
    with st.spinner("Ingesting article... this may take a minute"): #URL → extract title → scrape article → chunk → embed chunks → store in ChromaDB + Groq API calls (one context summary per chunk)
        ingest_response = requests.post(   #call with 'post' to use the endpoint
            "https://wikipedia-rag-qa.onrender.com/ingest", #Render URL
            json={"url": url}
            ) # check return with st.write(ingest_response.status_code) and st.write(ingest_response.text)

        ingest_result = ingest_response.json() #the response comes back as a raw Response object. Now its a python dict.
        st.session_state["article_title"] = ingest_result["article"]
        st.success(f"Ingested {ingest_result['chunks']} chunks from the article {ingest_result['article']}")
    

# Chat
if "article_title" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    question = st.chat_input(f'Ask a question about the article "{st.session_state['article_title']}"')
    if question:
        st.session_state["messages"].append({"role": "user", "content": question})
        chat_response = requests.post(
            "https://wikipedia-rag-qa.onrender.com/chat",   #Render URL
            json={
                "user_query": question,
                "article_title": st.session_state["article_title"]}
        )
        chat_result = chat_response.json()
        answer = chat_result["llm_answer"]

        st.session_state["messages"].append({"role":"assistant", "content": answer})

        st.rerun()



