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
import time
import asyncio

# --- MOCK FUNCTIONS (for testing purposes) ---
# In your actual project, these will be your real chain functions.
# This makes the code runnable for demonstration.
def run_jd_match_chain(resume_text, jd):
    return "JD Match: Analysis complete."
def run_grammar_chain(resume_text):
    return "Grammar: Analysis complete. (mock)"
def run_keyword_chain(resume_text, jd):
    return "Keywords: Analysis complete. (mock)"
def run_skill_gap_chain(resume_text, jd):
    return "Skill Gap: Analysis complete. (mock)"
def get_final_score_from_outputs(outputs):
    return {"final_score": 85}
def run_suggestion_chain(resume_text, summary):
    return "Suggestions: Analysis complete. (mock)"
def run_resuem_Check_chain(resume_text):
    return {"isresume": True}
def run_format_chain(resume_text):
    return "Format: Analysis complete. (mock)"
def extract_resume_text(file_path):
    # In a real scenario, this would extract text from a PDF/DOCX.
    # For this example, we'll just return the path as a placeholder.
    return f"Extracted text from {os.path.basename(file_path)}. (mock)"
def run_chain_with_logging(chain_func, *args, **kwargs):
    # This is a simplified version of your logging wrapper.
    # It just calls the function.
    if "chain_name" in kwargs:
        del kwargs["chain_name"] # Remove chain_name as mock functions don't accept it
    return chain_func(*args, **kwargs)

# --- YOUR ORIGINAL ASYNC FUNCTION ---

async def analyze_resume(resume_file, jd):
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
        time.sleep(1) # Reduced sleep time for faster testing
        jd_result = run_chain_with_logging(run_jd_match_chain, resume_text, jd, chain_name="JD Match Chain")

        print("▶ Running Grammar Chain")
        time.sleep(1)
        grammar_result = run_chain_with_logging(run_grammar_chain, resume_text, chain_name="Grammar Chain")

        print("▶ Running Keyword Density Chain")
        time.sleep(1)
        keyword_result = run_chain_with_logging(run_keyword_chain, resume_text, jd, chain_name="Keyword Density Chain")

        print("▶ Running Skill Gap Chain")
        time.sleep(1)
        skill_result = run_chain_with_logging(run_skill_gap_chain, resume_text, jd, chain_name="Skill Gap Chain")

        print("▶ Running Format Check Chain")
        time.sleep(1)
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
        time.sleep(1)
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

# --- HELPER CLASS AND SCRIPT EXECUTION CODE ---

# This helper class simulates the file object your function expects
class MockFile:
    def __init__(self, file_path):
        self.filename = os.path.basename(file_path)
        self._path = file_path

    async def read(self):
        # Create a dummy file if it doesn't exist for the script to run
        if not os.path.exists(self._path):
            with open(self._path, "w") as f:
                f.write("This is a dummy resume file.")
        
        with open(self._path, "rb") as f:
            return f.read()

# Define an async main function to run the logic
async def main():
    # 1. DEFINE YOUR INPUTS
    # IMPORTANT: Replace this with the ACTUAL path to your resume file.
    path = r"C:\Users\polis\OneDrive\Desktop\f_proj\backend\temp\Resume1_g.pdf"
    
    jd="""Required Skills & Qualifications:
    Bachelors degree in Computer Science, Engineering, or a related field (or equivalent experience).
    Strong proficiency in JavaScript and backend technologies (Node.js, Python, Java, etc.).
    Experience with front-end frameworks (React, Angular, Vue.js).
    Solid understanding of databases (SQL and NoSQL).
    Familiarity with version control systems like Git.
    Knowledge of RESTful APIs and microservices architecture.
    Understanding of DevOps practices and cloud platforms (AWS, Azure, GCP) is a plus."""

    # 2. PREPARE AND RUN THE ANALYSIS
    mock_file_to_analyze = MockFile(path)
    
    print("🚀 Starting resume analysis...")
    # Use 'await' to properly call the async function
    result = await analyze_resume(mock_file_to_analyze, jd)
    print("---" * 10)
    print(result)
    print("---" * 10)


# Use asyncio.run() to execute the main async function
if __name__ == "__main__":
    asyncio.run(main())