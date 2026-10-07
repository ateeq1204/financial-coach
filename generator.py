from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    LLM_MODEL,
    TOP_K
)

from retriever import search_documents


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def generate_answer(question):

    results = search_documents(
        question,
        number_of_results=TOP_K
    )

    documents = results.get("documents", [[]])[0]

    metadatas = results.get("metadatas", [[]])[0]

    if not documents:

        return {
            "answer": (
                "I could not find relevant information "
                "in the uploaded financial documents."
            ),
            "sources": [],
            "context": []
        }

    context_parts = []

    for index, document in enumerate(documents):

        source = metadatas[index]["source"]

        context_parts.append(
            f"""
SOURCE: {source}

{document}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI Financial Coach.

Your job is to answer the user's question using
ONLY the financial information provided in the
retrieved document context.

RETRIEVED DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

RULES:

1. Use only the retrieved document context.
2. Do not invent financial information.
3. If the information is not available in the context,
   clearly say that you could not find it.
4. Use exact financial numbers when available.
5. Explain calculations clearly.
6. Keep the answer easy to understand.
7. Mention which document(s) support your answer.
8. Do not provide unsupported financial claims.
"""

    response = client.responses.create(
        model=LLM_MODEL,
        input=prompt
    )

    answer = response.output_text

    sources = []

    for metadata in metadatas:

        source = metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
        "context": documents
    }