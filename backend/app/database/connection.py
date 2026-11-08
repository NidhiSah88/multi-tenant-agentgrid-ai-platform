

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# - engine: Establishes the database connection.
# - SessionLocal: Creates database sessions for queries and transactions.
# - Base: Parent class for your SQLAlchemy models.
# - get_db(): Provides a database session and closes it after use.

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI endpoints
# - get_db(): Provides a database session and closes it after use.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



