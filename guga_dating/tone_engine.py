import json
import urllib.request
import os

GEMINI_API_KEY = "API"
# Try this first
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"
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

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                GEMINI_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(10)
            else:
                raise