# Resume Analyzer & Job Match Engine

An AI-assisted backend tool that analyzes a resume against multiple job
descriptions and highlights the best matches along with missing skills.

This project was built as a collaboration between a **software engineer
(Python/ML)** and a **DevOps engineer**, focusing on practical backend
architecture, API design, and automated analysis.

------------------------------------------------------------------------

# Problem

When applying to jobs, candidates often:

-   Manually read many job descriptions
-   Guess how well their resume fits
-   Miss important keywords recruiters look for
-   Spend a lot of time tailoring applications

This project automates that process.

------------------------------------------------------------------------

# What This Project Does

Given:

• A **resume (PDF)**\
• A **list of job descriptions (CSV)**

The system:

1.  Extracts text from the resume
2.  Processes each job description
3.  Calculates a similarity score
4.  Identifies missing keywords
5.  Ranks the best job matches

------------------------------------------------------------------------

# Features

• Resume parsing from PDF\
• Batch analysis against multiple jobs\
• Keyword extraction using TF‑IDF\
• Similarity scoring using cosine similarity\
• FastAPI backend with interactive API docs\
• Modular architecture for easy extension

------------------------------------------------------------------------

# Tech Stack

## Backend

-   Python
-   FastAPI
-   Scikit‑learn
-   Pydantic
-   Uvicorn

## Data Processing

-   TF‑IDF Vectorization
-   Cosine Similarity
-   CSV parsing
-   PDF text extraction

## Dev Tools

-   Git
-   VS Code
-   Virtual environments

Future DevOps Integration - Docker - CI/CD - Cloud deployment

------------------------------------------------------------------------

# Project Structure

    Resume_Analyzer_tracker
    │
    ├── backend
    │   └── app
    │       ├── api
    │       │   ├── applications.py
    │       │   ├── scoring.py
    │       │   └── batch.py
    │       │
    │       ├── services
    │       │   ├── scoring.py
    │       │   ├── resume_parser.py
    │       │   └── batch_analyzer.py
    │       │
    │       ├── models
    │       │   └── application.py
    │       │
    │       ├── core
    │       │   └── database.py
    │       │
    │       └── main.py
    │
    ├── data
    │   ├── resume.pdf
    │   └── jobs.csv
    │
    └── README.md

------------------------------------------------------------------------

# Running the Project

## 1. Clone the repository

``` bash
git clone <repo_url>
cd Resume_Analyzer_tracker
```

## 2. Install dependencies

``` bash
pip install fastapi uvicorn scikit-learn python-multipart pypdf
```

## 3. Start the server

``` bash
cd backend
python -m uvicorn app.main:app --reload
```

Server will run at:

    http://127.0.0.1:8000

------------------------------------------------------------------------

# 4. Open the API interface

    http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 5. Run Resume Analysis

Endpoint:

    POST /batch/analyze

Upload:

• resume.pdf\
• jobs.csv

The API returns ranked job matches and missing skills.

------------------------------------------------------------------------

# Example CSV Format

    job_id,title,company,description
    1,Backend Engineer,ExampleCorp,"Python, FastAPI, Docker"
    2,ML Engineer,AI Labs,"Python, ML, TensorFlow"

------------------------------------------------------------------------

# Future Improvements

• Resume storage and versioning\
• Job scraping from LinkedIn / Indeed\
• Skill gap recommendations\
• Frontend dashboard\
• Authentication & user profiles\
• Dockerized deployment\
• Cloud hosting

------------------------------------------------------------------------

# Why This Project Matters

This project demonstrates:

-   real‑world API design
-   data processing pipelines
-   ML‑based scoring
-   clean backend architecture
-   collaboration between dev and DevOps roles

------------------------------------------------------------------------



