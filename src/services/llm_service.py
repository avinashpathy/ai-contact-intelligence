from openai import OpenAI

from ..config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_completion(
    prompt: str
):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return (
        response
        .choices[0]
        .message
        .content
    )