from typing import TypedDict


class ContactState(
    TypedDict
):

    query: str

    intent: str

    filters: dict

    contacts: list

    response: str