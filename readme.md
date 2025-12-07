
# development setup
uv venv .venv
uv pip install -e backend/services/ingestion-service
source .venv/bin/activate
uv pip install -e backend/services/ingestion-service
uv pip install -e backend/services/shared-service
uv pip install -e backend/services/chat-service

# python interpretor
In Cursor:
Cmd + Shift + P
Search → Python: Select Interpreter
Choose: ./your-repo/.venv/bin/python

backend/
├─ ingestion-service/
│  ├─ src/ingestion-service/
│  │  ├─ api/                 # Expose ingestion-related APIs
│  │  │  ├─ routes/
│  │  │  │  ├─ ingestion_routes.py
│  │  │  │  └─ healthcheck.py
│  │  │  └─ main.py           # FastAPI/Flask app entry point
│  │  ├─ services/            # Business logic for ingestion
│  │  │  ├─ ingestion_service.py
│  │  │  └─ vector_service.py
│  │  ├─ chunker/
│  │  ├─ content_loader/
│  │  ├─ embedder/
│  │  ├─ vector_store/
│  │  ├─ config/              # Settings, environment loader
│  │  │  └─ settings.py
│  │  ├─ utils/               # Helpers, logging, file operations
│  │  │  └─ logger.py
│  │  └─ schemas/             # Request/response validation
│  │     ├─ request.py
│  │     └─ response.py
│  ├─ tests/
│  │  ├─ unit/
│  │  │  └─ test_chunker.py
│  │  └─ integration/
│  │     └─ test_ingestion_api.py
│  ├─ .env
│  ├─ pyproject.toml
│  ├─ main.py                 # Optional CLI entry
│  └─ uv.lock
│
├─ chat-service/
│  ├─ src/
│  │  ├─ api/                 # Expose retrieval-related APIs
│  │  │  ├─ routes/
│  │  │  │  ├─ retrieval_routes.py
│  │  │  │  ├─ user_routes.py
│  │  │  │  └─ healthcheck.py
│  │  │  └─ main.py           # FastAPI/Flask app entry point
│  │  ├─ services/            # Business logic for retrieval
│  │  │  ├─ retrieval_service.py
│  │  │  └─ rag_orchestrator.py  # Handles query + retrieval + LLM calls
│  │  ├─ vector_store/        # Access the same or replicated vector store
│  │  ├─ graph/        # Access the same or replicated vector store
│  │  ├─ config/
│  │  │  └─ settings.py
│  │  ├─ utils/
│  │  │  └─ logger.py
│  │  └─ schemas/
│  │     ├─ request.py
│  │     └─ response.py
│  ├─ tests/
│  │  ├─ unit/
│  │  └─ integration/
│  ├─ .env
│  ├─ pyproject.toml
│  ├─ main.py
│  └─ uv.lock
│
└─ shared-libs/               # Optional shared utilities
   ├─ utils/
   ├─ models/                 # Common Pydantic models or embeddings
   └─ logging/



### Phase 1
------------
   backend/
      services/
         ingestion-service/
         chat-service/
         shared/
            embeddings.py
            config.py
            logging.py

   vector-db: Chroma or Qdrant (local or docker)
   storage: local filesystem
   db: SQLite

### Phase 2
-------------
  - RBAC (roles & permissions)
  - separate auth-service/
  - Redis (caching)
  - Message queue (Redis Streams or RabbitMQ)
  - Background workers
  - S3 / GCS / Minio for file storage
  - Postgres

### phase 3
-------------
  - Multi-tenancy
  - Observability (Prometheus + Grafana)
  - Tracing (OpenTelemetry)
  - CI/CD
  - Feature flags
  - Canary deployments



