import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
)
def analyse_resume_gemini(resume_content, job_description):
    prompt = f"""
    You are a professional resume analyzer.
    Resume:
    {resume_content}
    Job Description:
    {job_description}
    Task:
    - Analyze the resume against the job description.
    - Give a match score out of 100.
    - Highlight missing skills or experiences .
    - Suggest  only 2 main improvements.
    -summary in 2 to 3 lines

    Return the result in structured format:
    Match Score: XX/100
    Missing Skills:
    - ...
    Suggestions:
    - ...
    Summary:
    ...
    """
    response = model.generate_content(prompt)
    return response.text

