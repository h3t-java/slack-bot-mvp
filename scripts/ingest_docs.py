import sys
import os
import uuid

# Disable Chroma telemetry BEFORE importing anything from chromadb
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Ensure project root is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.embeddings import embed
from app.vector_store import client, COLLECTION_NAME, add_document

DOC_FOLDER = "data/documents"


def split_text(text, chunk_size=400, overlap=80):
    """Split text into overlapping word chunks."""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap  # move window with overlap

    return chunks


def ingest_documents():
    # Drop old collection if exists
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        print("Dropping existing collection...")
        client.delete_collection(COLLECTION_NAME)

    # Recreate collection and get the new object
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"Collection '{COLLECTION_NAME}' ready for ingestion.")

    for file in os.listdir(DOC_FOLDER):
        path = os.path.join(DOC_FOLDER, file)

        if not os.path.isfile(path):
            continue

        print("Processing:", file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            embedding = embed(chunk)
            metadata = {
                "source": file,
                "chunk": i
            }
           # Add directly using the current collection object
            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[metadata]
            )

    print("Ingestion completed")
    print("Total documents:", collection.count())


if __name__ == "__main__":
    ingest_documents()
