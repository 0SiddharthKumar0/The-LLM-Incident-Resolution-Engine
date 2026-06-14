from app.database.database import SessionLocal
from app.models.models import Diagnosis


class DiagnosisRepository:

    @staticmethod
    def save_diagnosis(
        incident_id,
        root_cause,
        confidence_score,
        recommendation
    ):

        session = SessionLocal()

        diagnosis = Diagnosis(
            incident_id=incident_id,
            root_cause=root_cause,
            confidence_score=confidence_score,
            recommendation=recommendation
        )

        session.add(diagnosis)

        session.commit()

        session.refresh(diagnosis)

        diagnosis_id = diagnosis.id

        session.close()

        return diagnosis_id