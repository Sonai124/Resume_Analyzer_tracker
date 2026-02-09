from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.resume_parser import extract_text_from_pdf
from app.services.batch_analyzer import parse_jobs_csv, analyze_resume_against_jobs

router = APIRouter(prefix="/batch", tags=["batch"])


@router.post("/analyze")
async def analyze(
    resume_pdf: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
):
    # Validate inputs
    if not resume_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="resume_pdf must be a .pdf file")

    if not jobs_file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="jobs_file must be a .csv file")

    resume_bytes = await resume_pdf.read()
    jobs_bytes = await jobs_file.read()

    try:
        resume_text = extract_text_from_pdf(resume_bytes)
        if not resume_text:
            raise ValueError("Could not extract text from PDF (is it scanned image-only?)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume PDF parsing failed: {e}")

    try:
        jobs = parse_jobs_csv(jobs_bytes)
        if not jobs:
            raise ValueError("No jobs found in CSV")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Jobs CSV parsing failed: {e}")

    return analyze_resume_against_jobs(resume_text, jobs)
