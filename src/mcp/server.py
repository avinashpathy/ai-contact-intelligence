from mcp.server.fastmcp import (
    FastMCP
)

from ..graph.workflow import workflow
from ..repositories.contact_repository import ContactRepository

mcp = FastMCP(
    "Contact Intelligence"
)


@mcp.tool()
def search_contacts(
    query: str
):

    result = workflow.invoke(
        {
            "query":
            query,

            "intent":
            "",

            "filters":
            {},

            "contacts":
            [],

            "response":
            ""
        }
    )

    return {
        "response":
        result["response"],

        "contacts":
        result["contacts"]
    }


@mcp.tool()
def get_contact(
    contact_id: str
):

    return (
        ContactRepository
        .get_contact_by_id(
            contact_id
        )
    )


@mcp.tool()
def count_contacts():

    return {
        "count":
        ContactRepository
        .count_contacts()
    }


@mcp.tool()
def match_candidates(
    job_description: str
):

    result = workflow.invoke(
        {
            "query":
            job_description,

            "intent":
            "",

            "filters":
            {},

            "contacts":
            [],

            "response":
            ""
        }
    )

    return result


if __name__ == "__main__":

    mcp.run()