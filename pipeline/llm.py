from dotenv import load_dotenv
import os 
from groq import Groq

load_dotenv()

history = [{"role":"user", "content": "Say hello!"}] #need a history list as input later

def generate_messages(messages :list, stream=False, temperature=0) -> str | Iterator[str]:  #need to explicitly set stream to True
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=temperature,
        stream=stream
    )

    if not stream:
        return response.choices[0].message.content
    
    def stream_generator():
        for chunk in response:
            llm_content = chunk.choices[0].delta.content
            if llm_content is None:
                continue
            yield llm_content
    
    return stream_generator()

    
print(generate_messages(history))
