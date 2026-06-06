from fastapi import APIRouter

from ..graph.workflow import workflow
from ..models.schemas import SearchRequest

router = APIRouter()


@router.post(
    "/search"
)
async def search_contacts(
    request: SearchRequest
):

    result = workflow.invoke(
        {
            "query":
            request.query,

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