from langchain.prompts import PromptTemplate
from config import llm  # This should be your initialized LLM (e.g., OpenAI or Gemini)

# Load the prompt from file
def load_prompt():
    with open("prompts/Format_check.txt", "r", encoding="utf-8") as file:
        return file.read()

# Create the format checking chain using LangChain 1.0+ style
def get_format_chain():
    prompt_template = PromptTemplate(
        input_variables=["resume"],
        template=load_prompt()
    )
    return prompt_template | llm  # Use RunnableSequence

# Run the chain and return the model's JSON output

def run_format_chain(resume_text):
    chain = get_format_chain()
    result = chain.invoke({"resume": resume_text})

    # Extract content and clean if markdown block is returned
    content = result.content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    return content
