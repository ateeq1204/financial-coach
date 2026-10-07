import os
from dotenv import load_dotenv

load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY=os.environ.get("OPENROUTER_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"

# Replace this with the OpenAI model you have chosen for your project.
LLM_MODEL = "openrouter/free"

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "financial_documents"

DOCUMENTS_PATH = "./documents"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K = 5