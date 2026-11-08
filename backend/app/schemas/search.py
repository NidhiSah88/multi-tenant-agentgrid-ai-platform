from pydantic import BaseModel, Field


class CodeSearchRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    query: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


class CodeSearchResult(BaseModel):
    file_path: str
    language: str
    start_line: int
    end_line: int
    content: str
    similarity_score: float


class CodeSearchResponse(BaseModel):
    repository_id: str
    query: str
    total_results: int
    results: list[CodeSearchResult]

    