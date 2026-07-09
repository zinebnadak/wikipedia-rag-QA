from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Wikipedia RAG")

@app.get("http://localhost:8000/health")
def health():
    return {"status": "ok"}









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