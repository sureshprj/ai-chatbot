from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ingestion_service.models.model import Base
from pathlib import Path
from ingestion_service.config.settings import settings

print(settings.SQL_PATH)
# SQLite now — swap with Postgres later
DATABASE_URL = f"sqlite:///{settings.SQL_PATH}"

# For Postgres later:
# DATABASE_URL = "postgresql+psycopg2://user:pass@host/dbname"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite + FastAPI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("db init...")
    Base.metadata.create_all(bind=engine)
    print("db init completed.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
