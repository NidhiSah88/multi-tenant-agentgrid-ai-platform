from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AgentGrid API"
    APP_ENV: str = "development"
    API_VERSION: str = "v1"

    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "amazon.nova-lite-v1:0"

    DATABASE_URL: str = (
        "postgresql+psycopg://agentgrid:agentgrid@localhost:5432/agentgrid"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()





