import csv
import io
from typing import Any, Dict, List

from app.services.scoring import score_resume


def parse_jobs_csv(file_bytes: bytes) -> List[Dict[str, str]]:
    text = file_bytes.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    required = {"title", "company", "description"}
    if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
        raise ValueError(f"CSV must contain columns: {sorted(required)} (job_id optional)")

    jobs: List[Dict[str, str]] = []
    for row in reader:
        jobs.append({
            "job_id": (row.get("job_id") or "").strip(),
            "title": (row.get("title") or "").strip(),
            "company": (row.get("company") or "").strip(),
            "description": (row.get("description") or "").strip(),
        })
    return jobs


def analyze_resume_against_jobs(resume_text: str, jobs: List[Dict[str, str]]) -> Dict[str, Any]:
    results = []
    for job in jobs:
        jd = job["description"]
        score = score_resume(resume_text, jd)
        results.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            **score,
        })

    # Sort best matches first
    results.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "total_jobs": len(results),
        "results": results,
    }
