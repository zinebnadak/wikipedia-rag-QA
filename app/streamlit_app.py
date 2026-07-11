# Streamlit Frontend
# run with: uv run streamlit run app/streamlit_app.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # tells python to also look at the project root not just /app folder. run with: uv run streamlit run app/streamlit_app.py

import streamlit as st
import requests 
import chromadb
from scraper.wikipedia import extract_title_from_url
import time

#check if article already ingested
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection("wiki-rag")

def is_ingested(article_title: str) -> bool:
    results = collection.get(where={"article_title": article_title})
    return len(results["ids"]) > 0 # If the article is ingested, this list of chunk IDs has items and is True


st.title("Chat with Wikipedia")
# st.subheader("Enter a any valid Wikipdia URL and have a chat!")


# Ingest
url = st.text_input("Enter a valid Wikipdia URL and have a chat!") #requests sends url to FastAPI endpoint

if st.button("Ingest"): #runs only when the user clicks
    title, lang = extract_title_from_url(url)
    if is_ingested(title):
        with st.spinner(f"Loading '{title}' from knowledge base and opening chat..."):
            time.sleep(2)
        st.session_state["article_title"] = title
        st.success(f"Article '{title}' loaded!")    
    else: 
        with st.spinner("Ingesting article... this may take a minute"): #URL → extract title → scrape article → chunk → embed chunks → store in ChromaDB + Groq API calls (one context summary per chunk)
            ingest_response = requests.post(   #call with 'post' to use the endpoint
                "http://localhost:8000/ingest",
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
            "http://localhost:8000/chat",
            json={
                "user_query": question,
                "article_title": st.session_state["article_title"]}
        )
        chat_result = chat_response.json()
        answer = chat_result["llm_answer"]

        st.session_state["messages"].append({"role":"assistant", "content": answer})

        st.rerun()



