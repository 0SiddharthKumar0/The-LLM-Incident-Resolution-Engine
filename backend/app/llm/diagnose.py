from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.database.database import SessionLocal
from app.models.models import KnowledgeDocument
from app.llm.llm_provider import generate_response


client = QdrantClient(path="./qdrant_storage")

client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

model = SentenceTransformer("all-MiniLM-L6-v2")

session = SessionLocal()

documents = session.query(KnowledgeDocument).all()

points = []

for doc in documents:

    text = f"{doc.title}\n{doc.content}"

    embedding = model.encode(text).tolist()

    points.append(
        PointStruct(
            id=doc.id,
            vector=embedding,
            payload={
                "title": doc.title,
                "doc_type": doc.doc_type,
                "content": doc.content
            }
        )
    )

client.upsert(
    collection_name="knowledge_base",
    points=points
)

incident = """
Payment API returning 503 errors.
Database timeout observed.
High latency across requests.
"""

query_embedding = model.encode(incident).tolist()

results = client.query_points(
    collection_name="knowledge_base",
    query=query_embedding,
    limit=3
)

context = ""

for point in results.points:
    context += f"""
Title: {point.payload['title']}
Type: {point.payload['doc_type']}
Content: {point.payload['content']}
"""

prompt = f"""
You are an SRE incident diagnosis assistant.

Incident:
{incident}

Relevant Knowledge:
{context}

Provide:

1. Likely Root Cause
2. Confidence Score (0-1)
3. Recommended Actions
"""

response = generate_response(prompt)

print("\n===== DIAGNOSIS =====\n")
print(response)

session.close()