import time # Wraps Groq API call in a for loop that retries up to 3 times. 
from dotenv import load_dotenv
import os 
from groq import Groq, RateLimitError
from typing import Iterator

load_dotenv()

def generate_messages(messages: list, stream=False, temperature=0) -> str | Iterator[str]: #need to explicitly set stream to True
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=temperature,
                stream=stream
            )
            break
        except RateLimitError:
            if attempt < max_retries - 1:
                wait = 30 * (attempt + 1)
                print(f"Rate limit hit, waiting {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise

    if not stream:
        return response.choices[0].message.content

    def stream_generator():
        for chunk in response:
            llm_content = chunk.choices[0].delta.content
            if llm_content is None:
                continue
            yield llm_content

    return stream_generator()
