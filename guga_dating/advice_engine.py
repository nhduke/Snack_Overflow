import json
import urllib.request
import os
import time

GEMINI_API_KEY = "AIzaSyAlnOVZAEhob0DIwZliXU9f_SpEkp1edSc"
# Try this first
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"

def analyze_dimensions(answers):
    return answers

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