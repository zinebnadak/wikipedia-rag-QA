import json
from dotenv import load_dotenv
from llama_index.core import Document
from llama_index.core.evaluation import DatasetGenerator
from llama_index.llms.openai import OpenAI
from scraper.wikipedia import get_article

try: 
    load_dotenv()

    article_loader = get_article("Madrid")
    document = Document(
        text=article_loader["text"],
        metadata={"title" : article_loader["title"], "page_id" : article_loader["page_id"]})

    llm = OpenAI(model="gpt-4o-mini")

    generator = DatasetGenerator.from_documents(
        documents=[document],
        llm=llm,
        num_questions_per_chunk=3,
        show_progress=True,
    )

    dataset = generator.generate_dataset_from_nodes()

    
    try:
        pairs = [
        {
            "question": question,
            "ground_truth": dataset.responses[qid], #qid= query ID 
            "source_article": "Madrid"
        }
        for qid, question in dataset.queries.items()
        if qid in dataset.responses
    ]
        
        with open("eval/golden_set.json", "w") as file :
            json.dump(pairs, file , indent=2)
            print(f"Generated {len(pairs)} Q&A pairs")
    except Exception as e: 
        print(f"Generating pairs error: {e}")
    
    
except Exception as e: 
    print(f"Other Error: {e}")

print(list(dataset.responses.items())[:2])