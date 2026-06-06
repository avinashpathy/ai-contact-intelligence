from pydantic import BaseModel


class SearchRequest(BaseModel):

    query: str


class SearchResponse(BaseModel):

    response: str

    contacts: list


class ContactResponse(BaseModel):

    contactId: str

    name: str

    title: str

    location: str

    skills: list[str]