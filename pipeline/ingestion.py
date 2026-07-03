# URL → extract title → scrape article → chunk → embed chunks → store in ChromaDB

import chromadb

from scraper.wikipedia import get_article, extract_title_from_url
from pipeline.chunking import chunk_article_data
from pipeline.embeddings import embed 

chroma_client = chromadb.PersistentClient(path="chroma_db")   # persistent Client and collection here  , but in a real production app, I'd use dependency injection for both ( eg. FastAPI's Depends() system ) to manage the ChromaDB client lifecycle. The function creates/returns the client, and FastAPI injects it into each endpoint that needs it. 
collection = chroma_client.get_or_create_collection(name="wiki-rag")  

def ingest_article(url: str) -> dict:
    title, lang = extract_title_from_url(url)

    article_data = get_article(title)
    if article_data is None:
        return {"ingestion_status":"article fetching error", "message": f"Failed to fetch '{title}' from Wikipedia"}
    
    article_data_chunks = chunk_article_data(article_data)
    embeddings_list = embed([chunk["text"] for chunk in article_data_chunks])

    try: 
        collection.upsert(
            ids=[f'{chunk["page_id"]}_{chunk["section"]}_{chunk["subsection"] or "none"}' for chunk in article_data_chunks], # building a unique id form page_id + section + sub_section ,
            documents=[chunk["text"] for chunk in article_data_chunks],
            embeddings= embeddings_list,
            metadatas= [
                {
                    "article_title": chunk["article_title"],
                    "section": chunk["section"],
                    "subsection": chunk["subsection"] or "none",
                    "page_id": chunk["page_id"]
                }
                for chunk in article_data_chunks
            ]
        )
        return {"status":"ok", "article":f"{title}", "language":f"{lang}", "chunks": len(article_data_chunks)}

    except Exception as e:
        return {"status":"error", "message": f"Failed to update/insert documents to ChromaDB: {str(e)}"}


# results = collection.get(where={"article_title": "Madrid"})
# print(len(results["ids"])) #total chunks with the article title
# print(collection.count()) #total chunks in chromadb 


