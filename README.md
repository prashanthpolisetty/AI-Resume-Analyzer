# Student Resume Analyzer

A practical resume coaching API for students and early-career applicants. It supports targeted analysis against a job description, a general resume health check, ATS text inspection, project bullet rewriting, skill-proof validation, buzzword detection, score history, and a lightweight mock interview flow.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

The API is available at `http://localhost:8000`; interactive docs are at `/docs`. No LLM key is required for the core analyzer: feedback is deterministic and explainable, which makes it suitable for a first pass. An LLM can be added later for richer rewriting or interview conversations.

## Analysis modes

`POST /analyze` accepts multipart form data:

- `resume_file`: PDF, DOCX, or TXT (maximum 10 MB)
- `email`: used to associate reports with a user
- `jd`: optional job description. Supplying it activates targeted mode; leaving it blank activates general health-check mode.
- `job_title`: optional context for the report

Reports are stored in SQLite (`resume_analyzer.db`, configurable with `RESUME_ANALYZER_DB`). `GET /history/{email}` returns previous reports and score history.

## Helpful tools

- `POST /debug-text` — return the text an ATS-style parser extracts
- `POST /boost-project` — turn rough project notes into three measurable bullet templates
- `POST /validate-skills` — compare claimed skills with evidence in resume text
- `POST /check-buzzwords` — find weak phrases and suggest evidence-based replacements
- `POST /interview-chat` — ask a resume-aware mock interview question
- `GET /health` — health check

Set `CORS_ORIGINS` to a comma-separated list of trusted frontend origins before deployment. This version deliberately does not store uploaded files, only the resulting report and metadata.
