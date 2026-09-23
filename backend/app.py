from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from analyzer import analyze_resume, boost_project, buzzword_report, skill_proof
from database import get_analysis, init_db, list_analyses, save_analysis, score_history
from utils.file_loader import extract_resume_text

app = FastAPI(title="Student Resume Analyzer", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(","),
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class ProjectRequest(BaseModel):
    notes: str = Field(min_length=10, max_length=5000)
    target_role: str | None = Field(default=None, max_length=120)


class SkillProofRequest(BaseModel):
    skills: list[str] = Field(min_length=1, max_length=50)
    resume_text: str = Field(min_length=20, max_length=100000)


class BuzzwordRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=100000)


class ChatRequest(BaseModel):
    resume: str = Field(min_length=20, max_length=100000)
    job_description: str | None = Field(default=None, max_length=30000)
    user_input: str = Field(min_length=1, max_length=2000)
    chat_history: list[dict[str, str]] = Field(default_factory=list, max_length=20)


def _validate_email(email: str) -> str:
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(status_code=422, detail="A valid email address is required.")
    return email.lower().strip()


async def _read_resume(upload: UploadFile) -> tuple[str, str]:
    suffix = Path(upload.filename or "resume.txt").suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(status_code=415, detail="Only PDF, DOCX, and TXT resumes are supported.")
    data = await upload.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume must be smaller than 10 MB.")
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temporary:
        temporary.write(data)
        path = temporary.name
    try:
        text = extract_resume_text(path)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        Path(path).unlink(missing_ok=True)
    if len(text.strip()) < 30:
        raise HTTPException(status_code=422, detail="We could not find enough readable text in that file.")
    return text, Path(upload.filename or "resume").name


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "student-resume-analyzer"}


@app.post("/analyze")
async def analyze(
    resume_file: UploadFile = File(...),
    email: EmailStr = Form(...),
    jd: str = Form(default=""),
    job_title: str = Form(default=""),
) -> dict:
    text, filename = await _read_resume(resume_file)
    report = analyze_resume(text, jd or None, job_title or None)
    report["filename"] = filename
    report["email"] = str(email)
    analysis_id = save_analysis(email=str(email), mode=report["mode"], filename=filename, job_title=job_title or None, score=report["score"], report_json=json.dumps(report))
    report["analysis_id"] = analysis_id
    return report


@app.post("/debug-text")
async def debug_text(resume_file: UploadFile = File(...)) -> dict:
    text, filename = await _read_resume(resume_file)
    return {"filename": filename, "characters": len(text), "text": text}


@app.post("/boost-project")
def project_booster(request: ProjectRequest) -> dict:
    return {"bullets": boost_project(request.notes, request.target_role)}


@app.post("/validate-skills")
def validate_skills(request: SkillProofRequest) -> dict:
    return {"results": skill_proof(request.skills, request.resume_text)}


@app.post("/check-buzzwords")
def check_buzzwords(request: BuzzwordRequest) -> dict:
    return {"matches": buzzword_report(request.resume_text)}


@app.get("/history/{email}")
def history(email: str) -> dict:
    email = _validate_email(email)
    return {"email": email, "analyses": list_analyses(email), "score_history": score_history(email)}


@app.get("/history/{email}/{analysis_id}")
def report_history(email: str, analysis_id: int) -> dict:
    report = get_analysis(analysis_id, _validate_email(email))
    if not report:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return report


@app.post("/interview-chat")
def interview_chat(request: ChatRequest) -> dict:
    focus = "the target role" if request.job_description else "your resume"
    previous = len(request.chat_history)
    question = (
        f"Based on {focus}, tell me about a project where you used one of these skills: "
        f"{', '.join(analyze_resume(request.resume).get('strengths', [])[:4]) or 'a key skill'}.")
    if previous:
        question = "Thanks. Can you quantify the result of that work and explain what you personally owned?"
    return {"message": question, "question_number": previous + 1, "suggested_follow_up": "Use the STAR structure: situation, task, action, result."}
