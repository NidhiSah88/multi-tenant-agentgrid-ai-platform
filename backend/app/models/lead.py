
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Lead(Base):
    __tablename__ = "leads"

    lead_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    tenant_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    customer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    contact_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending_approval",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("idx_leads_tenant_status", "tenant_id", "status"),
    )








