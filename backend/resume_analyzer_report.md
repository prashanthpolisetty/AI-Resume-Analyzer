# Resume Analyzer Project - Final Design Report

## 🎯 Project Goal

To build an AI-powered Resume Analyzer using LangChain that evaluates resumes (PDF/DOCX) against job descriptions (JD) and generates an ATS (Applicant Tracking System) score along with suggestions for improvement.

---

## ✅ Key Features

1. **JD Match** (25 points)
   - Match resume content with keywords/skills from JD.
2. **Experience Evaluation** (15 points)
   - Analyze years and relevance of experience.
3. **Skill Gap Detection** (20 points)
   - Identify missing skills based on JD.
4. **Grammar Check** (10 points)
   - Check for spelling and grammar issues.
5. **Keyword Density** (15 points)
   - Evaluate how well the resume reflects key JD terms.
6. **Suggestions for Improvement** (No score, but important)
   - Tailored suggestions to enhance resume quality.
7. **Final ATS Score** (100-point scale)
   - Calculated from the weighted results above.

---

## 🧱 Project Folder Structure

```
resume_analyzer/
├── app.py                         # Main runner
├── .env                           # API key config
├── requirements.txt               # Python packages
│
├── prompts/                       # LangChain prompt templates
│   ├── jd_match.txt
│   ├── experience.txt
│   ├── keyword_density.txt
│   ├── grammar.txt
│   ├── skill_gap.txt
│   └── improvement.txt
│
├── chains/                        # LangChain chains for each feature
│   ├── jd_match_chain.py
│   ├── experience_chain.py
│   ├── keyword_chain.py
│   ├── grammar_chain.py
│   ├── skill_gap_chain.py
│   ├── final_score_chain.py
│   └── suggestion_chain.py
│
├── utils/                         # Helper utilities
│   ├── file_loader.py            # Extract PDF/DOCX text
│   ├── score_utils.py            # Score combining logic
│   ├── save_outputs.py           # Generate combined report string
│   └── chain_logger.py           # Log status of each chain execution
│
├── output/                        # Generated results per resume
│   └── [resume_name]/            # Folder per resume
│       ├── ats_score.txt
│       ├── suggestions.txt
│       ├── jd_match_result.txt
│       ├── experience_result.txt
│       ├── keyword_density_result.txt
│       ├── grammar_result.txt
│       ├── skill_gap_result.txt
│       └── full_report.txt
│
└── README.md                      # Project setup and usage
```

---

## 🔄 Workflow (Flow Diagram in Words)

1. **Resume Upload** →
2. **Text Extraction** from PDF/DOCX using `file_loader.py` →
3. **Each Chain Executes** with relevant prompts and inputs →
4. **Individual Scores Returned** (JD match, grammar, etc.) →
5. **Score Combination** using `score_utils.py` →
6. **Improvement Suggestions** generated via `suggestion_chain.py` →
7. **Combined Report** returned via `generate_output_report()` →
8. **(Optional)** Save results to `output/` folder per resume.

---

## 🧠 LangChain Concepts Used (Per Chain)

- `PromptTemplate` → For reusable prompts (in `/prompts/*.txt`)
- `LLMChain` → Each feature has its own chain
- `SimpleSequentialChain` → Used if chaining outputs together (e.g., grammar → suggestion)
- `OpenAI/ChatOpenAI` → Underlying LLM provider
- `load_tools()` → Optional if using integrations like grammar check via external APIs

---

## 📤 Output Format (Frontend-Ready)

- Returned as a **JSON** object from backend
- Can also use \`\` to get combined report in plain text

```json
{
  "ats_score": "82/100",
  "jd_match": "21/25",
  "experience": "13/15",
  "keyword_density": "14/15",
  "grammar": {
    "score": "8/10",
    "issues": ["Replace 'Teh' with 'The'"]
  },
  "skill_gap": {
    "score": "10/10",
    "missing": []
  },
  "suggestions": [
    "Improve grammar in summary.",
    "Add measurable job impact.",
    "Mention leadership in experience."
  ]
}
```

---

## 🔔 Chain Execution Logging (Terminal Status)

To track progress of each chain in terminal (CMD), wrap each chain execution with:

```python
def run_chain_with_logging(chain, inputs, chain_name):
    print(f"▶️ Running {chain_name}...")

    try:
        result = chain.run(inputs)
        print(f"✅ {chain_name} completed successfully.\n")
        return result
    except Exception as e:
        print(f"❌ {chain_name} failed: {str(e)}\n")
        return f"Error in {chain_name}: {str(e)}"
```

Use it like:

```python
jd_result = run_chain_with_logging(jd_chain, inputs, "JD Match Chain")
grammar_result = run_chain_with_logging(grammar_chain, resume_text, "Grammar Chain")
```

This helps track chain execution clearly for debugging and development.

---

## ✅ Next Steps

- Write chains based on prompt templates.
- Call each chain in `app.py` and collect their outputs.
- Format and return results as a combined string or JSON.
- Add chain status tracking using logging utility.
- Optionally integrate with frontend (e.g., Streamlit, React).

Let me know when you're ready to start coding each chain!

## Run Backend
python -m uvicorn app:app --reload



 


