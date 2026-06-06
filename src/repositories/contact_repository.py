from ..services.dynamo_service import (
    batch_get_contacts,
    count_contacts,
    get_contact,
)
from ..services.embedding_service import generate_embedding
from ..services.opensearch_service import keyword_search
from ..services.pinecone_service import semantic_search


class ContactRepository:

    @staticmethod
    def hybrid_search(query, filters=None):
        query_embedding = generate_embedding(query)

        pinecone_results = semantic_search(
            query_embedding,
            filters,
        )

        try:
            opensearch_results = keyword_search(query)
        except Exception:
            opensearch_results = []

        return {
            "pinecone": pinecone_results,
            "opensearch": opensearch_results,
        }

    @staticmethod
    def get_contacts_by_ids(contact_ids):
        try:
            return batch_get_contacts(contact_ids)
        except Exception:
            return []

    @staticmethod
    def get_contact_by_id(contact_id):
        return get_contact(contact_id)

    @staticmethod
    def count_contacts():
        return count_contacts()
