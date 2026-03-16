# Force Python to use modern SQLite before anything else loads
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import uuid
from chromadb import Client
from chromadb.config import Settings

# Ensure the directory exists
os.makedirs("data/chroma_db", exist_ok=True)

# Name your collection
COLLECTION_NAME = "documents"

# Create Chroma client using the NEW API (0.5.x)
client = Client(
    Settings(
        is_persistent=True,
        persist_directory="data/chroma_db",
        anonymized_telemetry=False  # disables noisy telemetry warnings
    )
)

# Create or load collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # recommended for cosine similarity
)

def add_document(text, embedding,  metadata=None):
    """Add a single document chunk + embedding to Chroma."""
    doc_id = str(uuid.uuid4())  # REQUIRED in Chroma 0.5.x
    collection.add(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata or {}],
        embeddings=[embedding]
    )

def search(embedding, k=3):
    """Search for similar chunks."""
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k
    )

    docs = results["documents"][0]
    scores = results["distances"][0]
    metadatas = results["metadatas"][0]

    return docs, scores, metadatas
