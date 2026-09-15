import os
import json
import re
import time

from dotenv import load_dotenv
from google import genai

from services.vector_store import retrieve_resume_chunks


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )


client = genai.Client(api_key=api_key)


MODEL_NAME = "gemini-3.5-flash-lite"


def parse_json(text):
    

    if not text:
        raise ValueError("Gemini returned an empty response.")

    cleaned = (
        text.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    start = cleaned.find("{")

    if start == -1:
        raise ValueError(
            f"No JSON object found in Gemini response:\n{cleaned}"
        )

    decoder = json.JSONDecoder()

    data, _ = decoder.raw_decode(cleaned[start:])

    if not isinstance(data, dict):
        raise ValueError(
            "Gemini response is not a valid JSON object."
        )

    return data


def normalize_analysis(data):

    try:
        score = float(data.get("overall_score", 0))
    except (TypeError, ValueError):
        score = 0.0

    score = max(0.0, min(100.0, score))

    return {
        "overall_score": round(score, 2),

        "matching_skills":
            data.get("matching_skills") or [],

        "missing_skills":
            data.get("missing_skills") or [],

        "summary":
            str(data.get("summary") or ""),

        "strengths":
            data.get("strengths") or [],

        "weaknesses":
            data.get("weaknesses") or []
    }


def get_retry_seconds(error_message):
   

    match = re.search(
        r"retry in ([0-9.]+)s",
        error_message.lower()
    )

    if match:
        return int(float(match.group(1))) + 2

    return 30


def generate_analysis(prompt, max_retries=2):
   

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            return response.text

        except Exception as error:

            error_message = str(error)

           
            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                wait_seconds = get_retry_seconds(error_message)

                print(
                    f"Gemini quota/rate limit reached. "
                    f"Waiting {wait_seconds} seconds..."
                )

                # Retry only once
                if attempt < max_retries - 1:
                    time.sleep(wait_seconds)
                    continue

                raise RuntimeError(
                    "Gemini API quota is currently exhausted. "
                    "Please wait a few minutes and try again."
                )
            raise error

    raise RuntimeError(
        "Unable to get a response from Gemini."
    )


def analyze_resume(resume_id, job_description):

    chunks = retrieve_resume_chunks(
        resume_id=resume_id,
        query=job_description,
        n_results=10
    )

    if not chunks:
        raise ValueError(
            "No relevant resume chunks were retrieved."
        )


    context = "\n\n".join(

        f"SECTION: {chunk['section']}\n"
        f"{chunk['content']}"

        for chunk in chunks
    )


    prompt = f"""
You are an AI recruitment assistant.

Analyze the candidate resume against the job description.

JOB DESCRIPTION:
{job_description}

RELEVANT RESUME EVIDENCE:
{context}

IMPORTANT RULES:

1. Use only information present in the resume evidence.
2. Do not invent skills, experience or qualifications.
3. Calculate an overall match score from 0 to 100.
4. Compare:
   - technical skills
   - experience
   - projects
   - education
   - technologies
5. matching_skills must contain only skills found in the resume.
6. missing_skills must contain important requirements from the job description
   that are not supported by the resume.
7. Keep the summary concise and professional.
8. Return ONLY valid JSON.
9. Do not include markdown.
10. Do not include explanations outside JSON.

Return exactly this JSON structure:

{{
    "overall_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "summary": "",
    "strengths": [],
    "weaknesses": []
}}
"""

    response_text = generate_analysis(prompt)

    analysis = parse_json(response_text)

    return normalize_analysis(analysis)