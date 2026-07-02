# one-time script to add ground truths to your specific golden set, call it once. Target article, golden set hard-coded
# "only run this whole code when the file is executed directly, not when some function is imported elsewhere."

from dotenv import load_dotenv
import json 
from openai import OpenAI
from pipeline.chunking import chunk_article_data
from scraper.wikipedia import get_article

load_dotenv()
client = OpenAI()

# golden set uses "" for no subsection, chunks use None. To compare both need to be equal first
def normalize(value):
    if value is None or value == "":
        return None
    return value


if __name__ == "__main__":  # golden_set: list[dict], chunks: list[dict]) -> list[dict]:
    chunks = chunk_article_data(get_article("Madrid"))

    with open("eval/golden_set_2.json", "r") as file:
        golden_set = json.load(file)


    matched = 0
    no_match = 0

    for entry in golden_set: #loop trough list
        matching_chunk = None 
        for chunk in chunks:
            if (normalize(chunk["section"]) == normalize(entry["source_section"]) and
                normalize(chunk["subsection"]) == normalize (entry["source_subsection"])): #index the dict 
                matching_chunk = chunk
                break

        if matching_chunk is None:
            no_match += 1
            print(f"NO CHUNK MATCH: {entry['question']}")
        else: 
            matched += 1
            print(f"MATCHED! From golden questions set: {entry['source_section']} | {entry['source_subsection'] or "None"} -> From data: {matching_chunk['section']} | {matching_chunk['subsection']}")
            
            response = client.responses.create(
                model = "gpt-4o-mini",
                input = f"""
                You are extracting a factual answer from a Wikipedia excerpt.
                Excerpt: {matching_chunk["text"]}\n\n
                Question: {entry["question"]}\n\n
                
                Provide a concise, direct answer using ONLY information stated in the excerpt above.
                Do not add outside knowledge. Do not speculate.
                If the excerpt does not contain the answer, respond exactly with: "Not found in excerpt.
                """,
                temperature = 0
                )
            entry["ground_truth"] = response.output_text
    
    with open("eval/golden_set_2.json", "w") as file:
        json.dump(golden_set, file, indent=2)

    print(f"\nTotal matched: {matched} / {matched + no_match}\nDone. {matched} ground truths written to golden set")
    
