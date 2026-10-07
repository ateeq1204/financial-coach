import os
from openai import OpenAI
from config import OPENROUTER_API_KEY, EMBEDDING_MODEL


client = OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

def create_embedding(text):
    """
    Convert text into an embedding vector.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding