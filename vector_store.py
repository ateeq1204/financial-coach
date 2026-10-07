import chromadb

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    DOCUMENTS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from ingestion import load_documents
from chunking import chunk_text
from embeddings import create_embedding


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def get_collection():
    """
    Get or create the ChromaDB collection.
    """

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def reset_collection():
    """
    Delete the existing collection and create
    a fresh one.
    """

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        pass

    return client.create_collection(
        name=COLLECTION_NAME
    )


def ingest_documents():

    collection = reset_collection()

    documents = load_documents(DOCUMENTS_PATH)

    if not documents:
        return 0

    total_chunks = 0

    for document in documents:

        source = document["source"]

        chunks = chunk_text(
            document["text"],
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP
        )

        for index, chunk in enumerate(chunks):

            embedding = create_embedding(chunk)

            document_id = f"{source}-{index}"

            collection.add(
                ids=[document_id],

                documents=[chunk],

                embeddings=[embedding],

                metadatas=[
                    {
                        "source": source,
                        "chunk_index": index
                    }
                ]
            )

            total_chunks += 1

    return total_chunks