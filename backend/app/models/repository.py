
import uuid

from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Repository(Base):

    __tablename__ = "repositories"

    repository_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    tenant_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    repository_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="uploaded",
    )

    total_files: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    languages: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    frameworks: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    file_inventory: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )











