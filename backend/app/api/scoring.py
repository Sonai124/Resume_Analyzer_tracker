from fastapi import APIRouter
from pydantic import BaseModel

from app.services.scoring import score_resume

router = APIRouter(prefix="/score", tags=["scoring"])


class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/")
def score(req: ScoreRequest):
    return score_resume(req.resume_text, req.job_description)
