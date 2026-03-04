from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm  

# Load prompt from text file
def load_prompt():
    with open("prompts/grammar.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create grammar check chain
def get_grammar_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt_template)

# Run grammar chain
def run_grammar_chain(resume_text):
    chain = get_grammar_chain()
    return chain.run({"resume": resume_text})
