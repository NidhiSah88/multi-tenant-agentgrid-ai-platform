
import json
import os

import boto3


class BedrockEmbeddingService:

    def __init__(self):
        self.region = os.getenv("AWS_REGION", "ap-south-1")
        self.model_id = os.getenv(
            "BEDROCK_EMBEDDING_MODEL_ID",
            "amazon.titan-embed-text-v2:0",
        )
        self.dimensions = 1024

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.region,
        )

    def embed_text(self, text: str) -> list[float]:
        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "inputText": text,
                "dimensions": self.dimensions,
                "normalize": True,
            }),
        )

        response_body = json.loads(
            response["body"].read()
        )

        embedding = response_body["embedding"]

        if len(embedding) != self.dimensions:
            raise ValueError(
                f"Expected {self.dimensions} dimensions, "
                f"received {len(embedding)}"
            )

        return embedding

    


