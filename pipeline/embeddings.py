from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def embed(texts: list[str]) ->list[list[float]]: # list of vectors (list of decimals)
    response = client.embeddings.create(
        input = texts,
        model = "text-embedding-3-small"
    )
    return [vector.embedding for vector in response.data]


