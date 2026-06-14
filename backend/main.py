from fastapi import FastAPI

from app.database.database import (
    engine,
    Base
)

import app.models.models

from app.api.diagnosis_api import router
from app.api.incident_api import router as incident_router
from app.api.history_api import router as history_router
from app.api.approval_api import router as approval_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLM Incident Diagnosis Engine"
)

app.include_router(router)
app.include_router(incident_router)
app.include_router(history_router)
app.include_router(approval_router)

@app.get("/")
def root():

    return {
        "message":
        "LLM Incident Diagnosis Engine Running"
    }

