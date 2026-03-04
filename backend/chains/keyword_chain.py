from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm  # Shared Gemini LLM

# Load the keyword prompt
def load_prompt():
    with open("prompts/keyword_density.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create keyword match chain
def get_keyword_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume", "jd"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

# Run the keyword chain
def run_keyword_chain(resume_text, jd_text):
    chain = get_keyword_chain()
    return chain.run({"resume": resume_text, "jd": jd_text})
