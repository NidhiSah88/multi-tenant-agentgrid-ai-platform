import boto3

from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings


class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION,
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 500,
                    "temperature": 0.3,
                },
            )

            return response["output"]["message"]["content"][0]["text"]

        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(
                f"Bedrock request failed: {str(exc)}"
            ) from exc


bedrock_service = BedrockService()








