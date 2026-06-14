from fastapi import APIRouter

from app.services.diagnosis_service import (
    DiagnosisService
)

router = APIRouter()

diagnosis_service = DiagnosisService()


@router.post("/diagnose")
def diagnose(payload: dict):
   
    incident_text = payload["description"]

    incident_db_id = payload["incident_db_id"]

    diagnosis = diagnosis_service.diagnose(
        incident_text,
        incident_db_id
    )

    return {
        "diagnosis": diagnosis
    }