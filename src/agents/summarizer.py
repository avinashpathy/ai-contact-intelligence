from ..services.llm_service import generate_completion


def summarizer_agent(
    state
):

    query = state["query"]

    contacts = (
        state["contacts"]
    )

    prompt = f"""
    You are a recruiting
    assistant.

    Contacts:

    {contacts}

    User Query:

    {query}

    Answer only using
    retrieved contacts.

    If no contacts exist,
    say so.
    """

    response = (
        generate_completion(
            prompt
        )
    )

    return {
        **state,
        "response":
        response
    }