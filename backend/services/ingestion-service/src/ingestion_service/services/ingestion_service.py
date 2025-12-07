from sqlalchemy.sql.functions import now
from ingestion_service.core.content_loader import WebLoader
from ingestion_service.core.chunker.SemanticChunker import SemanticChunker
#from ingestion_service.core.vector_store.chroma_store import ChromaStore
from shared_service.vector_store.chroma_store import ChromaStore
from ingestion_service.models.model import DocumentRecord, ChunkRecord
from typing import List, Literal
from langchain_core.documents import Document
import uuid

class IngestionService:
    def __init__(self, db):
        self.web_loader = WebLoader()
        self.chroma_store = ChromaStore()
        self.semantic_chunker = SemanticChunker()
        #self.recursive_chunker = RecursiveChunker()
        self.db = db;
        

    def ingest_web_content(self, 
        urls: List[str], 
        collection_name: str, 
        chunker_type : Literal['semantic', 'recursive'] = "semantic" )-> list[dict]:

        
        all_response = []
        for url in urls:
            docs = self.web_loader.load_doc(url = url)
            response = self._process_text(url, collection_name, docs)
            all_response.append(response)

        return all_response
        
    def ingest_pdf_content(self):
        """ will be implemented later """
        return 0
    
    def _process_text(self, source_uri: str, collection_name: str, docs: List[Document])->dict:
        document_id = str(uuid.uuid4()) # new docuemnt id
        chunks = self.semantic_chunker.chunk(docs)

        existing_docs = (
            self.db.query(DocumentRecord)
            .filter(DocumentRecord.source_uri == source_uri)
            .all()
        )
        print("existing document::: ")
        print(existing_docs)

        # cleanup the existing records
        if existing_docs:
            self.chroma_store.delete_by_source(collection_name, source_id=source_uri)
            for doc in existing_docs:
                self.db.query(ChunkRecord).filter_by(document_id=doc.document_id).delete()
                self.db.delete(doc)
                self.db.commit()

        # process for insert the document
        doc_record = DocumentRecord(
            document_id=document_id,
            source_uri=source_uri,
            fingerprint="",
            version=1
        )
        self.db.add(doc_record)
        self.db.commit()

        # insert chunks  in db
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{document_id}-{idx}"
            chunk_record = ChunkRecord(
                chunk_id=chunk_id,
                document_id=document_id,
                chunk_index=idx,
                text=chunk.page_content
            )
            self.db.add(chunk_record)
            chunk.metadata["chunk_id"] = chunk_id  # store for vector DB
        
        self.db.commit()

        # store all chunks in chroma
        self.chroma_store.add_documents(collection_name, chunks)
        return {
            "chunks_stored": len(chunks),
            "document_id": document_id
        }