
from sqlalchemy.orm import Session

from app.models.code_chunk import CodeChunk
from app.services.embedding_service import BedrockEmbeddingService


def semantic_code_search(
    db: Session,
    repository_id: str,
    tenant_id: str,
    query: str,
    top_k: int = 5,
):
    embedding_service = BedrockEmbeddingService()
    query_embedding = embedding_service.embed_text(query)

    distance = CodeChunk.embedding.cosine_distance(query_embedding)

    records = (
        db.query(CodeChunk, distance.label("distance"))
        .filter(
            CodeChunk.repository_id == repository_id,
            CodeChunk.tenant_id == tenant_id,
            CodeChunk.embedding.isnot(None),
        )
        .order_by(distance.asc())
        .limit(top_k)
        .all()
    )

    results = []

    for chunk, cosine_distance in records:
        results.append({
            "file_path": chunk.file_path,
            "language": chunk.language,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content": chunk.content,
            "similarity_score": round(
                1 - float(cosine_distance), 4
            ),
        })

    return results


