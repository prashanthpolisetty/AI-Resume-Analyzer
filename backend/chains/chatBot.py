# chatbot.py (LangChain Chain for Interview Chat)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import llm  # Import your LLM instance (Gemini/OpenAI)

def load_prompt():
    with open("prompts/chatBot.txt", "r", encoding="utf-8") as f:
        return f.read()

def get_chatbot_chain():
    prompt = PromptTemplate(
        input_variables=["resume", "jd", "chat_history", "user_input"],
        template=load_prompt()
    )
    return LLMChain(llm=llm, prompt=prompt)

def run_interview_chat(resume, jd, chat_history, user_input):
    chain = get_chatbot_chain()
    result = chain.run({
        "resume": resume,
        "jd": jd,
        "chat_history": chat_history,
        "user_input": user_input
    })
    return result
