import os

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = "contacts-index"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
CHAT_MODEL = "gpt-4.1-mini"

client = OpenAI()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY") or os.getenv("PINECON_API_KEY"))
index = pc.Index(INDEX_NAME)

contacts = [
    {
        "contactId": "1",
        "name": "John Doe",
        "title": "Senior React Engineer",
        "location": "Bangalore",
        "skills": ["React", "TypeScript", "AWS Lambda"],
    },
    {
        "contactId": "2",
        "name": "Jane Smith",
        "title": "Backend Engineer",
        "location": "Hyderabad",
        "skills": ["Node.js", "DynamoDB", "AWS"],
    },
    {
        "contactId": "3",
        "name": "Mike Johnson",
        "title": "Cloud Architect",
        "location": "Bangalore",
        "skills": ["AWS", "Terraform", "Kubernetes"],
    },
    {
        "contactId": "4",
        "name": "Sarah Wilson",
        "title": "Mobile Engineer",
        "location": "Pune",
        "skills": ["React Native", "TypeScript"],
    },
    {
        "contactId": "5",
        "name": "Priya Nair",
        "title": "Frontend Engineer",
        "location": "Chennai",
        "skills": ["Vue.js", "JavaScript", "Tailwind CSS"],
    },
    {
        "contactId": "6",
        "name": "Arjun Mehta",
        "title": "DevOps Engineer",
        "location": "Mumbai",
        "skills": ["AWS", "Docker", "CI/CD", "Kubernetes"],
    },
    {
        "contactId": "7",
        "name": "Anita Rao",
        "title": "Data Engineer",
        "location": "Hyderabad",
        "skills": ["Spark", "Python", "S3", "AWS Glue"],
    },
    {
        "contactId": "8",
        "name": "Rahul Verma",
        "title": "Full Stack Developer",
        "location": "Delhi",
        "skills": ["React", "Node.js", "PostgreSQL", "AWS"],
    },
    {
        "contactId": "9",
        "name": "Deepa Iyer",
        "title": "UI Developer",
        "location": "Bangalore",
        "skills": ["React", "CSS", "Accessibility", "Figma"],
    },
    {
        "contactId": "10",
        "name": "Karthik Reddy",
        "title": "Java Backend Developer",
        "location": "Chennai",
        "skills": ["Java", "Spring Boot", "Microservices", "Kafka"],
    },
    {
        "contactId": "11",
        "name": "Neha Kapoor",
        "title": "AWS Solutions Architect",
        "location": "Pune",
        "skills": ["AWS", "VPC", "IAM", "Well-Architected"],
    },
    {
        "contactId": "12",
        "name": "Vikram Singh",
        "title": "Site Reliability Engineer",
        "location": "Gurgaon",
        "skills": ["Prometheus", "Grafana", "Kubernetes", "AWS"],
    },
    {
        "contactId": "13",
        "name": "Meera Joshi",
        "title": "iOS Engineer",
        "location": "Mumbai",
        "skills": ["Swift", "SwiftUI", "Core Data"],
    },
    {
        "contactId": "14",
        "name": "Sanjay Pillai",
        "title": "Python Backend Developer",
        "location": "Kochi",
        "skills": ["Python", "FastAPI", "Redis", "PostgreSQL"],
    },
    {
        "contactId": "15",
        "name": "Lakshmi Devi",
        "title": "Cloud Engineer",
        "location": "Hyderabad",
        "skills": ["GCP", "Terraform", "Networking"],
    },
    {
        "contactId": "16",
        "name": "Rohan Das",
        "title": "React Native Developer",
        "location": "Kolkata",
        "skills": ["React Native", "JavaScript", "Firebase"],
    },
    {
        "contactId": "17",
        "name": "Pooja Sharma",
        "title": "Security Engineer",
        "location": "Bangalore",
        "skills": ["AWS", "IAM", "SOC2", "Penetration Testing"],
    },
    {
        "contactId": "18",
        "name": "Aditya Ghosh",
        "title": "Platform Engineer",
        "location": "Pune",
        "skills": ["Go", "Kubernetes", "AWS EKS", "Terraform"],
    },
]


def build_contact_text(contact: dict) -> str:
    return f"""
Name: {contact['name']}
Title: {contact['title']}
Location: {contact['location']}
Skills: {", ".join(contact['skills'])}
"""


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return response.data[0].embedding


def store_contacts_in_pinecone() -> None:
    index.delete(delete_all=True)

    vectors = []

    for contact in contacts:
        contact_text = build_contact_text(contact)
        embedding = generate_embedding(contact_text)

        vectors.append(
            {
                "id": contact["contactId"],
                "values": embedding,
                "metadata": {
                    "name": contact["name"],
                    "title": contact["title"],
                    "location": contact["location"],
                    "skills": contact["skills"],
                },
            }
        )

    index.upsert(vectors=vectors)
    print("Contacts stored successfully")


def search_contacts(query: str, top_k: int = 5) -> dict:
    query_embedding = generate_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    return results


def rag_search(query: str, top_k: int = 10) -> str:
    search_results = search_contacts(query, top_k=top_k)

    context = ""
    for match in search_results["matches"]:
        metadata = match["metadata"]
        title = metadata.get("title") or metadata.get("role", "")
        skills = metadata.get("skills", [])
        skills_text = ", ".join(skills) if isinstance(skills, list) else str(skills)
        context += f"""
Name: {metadata.get('name', '')}
Title: {title}
Location: {metadata.get('location', '')}
Skills: {skills_text}
"""

    prompt = f"""
You are a recruiting assistant.

Contacts:
{context}

Question:
{query}

Answer only using the provided contacts.
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    store_contacts_in_pinecone()

    print("\n--- Step 9: Test Search ---\n")
    results = search_contacts("Find frontend developers with AWS experience", top_k=10)

    for match in results["matches"]:
        print(match["score"], match["metadata"])

    print("\n--- Step 10: Test RAG ---\n")
    answer = rag_search(
        "Who are the strongest frontend engineers with AWS experience?"
    )
    print(answer)
