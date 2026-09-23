# Frontend

This directory contains the Vite + React frontend for the Student Resume Analyzer.

## Run

```bash
npm install
cp .env.example .env
npm run dev
```

The frontend expects the API at `http://localhost:8000` by default. Set `VITE_API_URL` in `.env` to use another backend URL.

The UI includes targeted and general analysis modes, saved-report history, score visualization, ATS text checking, project bullet boosting, skill proof validation, buzzword detection, and responsive layouts for mobile screens.
