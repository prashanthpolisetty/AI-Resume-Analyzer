# Student Resume Analyzer - Human-Friendly To‑Do

This file describes, in plain language, what still needs to be built for the resume analyzer project.
Anyone on the team should be able to read it and understand the work ahead, not just the original author.

---

## 1. Backend Improvements (the engine that does the work)

These tasks enhance the core logic that processes resumes and job descriptions.

### a. Make the tool work without a job description

- Update the `suggestion_chain.py` prompt so it does not crash or give meaningless advice when the user skips the job description.
- Adjust the score-calculation in `final_score_chain.py` so it always produces a number between 0 and 100, whether or not a description was supplied.

### b. Add an "ATS Reality Check" debugging helper

- Build a new HTTP route (`/debug-text`) that returns the plain text extracted from the uploaded PDF or Word file.
- Later we will add a simple page on the website that shows the raw text next to the original document so students can see what the automated parser actually read.

---

## 2. Features that help students directly

These are user-facing capabilities designed to make resumes stronger.

### a. Project description booster

- Write a new processing module called `project_booster_chain.py`.
- The module should take a short description (or a link) of a school/project and return bullet points written in the STAR (Situation, Task, Action, Result) format.
- Expose this functionality via a `/boost-project` API endpoint so the frontend can call it.

### b. Skill‑to‑proof checker

- Create `skill_validator_chain.py` which:
  1. Reads the list of skills the student claims.
  2. Searches the rest of the resume (experience, projects, etc.) for evidence those skills were used.
  3. Returns a warning list of any skills with no supporting examples.
- Hook this validator into the main `/analyze` workflow so it runs automatically when a resume is submitted.

### c. Buzzword detector

- Compile a short list of overused buzzwords (e.g. "hard worker", "synergy", "team player").
- Either add checks for these words in the existing `grammar_chain` or create a separate `style_chain` that flags them and suggests stronger alternatives.

---

## 3. More advanced ideas (longer‑term)

These involve comparing multiple resumes or tailoring feedback to a specific role.

### a. Compare two versions of a resume

- Add a `/compare` route where the user can upload two files.
- Analyze both files and then compare their scores, sections, and suggestions.
- Return a human‑readable summary of the differences and indicate which version is stronger.

### b. Role‑aware recommendations

- Allow clients to pass `target_role` (e.g. "software engineer") and `experience_level` (e.g. "entry") to `/analyze`.
- Update all of the backend prompts so the advice changes depending on the desired job and level; for example, be more forgiving of gaps for junior applicants.

---

## 4. Frontend work (can wait until the backend is ready)

These bullets describe the user interface pieces we'll need.

- Start a new React or Next.js project for the application UI.
- Build a file‑upload form that has two modes: one where the student also uploads a job description, and one where they just upload their resume.
- Create a page to display the "ATS Reality Check" raw text output alongside the original resume document.

