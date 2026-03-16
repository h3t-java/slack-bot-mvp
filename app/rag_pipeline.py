from app.embeddings import embed
from app.vector_store import search
from app.llm_client import ask_llm


def run_rag(query, context=""):

    query_embedding = embed(query)

    docs, scores, metadatas = search(query_embedding)

    print("Vector scores:", scores)

    # No results
    if not docs:
        return ask_llm(query)

    # similarity threshold
    if scores[0] > 0.8:
        # Not relevant → normal LLM answer
        return ask_llm(query)

    context_parts = []

    for doc, meta in zip(docs, metadatas):

        source = "unknown"
        if meta and "source" in meta:
            source = meta["source"]

        context_parts.append(f"Source: {source}\n{doc}")

    doc_text = "\n\n".join(context_parts)

    prompt = f"""
You are a helpful assistant.

Use the provided documents if they are relevant.

Documents:
{doc_text}

Question:
{query}

Answer:
"""

    answer = ask_llm(prompt)

    # Collect unique sources
    sources = {
        meta["source"]
        for meta in metadatas
        if meta and "source" in meta
    }

    source_text = "\n\nSources:\n" + "\n".join(sources)

    return answer + source_text
