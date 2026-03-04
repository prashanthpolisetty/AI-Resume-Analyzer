from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm

def load_prompt():
    with open("prompts/jd_match.txt", "r", encoding="utf-8") as file:
        return file.read()

def get_jd_match_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume", "jd"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

def run_jd_match_chain(resume_text, jd_text):
    chain = get_jd_match_chain()
    return chain.run({"resume": resume_text, "jd": jd_text})
