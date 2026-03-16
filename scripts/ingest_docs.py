import sys
import os

# Disable Chroma telemetry BEFORE importing anything from chromadb
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Ensure project root is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.embeddings import embed
from app.vector_store import add_document, collection

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
    """Read documents, chunk them, embed them, and store them in Chroma."""
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
            add_document(chunk, embedding, metadata)  # uses ids=[uuid] inside vector_store

    print("Ingestion completed")
    print("Total documents:", collection.count())


if __name__ == "__main__":
    ingest_documents()
