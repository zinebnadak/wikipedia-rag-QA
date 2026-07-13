# FastAPI backend 
# run with: uv run uvicorn app.main:app --reload

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI #with uvicorn as server
from pydantic import BaseModel

from pipeline.ingestion import ingest_article
from pipeline.rag import answer_question

class IngestRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    user_query: str
    article_title: str

app = FastAPI(title="Wikipedia RAG")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")    #web browsers do GET by default so test POST at http://localhost:8000/docs (FastAPI's built-in Swagger UI)
def ingest(req: IngestRequest): #using validated pydantic class as typehint
    return ingest_article(req.url)

@app.post("/chat")
def chat(req: ChatRequest):
    return answer_question(req.user_query, req.article_title)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))



'''
Test 3: ask a question and provide a article on /chat
Try it out -> Json body
'''

'''¨
Test 2: make a @app.post request at http://localhost:8000/docs 
Try it out -> JSOn body with URL to ingest
'''

'''
Test 1: FastAPI
def health():
    return {"status": "ok"}

uvicorn app.main:app --reload
http://localhost:8000/health or whatever you defined in app.get()
'''

'''
Groq test

import os 
from dotenv import load_dotenv
from groq import Groq 
from fastapi import FastAPI

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello in exactly 3 words."}],
)

app = FastAPI()
@app.get("/")
def main()
    return{"message"."Hello World!"}

print(response.choices[0].message.content)
'''