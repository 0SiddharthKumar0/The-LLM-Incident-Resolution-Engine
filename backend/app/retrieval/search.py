from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.database.database import SessionLocal
from app.models.models import KnowledgeDocument


client = QdrantClient(
    path="./qdrant_storage"
)

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
                "doc_type": doc.doc_type
            }
        )
    )

client.upsert(
    collection_name="knowledge_base",
    points=points
)

query = "payment api database timeout"

query_embedding = model.encode(query).tolist()

results = client.query_points(
    collection_name="knowledge_base",
    query=query_embedding,
    limit=3
)

print("\nTop Matches:\n")

for point in results.points:
    print(point.payload)