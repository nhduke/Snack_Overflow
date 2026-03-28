import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(r"D:\DEV\Snack_Overflow\guga_dating\secret.env")

client = genai.Client(api_key="GEMINI_API_KEY")

TONE_INSTRUCTIONS = {
    "honest":         "Be direct and balanced. Call out what's real without softening or sharpening.",
    "brutal":         "Be blunt and unsparing. No comfort, no softening. Say what most people wouldn't.",
    "calm":           "Be measured and gentle. Use neutral language. Avoid charged words.",
    "slightly_toxic": "Be sardonic and a little cutting. Point out the uncomfortable irony in the situation.",
}

def style_output(advice, tone):
    instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["honest"])

    prompt = (
        f"Rewrite the following relationship advice in this tone: {instruction}\n"
        "Keep the same core meaning and length. Return only the rewritten advice, no preamble.\n\n"
        f"Advice:\n{advice}"
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            if attempt < 2:
                print(f"Error, retrying... ({e})")
                time.sleep(2)
            else:
                print(f"Failed after 3 attempts: {e}")
                return None