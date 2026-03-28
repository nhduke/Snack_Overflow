import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), 'secret.env'))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TONE_INSTRUCTIONS = {
    "honest": (
        "You're a brutally self-aware friend who tells it like it is. "
        "No fluff, no therapy-speak. Use casual, real language. "
        "Point out exactly what's happening and why it matters, even if it stings a little."
    ),
    "brutal": (
        "You're roasting this person's situation like a comedian who has zero patience for delusion. "
        "Be savage but specific — mock the behavior, not the person. "
        "Use punchy, cutting sentences. Make them laugh at how obvious the answer is. "
        "No softening, no 'but on the bright side'. End with one hard truth they can't ignore."
    ),
    "calm": (
        "You're a zen therapist who speaks slowly and clearly. "
        "Use gentle, neutral language. No charged words, no drama. "
        "Acknowledge feelings first, then give grounded, measured advice."
    ),
    "slightly_toxic": (
        "You're a sarcastic best friend who loves pointing out the irony in everything. "
        "Be witty and a little cutting — highlight how predictable or self-sabotaging the situation is. "
        "Use dry humor and rhetorical questions. Make them feel slightly called out but also seen."
    ),
}

def style_output(advice, tone):
    instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["honest"])

    prompt = (
        f"Rewrite the following relationship advice with this exact voice and style:\n{instruction}\n\n"
        "Rules:\n"
        "- Keep the same core meaning and approximate length\n"
        "- Sound like a real person talking, not an AI writing an essay\n"
        "- No bullet points, no headers, no preamble\n"
        "- Return only the rewritten advice\n\n"
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