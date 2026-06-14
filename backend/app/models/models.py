from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime
)
from sqlalchemy.sql import func

from app.database.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, nullable=False)
    service = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=False)
    root_cause = Column(Text)
    recommendation = Column(Text)
    confidence_score = Column(Float)
    status = Column(String, default="PENDING_APPROVAL")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    reviewer = Column(String)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer)
    event_type = Column(String, nullable=False)
    event_details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())