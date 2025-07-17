# embed_documents.py

import os
import hashlib
from sentence_transformers import SentenceTransformer
import chromadb


client = chromadb.PersistentClient(path="vector_store")
collection = client.get_or_create_collection(name="mental_health_docs")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Document source directory
DOC_DIR = "doc"

def chunk_text(text, max_length=300):
    """Splits long text into smaller chunks"""
    import textwrap
    return textwrap.wrap(text, width=max_length)

def generate_chunk_id(text):
    return hashlib.md5(text.encode()).hexdigest()

def embed_documents():
    for filename in os.listdir(DOC_DIR):
        if not filename.endswith((".txt", ".md")):
            continue

        path = os.path.join(DOC_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            chunk_id = generate_chunk_id(chunk)

            # Avoid duplicate embeddings
            try:
                existing = collection.get(ids=[chunk_id])
                if chunk_id in existing["ids"]:
                    continue  # already stored
            except:
                pass

            embedding = model.encode(chunk).tolist()
            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": filename}]
            )
            print(f"✅ Embedded: {filename} [chunk {i}]")

if __name__ == "__main__":
    embed_documents()
    print("✅ All documents embedded successfully.")
