import json
from pathlib import Path

from app.database.database import SessionLocal
from app.models.models import Incident, KnowledgeDocument


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "sample-data"


def load_incidents():
    session = SessionLocal()

    with open(DATA_DIR / "incidents.json", "r", encoding="utf-8") as file:
        incidents = json.load(file)

    for incident in incidents:
        db_incident = Incident(
            incident_id=incident["incident_id"],
            service=incident["service"],
            severity=incident["severity"],
            description=", ".join(incident["symptoms"])
        )

        session.add(db_incident)

    session.commit()
    session.close()

    print(f"Loaded {len(incidents)} incidents")


def load_knowledge_documents():
    session = SessionLocal()

    with open(DATA_DIR / "runbooks.json", "r", encoding="utf-8") as file:
        runbooks = json.load(file)

    for runbook in runbooks:
        document = KnowledgeDocument(
            doc_type="RUNBOOK",
            title=runbook["title"],
            content="\n".join(runbook["steps"]),
            source_id=runbook["runbook_id"]
        )

        session.add(document)

    with open(DATA_DIR / "architecture_docs.json", "r", encoding="utf-8") as file:
        architecture_docs = json.load(file)

    for doc in architecture_docs:
        document = KnowledgeDocument(
            doc_type="ARCHITECTURE",
            title=doc["service"],
            content=doc["description"],
            source_id=doc["service"]
        )

        session.add(document)

    session.commit()
    session.close()

    print(
        f"Loaded {len(runbooks)} runbooks and "
        f"{len(architecture_docs)} architecture documents"
    )


if __name__ == "__main__":
#    load_incidents()
    load_knowledge_documents()