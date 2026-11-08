
import os
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.code_chunk import CodeChunk
from app.legacy_discovery.ingestion.code_chunker import parse_repository
from app.services.embedding_service import BedrockEmbeddingService


def resolve_repository_path(storage_path: str) -> Path:
    """
    Resolve the extracted source directory.

    Supports storage_path pointing to:
    - The repository storage directory
    - The extracted directory
    - The uploaded ZIP file
    """

    path = Path(storage_path).resolve()

    if path.is_file():
        path = path.parent / "extracted"

    elif (path / "extracted").is_dir():
        path = path / "extracted"

    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(
            f"Extracted repository directory not found: {path}"
        )

    return path


def index_repository(
    db: Session,
    repository: Repository,
):
    repository_path = resolve_repository_path(
        repository.storage_path
    )

    chunks = parse_repository(repository_path)

    if not chunks:
        raise ValueError(
            "No supported source-code files were found."
        )

    # Remove the previous index so re-indexing does not duplicate chunks.
    db.query(CodeChunk).filter(
        CodeChunk.repository_id == repository.repository_id,
        CodeChunk.tenant_id == repository.tenant_id,
    ).delete(synchronize_session=False)

    embeddings_enabled = (
        os.getenv("BEDROCK_EMBEDDINGS_ENABLED", "false").lower()
        == "true"
    )

    embedding_service = (
        BedrockEmbeddingService()
        if embeddings_enabled
        else None
    )

    embedded_count = 0
    pending_count = 0

    try:
        for chunk in chunks:
            embedding = None

            if embedding_service:
                try:
                    embedding = embedding_service.embed_text(
                        chunk["content"]
                    )
                    embedded_count += 1
                except Exception:
                    # Preserve the chunk even if Bedrock is unavailable.
                    pending_count += 1
            else:
                pending_count += 1

            db.add(
                CodeChunk(
                    repository_id=repository.repository_id,
                    tenant_id=repository.tenant_id,
                    file_path=chunk["file_path"],
                    language=chunk["language"],
                    chunk_index=chunk["chunk_index"],
                    start_line=chunk["start_line"],
                    end_line=chunk["end_line"],
                    content=chunk["content"],
                    embedding=embedding,
                    metadata_json={
                        "source": "repository_ingestion",
                    },
                )
            )

        repository.status = (
            "indexed"
            if pending_count == 0
            else "chunks_created"
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "repository_id": repository.repository_id,
        "total_chunks": len(chunks),
        "embedded_chunks": embedded_count,
        "pending_embeddings": pending_count,
        "embedding_provider": (
            "amazon-bedrock-titan-v2"
            if embedding_service
            else None
        ),
        "status": repository.status,
    }


# This service supports re-indexing, avoids duplicate chunks, and retains code even when Bedrock is not yet available.



