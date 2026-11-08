from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.agent_routes import router as agent_router

from app.api.approval_routes import router as approval_router
from app.legacy_discovery.ingestion.upload import router as legacy_router

from app.api.routes import router
from app.core.config import settings

from app.legacy_discovery.ingestion.indexing_routes import (
    router as indexing_router,
)

from app.legacy_discovery.ingestion.retrieval_routes import (
    router as retrieval_router,
)




app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="AgentGrid - AI-powered customer engagement platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# General API routes
# endpoint here becomes: /api/v1/health
app.include_router(
    router,
    prefix=f"/api/{settings.API_VERSION}",
)

# AI Agent routes
# endpoint here becomes:  POST /api/v1/agents/chat
app.include_router(
    agent_router,
    prefix=f"/api/{settings.API_VERSION}/agents",
    tags=["AI Agents"],
)


app.include_router(
    approval_router,
    prefix=f"/api/{settings.API_VERSION}/approvals",
    tags=["Human Approval"],
)

# Legacy Application Discovery routes
app.include_router(
    legacy_router,
    prefix=f"/api/{settings.API_VERSION}/legacy",
    tags=["Legacy Application Discovery"],
)

app.include_router(
    indexing_router,
    prefix=f"/api/{settings.API_VERSION}/legacy",
    tags=["Legacy Source Code Intelligence"],
)


app.include_router(
    retrieval_router,
    prefix=f"/api/{settings.API_VERSION}/legacy",
    tags=["Semantic Code Intelligence"],
)




@app.get("/")
async def root():
    return {
        "message": "Welcome to AgentGrid",
        "status": "running",
    }


