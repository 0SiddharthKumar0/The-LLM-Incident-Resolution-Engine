from app.database.database import SessionLocal
from app.models.models import AuditLog


class AuditService:

    @staticmethod
    def log_event(
        incident_id,
        event_type,
        event_details
    ):
        print("AUDIT SERVICE CALLED")
        session = SessionLocal()

        log = AuditLog(
            incident_id=incident_id,
            event_type=event_type,
            event_details=event_details
        )

        session.add(log)

        session.commit()

        session.close()