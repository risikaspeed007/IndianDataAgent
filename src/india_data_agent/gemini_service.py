import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def ask_gemini(question, verified_answer):
    prompt = f"""
You are the India Data Agent.

Answer the user's question using ONLY the verified data below.
Do not change, calculate differently, or invent any numbers.

User question:
{question}

Verified data:
{verified_answer}

Give a short, clear answer.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()