from sentence_transformers import SentenceTransformer

from app.database.database import SessionLocal
from app.models.models import KnowledgeDocument

model = SentenceTransformer("all-MiniLM-L6-v2")

session = SessionLocal()

documents = session.query(KnowledgeDocument).all()

print(f"Found {len(documents)} documents")

for doc in documents:
    text = f"{doc.title}\n{doc.content}"

    embedding = model.encode(text)

    print(
        f"Document ID={doc.id} | "
        f"Type={doc.doc_type} | "
        f"Embedding Length={len(embedding)}"
    )

session.close()