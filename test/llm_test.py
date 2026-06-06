from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain AWS Lambda in one sentence"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)