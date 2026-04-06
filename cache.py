"""
cache.py — Semantic cache utilities using Pinecone vectorstore.
"""

import json
from config import VECTORSTORE, CACHE_DISTANCE


def get_cache(query: str):
    """
    Returns cached research_chunk list if a similar query was previously stored,
    otherwise returns None.
    """
    docs = VECTORSTORE.similarity_search_with_score(query, k=1)

    if not docs:
        return None

    doc, distance = docs[0]

    if distance < CACHE_DISTANCE:
        print("Distance too short:", distance)
        return None

    if "response" not in doc.metadata:
        print("No response in metadata:", doc.metadata)
        return None

    print("Distance :", distance)
    return json.loads(doc.metadata["response"])


def set_cache(query: str, value: dict | list):
    """
    Stores the research result in the vectorstore for future cache hits.
    """
    VECTORSTORE.add_texts(
        texts=[query],
        metadatas=[{"response": json.dumps(value)}],
    )
