from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()  

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3  )
