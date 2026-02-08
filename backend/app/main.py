from fastapi import FastAPI

from app.api.applications import router as applications_router
from app.api.scoring import router as scoring_router

app = FastAPI(title="Job Application Tracker API")

app.include_router(applications_router)
app.include_router(scoring_router)


@app.get("/health")
def health():
    return {"status": "ok"}

