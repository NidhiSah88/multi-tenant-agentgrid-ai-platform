
from sqlalchemy.orm import Session

from app.models.code_chunk import CodeChunk
from app.services.embedding_service import BedrockEmbeddingService


def generate_missing_embeddings(
    db: Session,
    repository_id: str,
    tenant_id: str,
    batch_size: int = 50,
):
    service = BedrockEmbeddingService()

    chunks = (
        db.query(CodeChunk)
        .filter(
            CodeChunk.repository_id == repository_id,
            CodeChunk.tenant_id == tenant_id,
            CodeChunk.embedding.is_(None),
        )
        .order_by(CodeChunk.file_path, CodeChunk.chunk_index)
        .limit(batch_size)
        .all()
    )

    processed = 0

    try:
        for chunk in chunks:
            chunk.embedding = service.embed_text(chunk.content)
            processed += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    remaining = (
        db.query(CodeChunk)
        .filter(
            CodeChunk.repository_id == repository_id,
            CodeChunk.tenant_id == tenant_id,
            CodeChunk.embedding.is_(None),
        )
        .count()
    )

    return {
        "repository_id": repository_id,
        "processed": processed,
        "remaining": remaining,
        "status": "completed" if remaining == 0 else "in_progress",
    }


