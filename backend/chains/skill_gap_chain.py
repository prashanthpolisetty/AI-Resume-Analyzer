from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm  # Reused Gemini LLM

# Load the skill gap prompt
def load_prompt():
    with open("prompts/skill_gap.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create the Skill Gap Chain
def get_skill_gap_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume", "jd"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

# Run the skill gap chain
def run_skill_gap_chain(resume_text, jd_text):
    chain = get_skill_gap_chain()
    return chain.run({"resume": resume_text, "jd": jd_text})
