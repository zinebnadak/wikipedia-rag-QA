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
    #embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

    generator = DatasetGenerator.from_documents(
        documents=[document],
        llm=llm,
        num_questions_per_chunk=3,
        show_progress=True,
    )

    dataset = generator.generate_dataset_from_nodes()

    
    try:
        questions = list(dataset.queries.values())
        with open("eval/golden_set.json", "w") as file :
            json.dump(questions, file , indent=2)
            print(f"Generated {len(questions)} questions")
    except Exception as e: 
        print(f"Generating questions error: {e}")
    
    
except Exception as e: 
    print(f"Other Error: {e}")

print(list(dataset.responses.items())[:2])