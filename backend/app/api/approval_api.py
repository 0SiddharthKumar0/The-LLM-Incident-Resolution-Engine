from fastapi import APIRouter
from requests import session

from app.database.database import SessionLocal
from app.models.models import Approval
from app.audit.audit_service import AuditService



router = APIRouter()


@router.post("/approve/{approval_id}")
def approve(
    approval_id: int
):

    session = SessionLocal()

    approval = session.query(
        Approval
    ).filter(
        Approval.id == approval_id
    ).first()

    if not approval:

        session.close()

        return {
            "message": "Approval not found"
        }
    
    approval.action = "APPROVED"

    session.commit()

    AuditService.log_event(
    incident_id=None,
    event_type="APPROVAL_GRANTED",
    details=f"Approval ID {approval_id} approved"
    )

    session.close()

    return {
        "message": "Approved"
    }


@router.post("/reject/{approval_id}")
def reject(
    approval_id: int
):

    session = SessionLocal()

    approval = session.query(
        Approval
    ).filter(
        Approval.id == approval_id
    ).first()

    if not approval:

        session.close()

        return {
            "message": "Approval not found"
        }

    approval.action = "REJECTED"

    session.commit()

    AuditService.log_event(
    incident_id=None,
    event_type="APPROVAL_REJECTED",
    details=f"Approval ID {approval_id} rejected"
    )

    session.close()

    return {
        "message": "Rejected"
    }