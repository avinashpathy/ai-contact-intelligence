import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.contacts_seed import contacts
from src.services.embedding_service import generate_embedding
from src.services.pinecone_service import index


def build_contact_text(contact):
    return f"""
    Name: {contact['name']}
    Title: {contact['title']}
    Location: {contact['location']}
    Skills: {', '.join(contact['skills'])}
    """


def ingest_contacts():
    vectors = []

    for contact in contacts:

        embedding = generate_embedding(
            build_contact_text(contact)
        )

        vectors.append(
            {
                "id": contact["contactId"],
                "values": embedding,
                "metadata": {
                    "name": contact["name"],
                    "title": contact["title"],
                    "location": contact["location"],
                    "skills": contact["skills"],
                }
            }
        )

    index.upsert(
        vectors=vectors
    )

    print("Contacts indexed")


if __name__ == "__main__":
    ingest_contacts()
