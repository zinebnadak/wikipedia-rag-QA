import json
from dotenv import load_dotenv
from llama_index.core import Document
from llama_index.core.evaluation import DatasetGenerator
from llama_index.llms.openai import OpenAI
from scraper.wikipedia import get_article
from pipeline.chunking import chunk_article_data

try:
    load_dotenv()

    article_loader = get_article("Madrid")
    chunks = chunk_article_data(article_loader)

    documents = [
        Document(
            text=chunk["text"],
            metadata={
                "title": chunk["article_title"],
                "section": chunk["section"],
                "subsection": chunk["subsection"] or "",
            }
        )
        for chunk in chunks
        if len(chunk["text"]) > 200
    ]

    llm = OpenAI(model="gpt-4o-mini")
    all_pairs = []

    for document in documents:
        section = document.metadata.get("section", "Unknown")
        subsection = document.metadata.get("subsection", "")

        try:
            doc_generator = DatasetGenerator.from_documents(
                documents=[document],
                llm=llm,
                num_questions_per_chunk=3,
                show_progress=False,
            )
            doc_dataset = doc_generator.generate_dataset_from_nodes()

            for qid, question in doc_dataset.queries.items():
                all_pairs.append({
                    "question": question,
                    "source_article": "Madrid", #hardcoded
                    "source_section": section,
                    "source_subsection": subsection,
                })

        except Exception as e:
            print(f"Error on section '{section}': {e}")
            continue

    with open("eval/golden_set.json", "w") as f:
        json.dump(all_pairs, f, indent=2)
    print(f"Generated {len(all_pairs)} pairs")

except Exception as e:
    print(f"Main error: {e}")


'''
The terminal output "/Users/nadak/ep-005-wikipedia-rag-QA/.venv/lib/python3.12/site-packages/llama_index/core/evaluation/dataset_generation.py:297: DeprecationWarning: Call to deprecated class QueryResponseDataset. (Deprecated in favor of `LabelledRagDataset` which should be used instead.)
  return QueryResponseDataset(queries=queries, responses=responses_dict)
/Users/nadak/ep-005-wikipedia-rag-QA/.venv/lib/python3.12/site-packages/llama_index/core/evaluation/dataset_generation.py:201: DeprecationWarning: Call to deprecated class DatasetGenerator. (Deprecated in favor of `RagDatasetGenerator` which should be used instead.)
  return cls("

IS NOT an error, it is just an deprecation warning so wait until it finishes slowly
'''