from .llm_service import generate_completion


def rerank_results(
    query,
    contacts
):

    prompt = f"""
    Query:

    {query}

    Contacts:

    {contacts}

    Rank contacts
    from most relevant
    to least relevant.

    Return contactIds
    in ranked order.
    """

    result = generate_completion(
        prompt
    )

    ranked_ids = (
        result
        .replace("\n", "")
        .split(",")
    )

    return ranked_ids