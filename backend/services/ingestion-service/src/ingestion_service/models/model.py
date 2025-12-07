from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import hashlib

Base = declarative_base()

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class DocumentRecord(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True)         
    source_uri = Column(String, nullable=False)           
    fingerprint = Column(String, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=True, default="active")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    chunks = relationship("ChunkRecord", back_populates="document")


class ChunkRecord(Base):
    __tablename__ = "chunks"

    chunk_id = Column(String, primary_key=True)             # stable ID for chunk
    document_id = Column(String, ForeignKey("documents.document_id"))
    chunk_index = Column(Integer, nullable=False)
    fingerprint = Column(String, nullable=True)            # hash of chunk
    text = Column(Text, nullable=False)

    document = relationship("DocumentRecord", back_populates="chunks")

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="u_document_chunk"),
    )
