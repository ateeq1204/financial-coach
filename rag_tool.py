import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY")
)


vector_store = Chroma(
    collection_name="financial_documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 4
    }
)

results = retriever.invoke(
    "What is my home loan EMI?"
)

for document in results:

    print("=" * 50)

    print(document.page_content)

    print(document.metadata)