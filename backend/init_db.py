
# from app.database.connection import Base, engine
# from app.models import Lead

# print("Creating AgentGrid database tables...")

# Base.metadata.create_all(bind=engine)

# print("Database tables created successfully!")




from sqlalchemy import text

from app.database.connection import Base, engine
from app.models import Lead, Repository, CodeChunk


def init_db():
    print("Enabling pgvector extension...")

    # with engine.begin() as connection:
    #     connection.execute(
    #         text("CREATE EXTENSION IF NOT EXISTS vector")
    #     )

    # Add a vector similarity index

    with engine.begin() as connection:
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_code_chunks_embedding_hnsw
            ON code_chunks
            USING hnsw (embedding vector_cosine_ops)
        """))

    

    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()











