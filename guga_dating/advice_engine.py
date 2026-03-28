import json
import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(r"D:\DEV\Snack_Overflow\guga_dating\secret.env")

client = genai.Client(api_key="GEMINI_API_KEY")

def generate_advice(answers):
    qa_text = "\n".join(f"Q: {q}\nA: {a}" for q, a in answers.items())

    prompt = (
        "You are a sharp, insightful relationship advisor. "
        "Analyze the following Q&A from someone dealing with a dating situation. "
        "Identify patterns across five dimensions: effort balance, communication clarity, "
        "consistency, emotional safety, and intent/commitment signals. "
        "Give 3-5 sentences of concrete, specific advice based only on what they shared. "
        "Do not be vague. Do not moralize. Speak directly to their situation.\n\n"
        f"{qa_text}"
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()  # plain text, no json.loads needed

        except Exception as e:
            if attempt < 2:
                print(f"Error, retrying... ({e})")
                time.sleep(2)
            else:
                print(f"Failed after 3 attempts: {e}")
                return None