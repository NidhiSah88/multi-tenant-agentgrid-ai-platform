

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.repository import Repository
from app.legacy_discovery.ingestion.indexing import index_repository

router = APIRouter()


@router.post("/{repository_id}/index")
def index_uploaded_repository(
    repository_id: str,
    tenant_id: str = Query(...),
    db: Session = Depends(get_db),
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

    try:
        result = index_repository(db, repository)
        return {
            "message": "Repository source-code indexing completed.",
            **result,
        }

    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Repository indexing failed: {str(exc)}",
        )

