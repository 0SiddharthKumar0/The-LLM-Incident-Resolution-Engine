from fastapi import APIRouter

from app.database.database import SessionLocal
from app.models.models import Diagnosis

router = APIRouter()


@router.get("/diagnoses")
def get_diagnoses():

    session = SessionLocal()

    diagnoses = session.query(
        Diagnosis
    ).all()

    result = []

    for diagnosis in diagnoses:

        result.append(
            {
                "id": diagnosis.id,
                "incident_id": diagnosis.incident_id,
                "confidence_score": diagnosis.confidence_score,
                "status": diagnosis.status
            }
        )

    session.close()

    return result


@router.get("/diagnosis/{diagnosis_id}")
def get_diagnosis(
    diagnosis_id: int
):

    session = SessionLocal()

    diagnosis = session.query(
        Diagnosis
    ).filter(
        Diagnosis.id == diagnosis_id
    ).first()

    session.close()

    if not diagnosis:

        return {
            "message": "Diagnosis not found"
        }

    return {
        "id": diagnosis.id,
        "incident_id": diagnosis.incident_id,
        "root_cause": diagnosis.root_cause,
        "recommendation": diagnosis.recommendation,
        "confidence_score": diagnosis.confidence_score,
        "status": diagnosis.status
    }