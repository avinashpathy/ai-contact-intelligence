from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()

client = OpenAI()

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )

embedding = []

texts = [
    "Frontend Engineer",
    "React Developer",
    # "UI Engineer",
    # "Backend Engineer"
]

for i in range(len(texts)):
    response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts[i]
    )
    embedding.append(response.data[0].embedding)

similarity_result = cosine_similarity(embedding[0], embedding[1])
print(f"similarity result: {similarity_result}")

# print(embedding[:10])
# print(len(embedding))


# Steps:

# 1

# Generate query embedding.

# 2

# Generate contact embeddings.

# 3

# Calculate similarity.

# 4

# Sort descending.

# 5

# Print results.
