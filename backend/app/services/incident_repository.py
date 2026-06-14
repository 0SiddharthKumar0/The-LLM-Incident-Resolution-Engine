from app.database.database import SessionLocal
from app.models.models import Incident


class IncidentRepository:

    @staticmethod
    def create_incident(
        incident_code,
        service,
        severity,
        description
    ):

        session = SessionLocal()

        incident = Incident(
            incident_id=incident_code,
            service=service,
            severity=severity,
            description=description
        )

        session.add(incident)

        session.commit()

        session.refresh(incident)

        incident_db_id = incident.id

        session.close()

        return incident_db_id

    @staticmethod
    def get_all_incidents():

        session = SessionLocal()

        incidents = session.query(
            Incident
        ).all()

        session.close()

        return incidents