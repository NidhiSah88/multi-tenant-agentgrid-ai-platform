
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    Index,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database.connection import Base


class CodeChunk(Base):
    __tablename__ = "code_chunks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    repository_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("repositories.repository_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tenant_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    end_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1024),
        nullable=True,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "idx_code_chunks_repository_file",
            "repository_id",
            "file_path",
        ),
        Index(
            "idx_code_chunks_tenant_repository",
            "tenant_id",
            "repository_id",
        ),
    )





