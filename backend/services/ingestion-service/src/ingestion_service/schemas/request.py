from typing import List
from pydantic import BaseModel

class IngestRequest(BaseModel):
    urls: List[str]          # comma-separated URLs
    collection_name: str