import json
from dotenv import load_dotenv
from llama_index.core.evaluation import DatasetGenerator
from llama_index.core import Document
from llama_index.llms.openai import OpenAI
from scraper.wikipedia import get_article

article_loader = get_article("Madrid")
document = Document(
    page_content=article_loader["text"],
    metadata={"title" : article_loader["title"], "page_id" : article_loader["page_id"]})

llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

generator = TestsetGenerator.from_langchain(
    llm=llm,
    embedding_model=embeddings,
)

testset = generator.generate_with_langchain_docs(
    documents = [document], 
    testset_size=30,
    query_distribution=default_query_distribution
    )

data_frame = testset.to_pandas()
data_frame.to_json("eval/golden_set.json", orient="records", indent=2)
print(f"Generated {len(data_frame)} questions")



