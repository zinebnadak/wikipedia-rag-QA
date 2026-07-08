# URL → extract title → scrape article → chunk → embed chunks → store in ChromaDB
# Contextual embeddings : chunk → generate_context_summary(chunk) → embed(summary + chunk["text"]) → store
import chromadb

from scraper.wikipedia import get_article, extract_title_from_url
from pipeline.chunking import chunk_article_data
from pipeline.embeddings import embed 

from dotenv import load_dotenv
from scraper.wikipedia import get_article
from pipeline.llm import generate_messages

chroma_client = chromadb.PersistentClient(path="chroma_db")   # persistent Client and collection here  , but in a real production app, I'd use dependency injection for both ( eg. FastAPI's Depends() system ) to manage the ChromaDB client lifecycle. The function creates/returns the client, and FastAPI injects it into each endpoint that needs it. 
collection = chroma_client.get_or_create_collection(name="wiki-rag")  

def ingest_article(url: str) -> dict:
    title, lang = extract_title_from_url(url)

    article_data = get_article(title)
    if article_data is None:
        return {"ingestion_status":"article fetching error", "message": f"Failed to fetch '{title}' from Wikipedia"}
    
    article_data_chunks = chunk_article_data(article_data)

    #contextual retrieval
    contextualized_texts = [
        generate_chunk_context(article_data, chunk) + "\n\n" + chunk["text"] for chunk in article_data_chunks
        ]
    embeddings_list = embed(contextualized_texts)


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


'''
Test:
results = collection.get(where={"article_title": "Madrid"})
print(len(results["ids"])) #total chunks with the article title
print(collection.count()) #total chunks in chromadb 
'''


def generate_chunk_context(article_data, chunk):    

    messages = [
        {"role": "system", "content": f""" You are a helpful assistant that writes concise context summaries for document chunks.
    Here is a Wikipedia article about {article_data["title"]}: {article_data["text"][:3000]}"""},
            
        {"role": "user", "content": f""" Here is a chunk from the '{chunk["section"]}' section: {chunk["text"]}
    Write 2-3 sentences situating this chunk within the broader article. Be concise and focus on what makes this chunk unique and findable."""}
        ]

    response = generate_messages(messages) #default stream=False
    return response 

'''
Test with uv run python -m pipeline.ingestion
if __name__ == "__main__":
    article = get_article("Madrid")
    chunk = chunk_article_data(article)[0]
    print(generate_chunk_context(article, chunk))

Test what is actually in db:
uv run python -c "
import chromadb
client = chromadb.PersistentClient(path='chroma_db')
collection = client.get_or_create_collection('wiki-rag')
print('Total chunks:', collection.count())
results = collection.get(where={'article_title': 'Computer science'})
print('Computer Science chunks:', len(results['ids']))
"

Begin eval by ingesting. chunks × 1 Groq call each to generate context summaries, then n embeddings, will take some time
if __name__ == "__main__":
    print(ingest_article("https://en.wikipedia.org/wiki/Octopus"))

'''

if __name__ == "__main__":
    print(ingest_article("https://en.wikipedia.org/wiki/Madrid")) #takes about 3 minutes 