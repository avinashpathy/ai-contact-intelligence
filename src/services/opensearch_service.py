from opensearchpy import (
    OpenSearch
)
from urllib.parse import urlparse

from ..config import settings


def build_host_config():
    if not settings.OPENSEARCH_HOST:
        raise ValueError("OPENSEARCH_HOST is not set")

    parsed = urlparse(settings.OPENSEARCH_HOST)

    if parsed.scheme:
        return {
            "host": parsed.hostname,
            "port": parsed.port or 443,
            "scheme": parsed.scheme,
        }

    return {
        "host": settings.OPENSEARCH_HOST,
        "port": 443,
        "scheme": "https",
    }


client = OpenSearch(
    hosts=[
        build_host_config()
    ],
    http_auth=(
        settings.OPENSEARCH_USERNAME,
        settings.OPENSEARCH_PASSWORD
    ),
    use_ssl=True,
    verify_certs=True
)


INDEX_NAME = "contacts"


def keyword_search(
    query,
    size=20
):

    body = {
        "size": size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "name",
                    "title",
                    "skills"
                ]
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body=body
    )

    return response["hits"]["hits"]
