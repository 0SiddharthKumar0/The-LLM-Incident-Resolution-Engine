from fastapi import APIRouter

from app.services.incident_repository import (
    IncidentRepository
)

router = APIRouter()


@router.post("/incident")
def create_incident(payload: dict):

    incident_db_id = (
        IncidentRepository.create_incident(
            incident_code=payload["incident_id"],
            service=payload["service"],
            severity=payload["severity"],
            description=payload["description"]
        )
    )

    return {
        "incident_db_id": incident_db_id
    }


@router.get("/incidents")
def get_incidents():

    incidents = (
        IncidentRepository.get_all_incidents()
    )

    result = []

    for incident in incidents:

        result.append(
            {
                "id": incident.id,
                "incident_id": incident.incident_id,
                "service": incident.service,
                "severity": incident.severity,
                "status": incident.status
            }
        )

    return result