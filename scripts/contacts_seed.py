import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

contacts = [
    {
        "contactId": "1",
        "name": "John Doe",
        "title": "Frontend Engineer",
        "location": "Bangalore",
        "skills": ["React", "TypeScript", "AWS"]
    },
    {
        "contactId": "2",
        "name": "Sarah Smith",
        "title": "Backend Engineer",
        "location": "Hyderabad",
        "skills": ["Python", "FastAPI", "AWS"]
    },
    {
        "contactId": "3",
        "name": "Mike Johnson",
        "title": "Cloud Architect",
        "location": "Bangalore",
        "skills": ["AWS", "Terraform", "Kubernetes"]
    },
    {
        "contactId": "4",
        "name": "Priya Nair",
        "title": "Senior React Engineer",
        "location": "Chennai",
        "skills": ["React", "Next.js", "GraphQL"]
    },
    {
        "contactId": "5",
        "name": "Arjun Mehta",
        "title": "DevOps Engineer",
        "location": "Mumbai",
        "skills": ["Docker", "CI/CD", "AWS", "Kubernetes"]
    },
    {
        "contactId": "6",
        "name": "Anita Rao",
        "title": "Data Engineer",
        "location": "Hyderabad",
        "skills": ["Spark", "Python", "S3", "Airflow"]
    },
    {
        "contactId": "7",
        "name": "Rahul Verma",
        "title": "Full Stack Developer",
        "location": "Delhi",
        "skills": ["React", "Node.js", "PostgreSQL", "AWS"]
    },
    {
        "contactId": "8",
        "name": "Deepa Iyer",
        "title": "UI Developer",
        "location": "Bangalore",
        "skills": ["React", "CSS", "Accessibility", "Figma"]
    },
    {
        "contactId": "9",
        "name": "Karthik Reddy",
        "title": "Java Backend Developer",
        "location": "Chennai",
        "skills": ["Java", "Spring Boot", "Kafka", "Microservices"]
    },
    {
        "contactId": "10",
        "name": "Neha Kapoor",
        "title": "AWS Solutions Architect",
        "location": "Pune",
        "skills": ["AWS", "VPC", "IAM", "Well-Architected"]
    },
    {
        "contactId": "11",
        "name": "Vikram Singh",
        "title": "Site Reliability Engineer",
        "location": "Gurgaon",
        "skills": ["Prometheus", "Grafana", "Kubernetes", "AWS"]
    },
    {
        "contactId": "12",
        "name": "Meera Joshi",
        "title": "iOS Engineer",
        "location": "Mumbai",
        "skills": ["Swift", "SwiftUI", "Core Data"]
    },
    {
        "contactId": "13",
        "name": "Sanjay Pillai",
        "title": "Python Backend Developer",
        "location": "Kochi",
        "skills": ["Python", "Django", "Redis", "PostgreSQL"]
    },
    {
        "contactId": "14",
        "name": "Lakshmi Devi",
        "title": "Cloud Engineer",
        "location": "Hyderabad",
        "skills": ["GCP", "Terraform", "Networking"]
    },
    {
        "contactId": "15",
        "name": "Rohan Das",
        "title": "React Native Developer",
        "location": "Kolkata",
        "skills": ["React Native", "JavaScript", "Firebase"]
    },
    {
        "contactId": "16",
        "name": "Pooja Sharma",
        "title": "Security Engineer",
        "location": "Bangalore",
        "skills": ["AWS", "IAM", "SOC2", "Penetration Testing"]
    },
    {
        "contactId": "17",
        "name": "Aditya Ghosh",
        "title": "Platform Engineer",
        "location": "Pune",
        "skills": ["Go", "Kubernetes", "AWS EKS", "Terraform"]
    },
    {
        "contactId": "18",
        "name": "Maria Garcia",
        "title": "Android Engineer",
        "location": "Bangalore",
        "skills": ["Kotlin", "Jetpack Compose", "Room"]
    },
    {
        "contactId": "19",
        "name": "Kevin Nguyen",
        "title": "Machine Learning Engineer",
        "location": "Chennai",
        "skills": ["Python", "PyTorch", "SageMaker", "MLOps"]
    },
    {
        "contactId": "20",
        "name": "Tom Wilson",
        "title": "Frontend Engineer",
        "location": "Pune",
        "skills": ["Vue.js", "Tailwind CSS", "Vite"]
    },
    {
        "contactId": "21",
        "name": "Jane Smith",
        "title": "Node.js Developer",
        "location": "Hyderabad",
        "skills": ["Node.js", "Express", "DynamoDB", "AWS"]
    },
    {
        "contactId": "22",
        "name": "Chris Lee",
        "title": "Backend Engineer",
        "location": "Dallas",
        "skills": ["Java", "Spring Boot", "RabbitMQ", "AWS"]
    },
    {
        "contactId": "23",
        "name": "Olivia Chen",
        "title": "QA Automation Engineer",
        "location": "Bangalore",
        "skills": ["Playwright", "Cypress", "CI/CD", "Test Strategy"]
    },
    {
        "contactId": "24",
        "name": "Daniel Rodriguez",
        "title": ".NET Backend Developer",
        "location": "Mumbai",
        "skills": ["C#", ".NET", "Azure", "SQL Server"]
    },
    {
        "contactId": "25",
        "name": "Sophia Miller",
        "title": "Technical Program Manager",
        "location": "Remote",
        "skills": ["Agile", "Roadmapping", "AWS Projects", "Stakeholder Management"]
    },
    {
        "contactId": "26",
        "name": "James Taylor",
        "title": "Mobile Engineer",
        "location": "Delhi",
        "skills": ["React Native", "TypeScript", "Redux"]
    },
    {
        "contactId": "27",
        "name": "Emily Davis",
        "title": "Data Scientist",
        "location": "Bangalore",
        "skills": ["Python", "Pandas", "Scikit-learn", "AWS"]
    },
    {
        "contactId": "28",
        "name": "Nina Patel",
        "title": "Infrastructure Engineer",
        "location": "Ahmedabad",
        "skills": ["Linux", "Ansible", "AWS", "Monitoring"]
    },
    {
        "contactId": "29",
        "name": "Ethan Wright",
        "title": "API Developer",
        "location": "Pune",
        "skills": ["REST", "OpenAPI", "Node.js", "AWS Lambda"]
    },
    {
        "contactId": "30",
        "name": "Rachel Kim",
        "title": "Product Designer",
        "location": "Bangalore",
        "skills": ["Figma", "UX Research", "Design Systems", "Prototyping"]
    },
]

def seed_contacts():
    from src.services.dynamo_service import save_contact

    for contact in contacts:

        save_contact(contact)

    print("Contacts seeded")


if __name__ == "__main__":
    seed_contacts()
