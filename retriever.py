from embeddings import create_embedding
from vector_store import get_collection


def search_documents(
    question,
    number_of_results=5
):
    """
    Search ChromaDB for chunks semantically
    related to the question.
    """

    collection = get_collection()

    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=number_of_results
    )

    return results