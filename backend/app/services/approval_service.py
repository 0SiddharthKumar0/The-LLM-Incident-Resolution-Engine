from dotenv import load_dotenv
from pathlib import Path
import os

from app.database.database import SessionLocal
from app.models.models import Approval

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path)


class ApprovalService:

    CONFIDENCE_THRESHOLD = float(
        os.getenv(
            "AUTO_APPROVAL_THRESHOLD",
            0.80
        )
    )

    @staticmethod
    def evaluate(confidence_score):

        if confidence_score >= ApprovalService.CONFIDENCE_THRESHOLD:
            return "AUTO_APPROVED"

        return "HUMAN_REVIEW_REQUIRED"

    @staticmethod
    def save_approval(
        diagnosis_id,
        action,
        reviewer="SYSTEM"
    ):

        session = SessionLocal()

        approval = Approval(
            diagnosis_id=diagnosis_id,
            action=action,
            reviewer=reviewer,
            comments="Generated automatically"
        )

        session.add(approval)

        session.commit()

        session.close()