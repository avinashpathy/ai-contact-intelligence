from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()

client = OpenAI()

query = "Find frontend developers"

contacts = [
    {
        "name": "John",
        "description": "Senior React Engineer with AWS experience"
    },
    {
        "name": "Jane",
        "description": "Backend Engineer skilled in Node.js and DynamoDB"
    },
    {
        "name": "Mike",
        "description": "UI Developer experienced in JavaScript and React"
    },
    {
        "name": "Sarah",
        "description": "Cloud Architect specializing in AWS infrastructure"
    }
]


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


query_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query,
)
query_embedding = query_response.data[0].embedding

descriptions = [contact["description"] for contact in contacts]
contact_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=descriptions,
)

results = []
for contact, item in zip(contacts, contact_response.data):
    similarity = cosine_similarity(query_embedding, item.embedding)
    results.append((contact["name"], similarity))

results.sort(key=lambda x: x[1], reverse=True)

for name, score in results:
    print(f"{name}  -> {score:.2f}")
