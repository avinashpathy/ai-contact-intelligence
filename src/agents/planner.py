import json

from ..services.llm_service import generate_completion


def planner_agent(state):

    query = state["query"]

    prompt = f"""
    You are a planner agent.

    Extract:

    intent
    location
    title
    skills

    Return ONLY JSON.

    Query:

    {query}
    """

    response = generate_completion(
        prompt
    )

    try:

        plan = json.loads(
            response
        )

    except Exception:

        plan = {
            "intent":
            "search_contacts",
            "location":
            None,
            "title":
            None,
            "skills":
            []
        }

    return {
        **state,
        "intent":
        plan["intent"],

        "filters":
        plan
    }