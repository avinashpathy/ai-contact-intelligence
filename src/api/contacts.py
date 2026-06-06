from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/contacts/count"
)
async def count_contacts():

    return {
        "count": 0
    }


@router.get(
    "/contacts/{contact_id}"
)
async def get_contact(
    contact_id: str
):

    return {
        "contactId":
        contact_id
    }