
from datetime import datetime
from pydantic import BaseModel, Field


class RepositoryAnalysis(BaseModel):
    total_files: int = 0
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)


class RepositoryUploadResponse(BaseModel):
    repository_id: str
    tenant_id: str
    repository_name: str
    original_filename: str
    status: str
    analysis: RepositoryAnalysis
    created_at: datetime







