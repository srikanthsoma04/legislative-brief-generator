import chromadb
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(collection_name: str = "legislative_votes"):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

def embed_documents(docs: List[str], ids: List[str], collection_name: str = "legislative_votes"):
    collection = get_or_create_collection(collection_name)
    existing = collection.get()["ids"]
    new_docs = [(doc, id_) for doc, id_ in zip(docs, ids) if id_ not in existing]
    if not new_docs:
        print("All documents already embedded.")
        return
    texts, new_ids = zip(*new_docs)
    collection.add(documents=list(texts), ids=list(new_ids))
    print(f"Embedded {len(new_ids)} new documents into ChromaDB.")

def embed_legislator(legislator: dict):
    from src.data_loader import format_votes_for_embedding
    docs = format_votes_for_embedding(legislator)
    ids = [f"{legislator['id']}-{i}" for i in range(len(docs))]
    embed_documents(docs, ids)