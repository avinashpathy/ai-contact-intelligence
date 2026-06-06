from pinecone import Pinecone, ServerlessSpec

from ..config import settings

pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

EMBEDDING_DIMENSIONS = 1536

_index = None


def ensure_index_exists():
    if not settings.PINECONE_INDEX_NAME:
        raise ValueError("PINECONE_INDEX_NAME is not set")

    index_names = pc.list_indexes().names()

    if settings.PINECONE_INDEX_NAME not in index_names:
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSIONS,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )


def get_index():
    global _index

    if _index is None:
        ensure_index_exists()
        _index = pc.Index(
            settings.PINECONE_INDEX_NAME
        )

    return _index


class PineconeIndexProxy:
    def __getattr__(self, name):
        return getattr(
            get_index(),
            name,
        )


index = PineconeIndexProxy()


def semantic_search(
    query_embedding,
    filters=None,
    top_k=20
):

    results = get_index().query(
        vector=query_embedding,
        top_k=top_k,
        filter=filters,
        include_metadata=True
    )

    return results["matches"]


def upsert_contact(
    contact_id,
    embedding,
    metadata
):

    get_index().upsert(
        vectors=[
            {
                "id": contact_id,
                "values": embedding,
                "metadata": metadata
            }
        ]
    )
