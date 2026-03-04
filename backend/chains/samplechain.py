#This chain is not a part of project only use for testing.
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp")

import os
import fitz  
import docx  

file_path = r"C:\Users\polis\OneDrive\Desktop\f_proj\backend\Android_Development_Roadmap_Report.pdf"

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_docx(file_path):
    from docx import Document
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_resume_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")



jd = """Position: Full Stack Developer (React.js, Node.js, MongoDB)
Location: Gurgaon / Remote
Experience: 6 months to 1.5 years (including internship or project-based experience)

🛠️ Responsibilities:
Design and develop scalable full-stack web applications using React.js, Node.js, and MongoDB.

Collaborate with UI/UX designers to implement user-friendly interfaces with Tailwind CSS and Bootstrap.

Integrate authentication and user management systems using JWT, Express.js, and REST APIs.

Work on routing and view management using React Router or Next.js Navigation.

Maintain clean, modular code with an emphasis on performance, reusability, and security.

Optimize backend APIs and frontend interactions for seamless user experience.

Contribute to both development and testing phases of product delivery lifecycle.

✅ Requirements:
Strong foundation in JavaScript, HTML, and CSS.

Proficiency in React.js, Redux, and Next.js for frontend development.

Hands-on backend experience with Node.js, Express.js, MongoDB, and Mongoose.

Experience in JWT-based authentication, RESTful APIs, and MVC architecture.

Familiarity with version control tools like GitHub.

Good understanding of DSA, OOPs, and DBMS concepts.

Passionate about full-stack development and continuous learning.

Ability to work independently or in a team and deliver within deadlines.

💡 Preferred Qualifications:
Prior internship experience (e.g., EY or similar) in frontend or full-stack development.

Strong problem-solving skills (e.g., Codeforces, Leetcode participation).

Portfolio or GitHub projects (e.g., Capwizard, Weather App, URL Shortener).

Open-source contributions or community involvement.

🔗 Tools & Tech Stack:
React.js, Next.js, Node.js, Express.js, MongoDB, Mongoose, Tailwind CSS, Redux, JWT, GitHub, REST APIs"""
resume = extract_resume_text(file_path)

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are a resume screening assistant.

Your task is to compare the resume against the job description and identify:
- Important keywords and phrases that appear in both
- Keywords that are missing but should be present
- The overall strength of keyword alignment

Guidelines:
- Focus ONLY on keyword match/mismatch
- Do NOT hallucinate content or scores
- Score should reflect how many important keywords from JD are found in the resume
- Each insight must be a one-line reason
- Respond in JSON format as shown below
- If fewer insights, return only those — no need to pad

-give only the 2 Insights.Not more than 2 .

Return your response in this exact JSON format:
{{
    "Score": "10/15",
    "Insights": [
        "React.js, Node.js, and MongoDB found in resume - good match",
        "Missing Tailwind CSS, JWT, or Express.js - weak backend exposure"
    ]
}}

Resume:
{resume}

Job Description (JD):
{jd}
""",
    input_variables=["resume", "jd"]
)






chain = LLMChain(prompt=prompt,llm=llm)

result = chain.invoke({
    "resume": resume,
    "jd": jd

})
print(result["text"])  #
