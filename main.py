from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import os
import shutil

app = FastAPI(title="Mini Resume Management API", version="1.0.0")

# Configuration

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
MAX_GRADUATION_YEAR = 2026

os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-Memory Storage

candidates: List[dict] = []
candidate_counter = 1

# Pydantic Response Model

class CandidateResponse(BaseModel):
    id: int
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education: str
    graduation_year: int
    experience_years: float
    skills: List[str]
    resume_file: str

# Utility Functions

def validate_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOC, DOCX allowed.")
    return extension


def save_file(file: UploadFile, file_id: int, extension: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{extension}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def find_candidate(candidate_id: int):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate
    return None

# Routes

@app.get("/health", status_code=200)
def health():
    return {"status": "healthy"}


@app.post("/candidates", response_model=CandidateResponse, status_code=201)
async def upload_candidate(
    full_name: str = Form(..., min_length=2),
    dob: date = Form(...),  # Swagger automatically shows date picker
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(...),
    experience_years: float = Form(..., ge=0),
    skills: str = Form(...),
    resume: UploadFile = File(...)
):
    global candidate_counter

    # Validate DOB (must be in the past)
    today = date.today()
    if dob >= today:
        raise HTTPException(status_code=400, detail="DOB must be in the past")

    # Validate Graduation Year
    if graduation_year > MAX_GRADUATION_YEAR:
        raise HTTPException(
            status_code=400,
            detail=f"Graduation year cannot be greater than {MAX_GRADUATION_YEAR}"
        )

    # Validate File
    extension = validate_file(resume)
    file_path = save_file(resume, candidate_counter, extension)

    candidate = {
        "id": candidate_counter,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education": education,
        "graduation_year": graduation_year,
        "experience_years": experience_years,
        "skills": [skill.strip() for skill in skills.split(",")],
        "resume_file": file_path
    }

    candidates.append(candidate)
    candidate_counter += 1

    return candidate


@app.get("/candidates", response_model=List[CandidateResponse])
def list_candidates(
    skill: Optional[str] = Query(None),
    min_experience: Optional[float] = Query(None),
    graduation_year: Optional[int] = Query(None)
):
    results = candidates.copy()

    if skill:
        results = [
            c for c in results
            if skill.lower() in [s.lower() for s in c["skills"]]
        ]

    if min_experience is not None:
        results = [
            c for c in results
            if c["experience_years"] >= min_experience
        ]

    if graduation_year:
        results = [
            c for c in results
            if c["graduation_year"] == graduation_year
        ]

    return results


@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int):
    candidate = find_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.delete("/candidates/{candidate_id}", status_code=200)
def delete_candidate(candidate_id: int):
    global candidates

    candidate = find_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    if os.path.exists(candidate["resume_file"]):
        os.remove(candidate["resume_file"])

    candidates = [c for c in candidates if c["id"] != candidate_id]

    return {"message": "Candidate deleted successfully"}
