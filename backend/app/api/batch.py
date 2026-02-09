from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.resume_parser import extract_text_from_pdf
from app.services.batch_analyzer import (
    parse_jobs_csv,
    analyze_resume_against_jobs,
)

router = APIRouter(prefix="/batch", tags=["batch"])


@router.post("/analyze")
async def analyze(
    resume_pdf: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
):
    if not resume_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Resume must be PDF")

    if not jobs_file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Jobs file must be CSV")

    resume_bytes = await resume_pdf.read()
    jobs_bytes = await jobs_file.read()

    resume_text = extract_text_from_pdf(resume_bytes)
    jobs = parse_jobs_csv(jobs_bytes)

    return analyze_resume_against_jobs(resume_text, jobs)
