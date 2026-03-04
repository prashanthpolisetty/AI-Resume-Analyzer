from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm

# Load the prompt from file
def load_prompt():
    with open("prompts/improvement.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create the suggestion chain
def get_suggestion_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume", "summary"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

# Run the chain
def run_suggestion_chain(resume_text, analysis_summary):
    chain = get_suggestion_chain()
    return chain.run({"resume": resume_text, "summary": analysis_summary})
