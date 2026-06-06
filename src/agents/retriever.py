from ..repositories.contact_repository import ContactRepository
from ..services.redis_service import get_cache, set_cache
from ..services.rerank_service import rerank_results


COUNTRY_LOCATIONS = {
    "india",
    "in",
    "indian",
}


def should_apply_location_filter(location):
    if not location:
        return False

    return location.strip().lower() not in COUNTRY_LOCATIONS


def contact_from_pinecone_match(match):
    metadata = match.get("metadata") or {}

    return {
        "contactId": match.get("id"),
        "name": metadata.get("name"),
        "title": metadata.get("title"),
        "location": metadata.get("location"),
        "skills": metadata.get("skills", []),
    }


def retriever_agent(
    state
):

    query = state["query"]

    cache_key = (
        f"search:{query}"
    )

    cached = get_cache(
        cache_key
    )

    if cached:

        return {
            **state,
            "contacts":
            cached
        }

    filters = {}

    planner_filters = (
        state["filters"]
    )

    location = (
        planner_filters
        .get("location")
    )

    if should_apply_location_filter(location):

        filters["location"] = {
            "$eq":
            location
        }

    results = (
        ContactRepository
        .hybrid_search(
            query,
            filters
        )
    )

    pinecone_results = (
        results["pinecone"]
    )

    pinecone_contacts_by_id = {
        result["id"]: contact_from_pinecone_match(result)
        for result
        in pinecone_results
    }

    contact_ids = [
        result["id"]
        for result
        in pinecone_results
    ]

    ranked_ids = (
        rerank_results(
            query,
            contact_ids
        )
    )

    ranked_ids = [
        contact_id
        for contact_id
        in ranked_ids
        if contact_id in pinecone_contacts_by_id
    ] or contact_ids

    contacts = (
        ContactRepository
        .get_contacts_by_ids(
            ranked_ids[:5]
        )
    )

    if not contacts:
        contacts = [
            pinecone_contacts_by_id[contact_id]
            for contact_id
            in ranked_ids[:5]
            if contact_id in pinecone_contacts_by_id
        ]

    set_cache(
        cache_key,
        contacts
    )

    return {
        **state,
        "contacts":
        contacts
    }
