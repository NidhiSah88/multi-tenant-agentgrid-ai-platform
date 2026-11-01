
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.bedrock_service import bedrock_service

router = APIRouter()


class AIRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class AIResponse(BaseModel):
    response: str


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "agentgrid-api",
    }

# bedrock api 

@router.post("/ai/test", response_model=AIResponse)
async def test_bedrock(request: AIRequest):
    try:
        result = bedrock_service.generate_response(request.prompt)
        return AIResponse(response=result)

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


















