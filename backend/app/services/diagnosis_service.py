from urllib import response

from qdrant_client import models

from app.services.approval_service import ApprovalService
from app.confidence.confidence_service import ConfidenceService

from app.services.diagnosis_repository import DiagnosisRepository

from sentence_transformers import SentenceTransformer
from app.audit.audit_service import AuditService
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.database.database import SessionLocal
from app.models.models import KnowledgeDocument
from app.llm.llm_provider import generate_response


class DiagnosisService:

    def __init__(self):

        self.client = QdrantClient(
            path="./qdrant_storage"
        )

        try:

            self.client.create_collection(
                collection_name="knowledge_base",
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )

        except:

            pass

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.load_documents()

    def load_documents(self):

        session = SessionLocal()

        documents = session.query(
            KnowledgeDocument
        ).all()

        points = []

        for doc in documents:

            text = f"{doc.title}\n{doc.content}"

            embedding = self.model.encode(
                text
            ).tolist()

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

        self.client.upsert(
            collection_name="knowledge_base",
            points=points
        )

        session.close()

    def diagnose(self, incident_text, incident_db_id):

        query_embedding = self.model.encode(
            incident_text
        ).tolist()

        results = self.client.query_points(
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
{incident_text}

Relevant Knowledge:
{context}

Provide:

1. Likely Root Cause
2. Confidence Score (0-1)
3. Recommended Actions
"""

        response = generate_response(prompt)

        confidence = (
            ConfidenceService.extract_confidence(
                response
            )
        )

        approval_status = (
            ApprovalService.evaluate(
                confidence
            )
        )

        diagnosis_id = (
            DiagnosisRepository.save_diagnosis(
                incident_id=incident_db_id,
                root_cause=response,
                confidence_score=confidence,
                recommendation=response
            )
        )

        ApprovalService.save_approval(
            diagnosis_id=diagnosis_id,
            action=approval_status
        )

        AuditService.log_event(
            incident_id=incident_db_id,
            event_type=approval_status,
            event_details=response
        )

        return {
            "approval_status": approval_status,
            "confidence_score": confidence,
            "diagnosis": response
        }