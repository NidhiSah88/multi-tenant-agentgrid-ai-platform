
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.repository import Repository
from app.legacy_discovery.schemas.search import CodeSearchRequest
from app.legacy_discovery.ingestion.retrieval import semantic_code_search
from app.legacy_discovery.ingestion.embedding_jobs import (
    generate_missing_embeddings,
)

router = APIRouter()


def ensure_bedrock_enabled():
    enabled = (
        os.getenv("BEDROCK_EMBEDDINGS_ENABLED", "false").lower()
        == "true"
    )

    if not enabled:
        raise HTTPException(
            status_code=503,
            detail=(
                "Bedrock embeddings are disabled. Configure AWS "
                "credentials, enable the Titan Embeddings model, "
                "and set BEDROCK_EMBEDDINGS_ENABLED=true."
            ),
        )


def get_repository(
    db: Session,
    repository_id: str,
    tenant_id: str,
):
    repository = db.query(Repository).filter(
        Repository.repository_id == repository_id,
        Repository.tenant_id == tenant_id,
    ).first()

    if not repository:
        raise HTTPException(
            status_code=404,
            detail="Repository not found for this tenant.",
        )

    return repository


@router.post("/{repository_id}/embeddings")
def create_repository_embeddings(
    repository_id: str,
    tenant_id: str,
    batch_size: int = 50,
    db: Session = Depends(get_db),
):
    ensure_bedrock_enabled()

    if batch_size < 1 or batch_size > 100:
        raise HTTPException(
            status_code=400,
            detail="batch_size must be between 1 and 100.",
        )

    get_repository(db, repository_id, tenant_id)

    try:
        return generate_missing_embeddings(
            db=db,
            repository_id=repository_id,
            tenant_id=tenant_id,
            batch_size=batch_size,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Embedding generation failed: {str(exc)}",
        )


@router.post("/{repository_id}/search")
def search_repository_code(
    repository_id: str,
    request: CodeSearchRequest,
    db: Session = Depends(get_db),
):
    ensure_bedrock_enabled()

    get_repository(db, repository_id, request.tenant_id)

    try:
        results = semantic_code_search(
            db=db,
            repository_id=repository_id,
            tenant_id=request.tenant_id,
            query=request.query,
            top_k=request.top_k,
        )

        return {
            "repository_id": repository_id,
            "query": request.query,
            "total_results": len(results),
            "results": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Semantic code search failed: {str(exc)}",
        )

