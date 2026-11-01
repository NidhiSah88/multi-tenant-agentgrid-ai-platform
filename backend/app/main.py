from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="AgentGrid - AI-powered customer engagement platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix=f"/api/{settings.API_VERSION}",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AgentGrid",
        "status": "running",
    }


