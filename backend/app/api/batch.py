from fastapi import APIRouter, File, UploadFile, HTTPException, Query

from app.services.resume_parser import extract_text_from_pdf
from app.services.batch_analyzer import parse_jobs_csv, analyze_resume_against_jobs

router = APIRouter(prefix="/batch", tags=["batch"])


@router.post("/analyze")
async def analyze(
    resume_pdf: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
    debug: bool = Query(False, description="Return debug info about extracted resume text"),
):
    try:
        resume_bytes = await resume_pdf.read()
        jobs_bytes = await jobs_file.read()

        resume_text = extract_text_from_pdf(resume_bytes)
        if not resume_text or len(resume_text.strip()) < 30:
            raise HTTPException(
                status_code=400,
                detail="Could not extract enough text from resume PDF. If it's scanned/image-based, OCR is needed.",
            )

        jobs = parse_jobs_csv(jobs_bytes)
        if not jobs:
            raise HTTPException(status_code=400, detail="No jobs found in CSV")

        result = analyze_resume_against_jobs(resume_text, jobs)

        if debug:
            low = resume_text.lower()
            result["_debug"] = {
                "resume_text_length": len(resume_text),
                "contains_cirq": ("cirq" in low),
                "contains_benchmark": ("benchmark" in low),
                "contains_benchmarked": ("benchmarked" in low),
                "snippet": resume_text[:800],  # first 800 chars to inspect extraction quality
            }

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch analyze failed: {e}")