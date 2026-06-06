import os

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = "contacts-index"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 512

openai_client = OpenAI()
pinecone_client = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY") or os.getenv("PINECON_API_KEY")
)
index = pinecone_client.Index(INDEX_NAME)

contacts = [
    {
        "id": "john",
        "name": "John",
        "description": "Senior React Engineer building SPAs with TypeScript and modern frontend tooling",
    },
    {
        "id": "jane",
        "name": "Jane",
        "description": "Backend engineer specializing in Node.js, Express APIs, and REST microservices",
    },
    {
        "id": "mike",
        "name": "Mike",
        "description": "UI developer focused on React, component libraries, and accessible web interfaces",
    },
    {
        "id": "sarah",
        "name": "Sarah",
        "description": "AWS Solutions Architect designing scalable cloud infrastructure and Well-Architected workloads",
    },
    {
        "id": "david",
        "name": "David",
        "description": "DevOps engineer experienced with CI/CD pipelines, Docker, and Kubernetes on AWS",
    },
    {
        "id": "emily",
        "name": "Emily",
        "description": "Mobile engineer building native iOS applications with Swift and SwiftUI",
    },
    {
        "id": "alex",
        "name": "Alex",
        "description": "Full-stack developer working with Python Django, PostgreSQL, and API design",
    },
    {
        "id": "lisa",
        "name": "Lisa",
        "description": "Data engineer building ETL pipelines with Spark, S3, and AWS data lake architectures",
    },
    {
        "id": "tom",
        "name": "Tom",
        "description": "Frontend engineer shipping Vue.js applications with Tailwind CSS and Vite",
    },
    {
        "id": "nina",
        "name": "Nina",
        "description": "Cloud engineer deploying multi-cloud infrastructure with GCP, Terraform, and networking",
    },
    {
        "id": "chris",
        "name": "Chris",
        "description": "Java backend developer building Spring Boot microservices and event-driven systems",
    },
    {
        "id": "priya",
        "name": "Priya",
        "description": "Site reliability engineer improving uptime, observability, and incident response in production",
    },
]

SEARCH_QUERIES = [
    "Find frontend developers",
    "Find cloud engineers",
    "Find AWS experts",
    "Find backend developers",
]


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return [item.embedding for item in response.data]


def store_contacts() -> None:
    descriptions = [c["description"] for c in contacts]
    embeddings = embed_texts(descriptions)

    vectors = [
        {
            "id": contact["id"],
            "values": embedding,
            "metadata": {
                "name": contact["name"],
                "description": contact["description"],
            },
        }
        for contact, embedding in zip(contacts, embeddings)
    ]

    index.upsert(vectors=vectors)
    print(f"Stored {len(vectors)} contacts in '{INDEX_NAME}'\n")


def search(query: str, top_k: int = 5) -> None:
    query_embedding = embed_texts([query])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    print(f"Query: {query}")
    print("-" * 50)
    for rank, match in enumerate(results["matches"], start=1):
        name = match["metadata"]["name"]
        description = match["metadata"]["description"]
        score = match["score"]
        print(f"{rank}. {name}  -> {score:.4f}")
        print(f"   {description}")
    print()


def print_observations() -> None:
    print("=" * 50)
    print("Observations")
    print("=" * 50)
    print(
        """
- Similarity scores are cosine similarity (0–1); higher = closer match.
- Rankings usually put React/UI/Vue contacts first for frontend queries.
- Cloud vs AWS: 'cloud engineer' may rank GCP (Nina) and AWS (Sarah, Lisa) highly;
  'AWS experts' should favor Sarah, Lisa, and David (DevOps on AWS).
- Backend queries should favor Jane, Chris, and Alex; watch for full-stack bleed.
- Surprising matches often happen when descriptions share vocabulary
  (e.g. 'engineer', 'APIs', 'production') even when the role differs.
- Re-run after changing contacts; upsert overwrites vectors with the same id.
"""
    )


if __name__ == "__main__":
    store_contacts()

    for query in SEARCH_QUERIES:
        search(query)

    print_observations()
