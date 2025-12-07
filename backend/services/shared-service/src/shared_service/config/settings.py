import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    CHUNKER_MODEL: str = os.getenv("CHUNKER_MODEL")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
    DB_PATH: str = os.getenv("DB_PATH")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")
    SQL_PATH: str = os.getenv("SQL_PATH")
    
settings = Settings()
