from .embedding_service import generate_embedding
from .pinecone_service import index


def search_contacts(query):

    query_embedding = generate_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    return results["matches"]