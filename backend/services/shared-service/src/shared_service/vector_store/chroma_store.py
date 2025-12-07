import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from pathlib import Path

from shared_service.config.settings import settings
from shared_service.embedder.hugging_face_embedding import HuggingFaceEmbedding

class ChromaStore:

    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        print(f"ChromaStore: { settings.DB_PATH }")
        self.embedder = HuggingFaceEmbedding()
        persist_dir = Path( settings.DB_PATH )
        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=persist_dir
        )

    def get_collection(self, name: str):
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, collection_name: str, documents: list[Document]):
        collection = self.get_collection(collection_name)

        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]
        ids = [chunk.metadata["chunk_id"] for chunk in documents]

        # Generate embeddings manually
        embeddings = self.embedder.embed_documents(texts)

        # Insert into Chroma
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, collection_name: str, query: str, k: int = 5):
        collection = self.get_collection(collection_name)

        query_embedding = self.embedder.embed(query)

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

    def delete_collection(self, name: str):
        # Permanently delete the entire collection
        self.client.delete_collection(name=name)
    
    def delete_by_source(self, collection_name: str, source_id: str):
        collection = self.get_collection(collection_name)
        collection.delete(where={"source_uri": source_id})