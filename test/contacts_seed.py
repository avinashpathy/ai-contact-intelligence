import os
from dataclasses import asdict, dataclass

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


@dataclass
class Contact:
    """Contact record stored in Pinecone with searchable description."""

    id: str
    name: str
    role: str
    email: str
    location: str
    years_experience: int
    skills: list[str]
    description: str

    def embedding_text(self) -> str:
        skills_line = ", ".join(self.skills)
        return (
            f"{self.role}. {self.description} "
            f"Skills: {skills_line}. "
            f"{self.years_experience} years experience. Based in {self.location}."
        )

    def to_metadata(self) -> dict:
        return asdict(self)


CONTACTS: list[Contact] = [
  Contact(
    id="john-smith",
    name="John Smith",
    role="Senior React Engineer",
    email="john.smith@example.com",
    location="San Francisco, CA",
    years_experience=8,
    skills=["React", "TypeScript", "Next.js", "GraphQL"],
    description="Builds performant SPAs and design systems for B2B SaaS products.",
  ),
  Contact(
    id="jane-doe",
    name="Jane Doe",
    role="Node.js Backend Developer",
    email="jane.doe@example.com",
    location="Austin, TX",
    years_experience=6,
    skills=["Node.js", "Express", "PostgreSQL", "Redis"],
    description="Designs REST and event-driven APIs for high-traffic web applications.",
  ),
  Contact(
    id="mike-johnson",
    name="Mike Johnson",
    role="UI Developer",
    email="mike.johnson@example.com",
    location="Seattle, WA",
    years_experience=5,
    skills=["React", "CSS", "Accessibility", "Storybook"],
    description="Implements accessible component libraries and responsive interfaces.",
  ),
  Contact(
    id="sarah-williams",
    name="Sarah Williams",
    role="AWS Solutions Architect",
    email="sarah.williams@example.com",
    location="Chicago, IL",
    years_experience=10,
    skills=["AWS", "Terraform", "VPC", "Well-Architected"],
    description="Designs secure, scalable cloud architectures for enterprise migrations.",
  ),
  Contact(
    id="david-brown",
    name="David Brown",
    role="DevOps Engineer",
    email="david.brown@example.com",
    location="Denver, CO",
    years_experience=7,
    skills=["Kubernetes", "Docker", "GitHub Actions", "AWS"],
    description="Automates CI/CD pipelines and manages container platforms on AWS.",
  ),
  Contact(
    id="emily-davis",
    name="Emily Davis",
    role="iOS Mobile Engineer",
    email="emily.davis@example.com",
    location="New York, NY",
    years_experience=6,
    skills=["Swift", "SwiftUI", "UIKit", "Core Data"],
    description="Ships native iOS apps with offline-first patterns and smooth UX.",
  ),
  Contact(
    id="alex-martinez",
    name="Alex Martinez",
    role="Full-Stack Developer",
    email="alex.martinez@example.com",
    location="Miami, FL",
    years_experience=5,
    skills=["Python", "Django", "React", "PostgreSQL"],
    description="Delivers end-to-end features from Django APIs to React dashboards.",
  ),
  Contact(
    id="lisa-anderson",
    name="Lisa Anderson",
    role="Data Engineer",
    email="lisa.anderson@example.com",
    location="Boston, MA",
    years_experience=9,
    skills=["Spark", "Airflow", "S3", "dbt"],
    description="Builds ETL pipelines and AWS data lakes for analytics teams.",
  ),
  Contact(
    id="tom-wilson",
    name="Tom Wilson",
    role="Frontend Engineer",
    email="tom.wilson@example.com",
    location="Portland, OR",
    years_experience=4,
    skills=["Vue.js", "Tailwind CSS", "Vite", "Pinia"],
    description="Develops Vue applications with modern build tooling and state management.",
  ),
  Contact(
    id="nina-patel",
    name="Nina Patel",
    role="Cloud Engineer",
    email="nina.patel@example.com",
    location="Atlanta, GA",
    years_experience=7,
    skills=["GCP", "Terraform", "Networking", "IAM"],
    description="Deploys multi-cloud infrastructure with Terraform and zero-trust networking.",
  ),
  Contact(
    id="chris-lee",
    name="Chris Lee",
    role="Java Backend Developer",
    email="chris.lee@example.com",
    location="Dallas, TX",
    years_experience=8,
    skills=["Java", "Spring Boot", "Kafka", "Microservices"],
    description="Builds event-driven microservices and integration layers for fintech.",
  ),
  Contact(
    id="priya-sharma",
    name="Priya Sharma",
    role="Site Reliability Engineer",
    email="priya.sharma@example.com",
    location="San Jose, CA",
    years_experience=6,
    skills=["Prometheus", "Grafana", "Kubernetes", "On-call"],
    description="Improves observability, SLOs, and incident response for production systems.",
  ),
  Contact(
    id="ryan-oconnor",
    name="Ryan O'Connor",
    role="Security Engineer",
    email="ryan.oconnor@example.com",
    location="Washington, DC",
    years_experience=7,
    skills=["IAM", "SOC2", "Penetration Testing", "AWS"],
    description="Hardens cloud workloads and leads security reviews for compliance programs.",
  ),
  Contact(
    id="maria-garcia",
    name="Maria Garcia",
    role="Android Mobile Engineer",
    email="maria.garcia@example.com",
    location="Los Angeles, CA",
    years_experience=5,
    skills=["Kotlin", "Jetpack Compose", "Room", "Firebase"],
    description="Builds Android apps with modern architecture and real-time sync.",
  ),
  Contact(
    id="kevin-nguyen",
    name="Kevin Nguyen",
    role="Machine Learning Engineer",
    email="kevin.nguyen@example.com",
    location="Toronto, ON",
    years_experience=4,
    skills=["Python", "PyTorch", "MLOps", "SageMaker"],
    description="Trains and deploys ML models with feature pipelines on AWS SageMaker.",
  ),
  Contact(
    id="rachel-kim",
    name="Rachel Kim",
    role="Product Designer",
    email="rachel.kim@example.com",
    location="Brooklyn, NY",
    years_experience=6,
    skills=["Figma", "UX Research", "Prototyping", "Design Systems"],
    description="Leads user research and designs flows for complex enterprise products.",
  ),
  Contact(
    id="james-taylor",
    name="James Taylor",
    role="Platform Engineer",
    email="james.taylor@example.com",
    location="Phoenix, AZ",
    years_experience=9,
    skills=["Go", "Kubernetes", "gRPC", "Internal Tools"],
    description="Builds developer platforms and shared services for engineering teams.",
  ),
  Contact(
    id="olivia-chen",
    name="Olivia Chen",
    role="QA Automation Engineer",
    email="olivia.chen@example.com",
    location="Minneapolis, MN",
    years_experience=5,
    skills=["Playwright", "Cypress", "CI/CD", "Test Strategy"],
    description="Automates end-to-end tests and integrates quality gates into release pipelines.",
  ),
  Contact(
    id="daniel-rodriguez",
    name="Daniel Rodriguez",
    role=".NET Backend Developer",
    email="daniel.rodriguez@example.com",
    location="Houston, TX",
    years_experience=7,
    skills=["C#", ".NET", "Azure", "SQL Server"],
    description="Develops enterprise APIs and integrations on Microsoft Azure.",
  ),
  Contact(
    id="sophia-miller",
    name="Sophia Miller",
    role="Technical Program Manager",
    email="sophia.miller@example.com",
    location="Remote",
    years_experience=11,
    skills=["Agile", "Roadmapping", "Stakeholder Management", "AWS Projects"],
    description="Coordinates cross-team cloud migrations and delivery for platform initiatives.",
  ),
]


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return [item.embedding for item in response.data]


def store_contacts_in_pinecone(contacts: list[Contact]) -> None:
    texts = [contact.embedding_text() for contact in contacts]
    embeddings = embed_texts(texts)

    vectors = [
        {
            "id": contact.id,
            "values": embedding,
            "metadata": contact.to_metadata(),
        }
        for contact, embedding in zip(contacts, embeddings)
    ]

    index.upsert(vectors=vectors)
    print(f"Stored {len(vectors)} contacts in '{INDEX_NAME}'")


if __name__ == "__main__":
    store_contacts_in_pinecone(CONTACTS)
