from fastapi import APIRouter, HTTPException, Depends
from ingestion_service.schemas.response import IngestResponse
from ingestion_service.services.ingestion_service import IngestionService
from ingestion_service.schemas.request import IngestRequest
from ingestion_service.config.db import get_db
from sqlalchemy.orm import Session
from typing import List
from shared_service.test import Test

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

import inspect, os


# Define ingestion endpoints here
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    service = IngestionService(db)
    t = Test()
    t.display()
    return {"status": "ok"}

@router.post("/ingest-urls", response_model=list[IngestResponse])
def ingest_urls(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        print(request.urls)
        if not request.urls:
            raise HTTPException(status_code=400, detail="No URLs provided")
        # Call service layer
        service = IngestionService(db)
        response = service.ingest_web_content(request.urls, collection_name=request.collection_name)
        print(f"the document loaded: {len(response)}")
        all_responses = [
            IngestResponse(status="success", **resp)
            for resp in response
        ]
        return all_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
