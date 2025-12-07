


from fastapi import FastAPI
from contextlib import asynccontextmanager
from ingestion_service.api import ingestion_routes
from ingestion_service.services.ingestion_service import IngestionService
from ingestion_service.config.db import init_db
# from ingestion_service.api import retrieval_routes, admin_routes  # add later
import uvicorn
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(sys.executable)
    print("Starting application...")
    init_db()
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Enterprise RAG API",
    description="API for ingestion, retrieval, and admin tasks",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers with optional version prefix
app.include_router(ingestion_routes.router, prefix="/v1")
# app.include_router(retrieval_routes.router, prefix="/v1/retrieval")
# app.include_router(admin_routes.router, prefix="/v1/admin")