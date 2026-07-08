# Episode 005 - Wikipedia RAG Q&A

> [One sentence single takeaway from this project.]

## The Problem / The Question
Second RAG build. Wikipedia as the data source, same overall pattern as my first project (ha.ax) but rebuilt with evaluation, better chunking, hybrid search, and reranking — because you don't own a pattern after building it once. I also wanted to stress-test it: does a standard RAG pipeline break when the data gets messier? Wikipedia text is noisier than a university website. Inconsistent heading structure, much longer articles, irrelevant sections mixed into the prose, tables and infoboxes interrupting flow. I wanted to measure how a RAG pipeline actually behaves on large, unstructured, real-world corpora.

## What I built
An AI-powered tool that lets you explore and study Wikipedia articles through a retrieval-based chat. 

## Features
- provide a valid wikipedia URL 
- ask questions about the content using natural language
- Session management to maintain context between questions

## What I Learned
- [Specific finding — not generic]
- [The thing that surprised me]
- [The assumption that broke]
- [The detail worth remembering]

## How to Run
´´´
uv init 
source .venv/bin/activate
uv sync 
uv run -m pipeline.ingestion
´´´


## Tech Used
- Lightweight but effective text embeddings using paraphrase-MiniLM-L6-v2
- [Library or tool and why it was chosen]

## Known Issues / Setup Notes
### RAGAS + OpenAI v2 compatibility fix 
RAGAS 0.4.x has a broken import from langchain_community.chat_models.vertexai. If RAGAS import fails with ModuleNotFoundError: No module named 'langchain_community.chat_models.vertexai' after installing, manually comment out two lines in .venv/lib/python3.12/site-packages/ragas/llms/base.py:
Line 12: from langchain_community.chat_models.vertexai import ChatVertexAI
Line 43: ChatVertexAI,

### Use llm_factory not LangchainLLMWrapper — per RAGAS deprecation warning

## References
- [Inspo](https://medium.com/@perfectsolution808/wikipedia-based-q-a-chatbot-a-beginners-approach-using-free-tools-5067d501a6ab)
- [Wikipedia](https://www.wikipedia.org/)
- [groq docs](https://console.groq.com/docs/responses-api)
- [build a request URL](https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls)
- [handling url sections](https://docs.python.org/3/library/urllib.parse.html)
- [regex (regular expression) in Python](https://www.w3schools.com/python/python_regex.asp), [findall vs. finditer](https://www.tutorialspoint.com/article/what-is-the-difference-between-re-findall-and-re-finditer-methods-available-in-python)

- [RAGAS TestsetGenerator](https://docs.ragas.io/en/stable/getstarted/rag_testset_generation/#a-deeper-look)
- [Langchain Document Object](https://reference.langchain.com/python/langchain-core/documents/base/Document)
- LangChain's [ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai) & [OpenAIEmbeddings](https://reference.langchain.com/python/langchain-openai/embeddings/base/OpenAIEmbeddings) (RAGAS speaks LangChain internally)
- [RAGAS 0.2.x mix of question types (default_query_distribution). Consisting of all three made to a default SingleHopSpecific/MultiHopAbstract/MultiHopSpecific - QuerySynthesizer](https://docs.ragas.io/en/stable/references/generate/)

- [llamaindex: from_documents, generate_dataset_from_nodes](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/dataset_generation/)

- [Vector Embeddings Openai](https://developers.openai.com/api/docs/guides/embeddings)

- [Chromadb create client & collection](https://docs.trychroma.com/docs/overview/getting-started)

- [RAGAS Evaluation Dataset](https://docs.ragas.io/en/stable/concepts/components/eval_dataset/)
- [RAGAS Customise models](https://docs.ragas.io/en/stable/howtos/customizations/customize_models/)
- [RAGAS evaluate ()](https://docs.ragas.io/en/v0.2.8/references/evaluate/#ragas.evaluation.evaluate)
- [RAGAS avaliable metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)


- [Hybrid search: BM25Okapi algorithm](https://pypi.org/project/rank-bm25/)
- [Reranking: Cross-Encoders](https://sbert.net/examples/cross_encoder/applications/README.html)
- [Reranking: Cross-encoder model from HF (compare to embedding model, bi-coder. Thi is a cross-encoder,reranker.)](https://huggingface.co/BAAI/bge-reranker-base)