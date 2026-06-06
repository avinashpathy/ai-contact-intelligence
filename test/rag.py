import os

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = "contacts-index"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 512
CHAT_MODEL = "gpt-4.1-mini"
TOP_K = 5

query = "Find frontend developers"

openai_client = OpenAI()
pinecone_client = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY") or os.getenv("PINECON_API_KEY")
)
index = pinecone_client.Index(INDEX_NAME)


def embed_text(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return response.data[0].embedding


def retrieve_top_contacts(user_query: str, top_k: int = TOP_K) -> list[dict]:
    query_embedding = embed_text(user_query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )
    return results["matches"]


def build_context(matches: list[dict]) -> str:
    lines = []
    for i, match in enumerate(matches, start=1):
        name = match["metadata"]["name"]
        description = match["metadata"]["description"]
        score = match["score"]
        lines.append(f"{i}. {name} (similarity: {score:.4f})\n   {description}")
    return "\n\n".join(lines)


def create_prompt(user_query: str, context: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": (
                "You are a contact search assistant. "
                "Answer only using the provided contacts. "
                "If the contacts do not contain enough information, say so. "
                "Do not invent names or skills."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Contacts:\n{context}\n\n"
                f"Question: {user_query}"
            ),
        },
    ]


def call_gpt(messages: list[dict]) -> str:
    response = openai_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    matches = retrieve_top_contacts(query)
    context = build_context(matches)
    messages = create_prompt(query, context)
    answer = call_gpt(messages)

    print(answer)
