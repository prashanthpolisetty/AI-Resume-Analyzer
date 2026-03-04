from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.file_loader import extract_resume_text
from utils.chain_logger import run_chain_with_logging

# Import all chains
from chains.jd_match_chain import run_jd_match_chain
from chains.grammar_chain import run_grammar_chain
from chains.keyword_chain import run_keyword_chain
from chains.skill_gap_chain import run_skill_gap_chain
from chains.final_score_chain import get_final_score_from_outputs
from chains.suggestion_chain import run_suggestion_chain
from chains.resume_check import run_resuem_Check_chain
from chains.format_chain import run_format_chain
from chains.chatBot import run_interview_chat

import os
import json
import time

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(resume_file: UploadFile, jd: str = Form(...)):
    """
    Accepts a resume file and job description input.
    Runs all analysis chains and returns the ATS score with suggestions.
    """

    # STEP 1: Save uploaded file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, resume_file.filename)

    with open(file_path, "wb") as f:
        f.write(await resume_file.read())

    # STEP 2: Extract text from resume
    resume_text = extract_resume_text(file_path)

    # STEP 3: Resume validation chain
    resume_check = run_chain_with_logging(run_resuem_Check_chain, resume_text, chain_name="Resume Check")

    if isinstance(resume_check, dict):
        if resume_check.get("isresume") is not True:
            return "The uploaded document is not recognized as a resume."
    else:
        return "Resume Check failed. LLM did not return valid response."
    
    try:
        print("▶ Running JD Match Chain")
        time.sleep(3)
        jd_result = run_chain_with_logging(run_jd_match_chain, resume_text, jd, chain_name="JD Match Chain")

        print("▶ Running Grammar Chain")
        time.sleep(3)
        grammar_result = run_chain_with_logging(run_grammar_chain, resume_text, chain_name="Grammar Chain")

        print("▶ Running Keyword Density Chain")
        time.sleep(3)
        keyword_result = run_chain_with_logging(run_keyword_chain, resume_text, jd, chain_name="Keyword Density Chain")

        print("▶ Running Skill Gap Chain")
        time.sleep(3)
        skill_result = run_chain_with_logging(run_skill_gap_chain, resume_text, jd, chain_name="Skill Gap Chain")

        print("▶ Running Format Check Chain")
        time.sleep(3)
        format_result = run_chain_with_logging(run_format_chain, resume_text, chain_name="Format Check Chain")

        # STEP 4: Compute final ATS score
        outputs = {
            "jd_match": jd_result,
            "grammar": grammar_result,
            "keyword_density": keyword_result,
            "skill_gap": skill_result,
        }
        score_data = get_final_score_from_outputs(outputs)

        # STEP 5: Generate improvement suggestions
        print("▶ Running Suggestion Chain")
        time.sleep(3)
        summary_for_suggestions = f"{jd_result}\n\n{grammar_result}\n\n{keyword_result}\n\n{skill_result}"
        suggestions = run_chain_with_logging(run_suggestion_chain, resume_text, summary_for_suggestions, chain_name="Suggestion Chain")

        # STEP 6: Return response as a single string
        suggestion_text = suggestions if isinstance(suggestions, str) else "\n".join(suggestions)
        result_string = (
            f"📄 Resume Analysis Report\n\n"
            f"✔ Final Score: {score_data['final_score']}/100\n\n"
            f"🔍 JD Match:\n{jd_result}\n\n"
            f"📝 Grammar:\n{grammar_result}\n\n"
            f"🔑 Keyword Density:\n{keyword_result}\n\n"
            f"📉 Skill Gap:\n{skill_result}\n\n"
            f"📐 Format Check:\n{format_result}\n\n"
            f"💡 Suggestions:\n{suggestion_text}"
        )
        return result_string.strip()

    except Exception as e:
        return f"Resume analysis failed: {str(e)}"

@app.post("/interview-chat")
async def interview_chat(request: Request):
    body = await request.json()
    resume = body.get("resume")
    jd = body.get("jd")
    chat_history = body.get("chat_history", "")
    user_input = body.get("user_input")

    if not all([resume, jd, user_input]):
        return "Missing input fields."

    try:
        response = run_interview_chat(resume, jd, chat_history, user_input)
        return response
    except Exception as e:
        return f"Interview chat failed: {str(e)}"
