from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    PINECONE_API_KEY = os.getenv(
        "PINECONE_API_KEY"
    )

    PINECONE_INDEX_NAME = os.getenv(
        "PINECONE_INDEX_NAME"
    )

    AWS_REGION = os.getenv(
        "AWS_REGION"
    )

    DYNAMODB_TABLE_NAME = os.getenv(
        "DYNAMODB_TABLE_NAME"
    )

    OPENSEARCH_HOST = os.getenv(
        "OPENSEARCH_HOST"
    )

    OPENSEARCH_USERNAME = os.getenv(
        "OPENSEARCH_USERNAME"
    )

    OPENSEARCH_PASSWORD = os.getenv(
        "OPENSEARCH_PASSWORD"
    )

    REDIS_HOST = os.getenv(
        "REDIS_HOST"
    )

    REDIS_PORT = int(
        os.getenv(
            "REDIS_PORT",
            6379
        )
    )


settings = Settings()