from langchain.prompts import PromptTemplate
from config import llm  # Your OpenAI model instance
import json

# Load the prompt from the prompt file
def load_prompt():
    with open("prompts/resumecheck.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create the resume check chain using new LangChain style
def get_resume_check_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume"],
        template=load_prompt()
    )
    return prompt_template | llm  # modern runnable sequence

# Run the resume check chain
def run_resuem_Check_chain(resume_text):
    chain = get_resume_check_chain()
    output = chain.invoke({"resume": resume_text})  # This is an AIMessage
    print("🔍 RAW OUTPUT from Resume Check Chain:\n", output)

    try:
        # Extract content and remove markdown block if present
        clean_content = output.content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(clean_content)
        return parsed
    except json.JSONDecodeError as e:
        print("❌ JSON decode failed:", e)
        return {"error": "Invalid JSON returned from LLM"}

