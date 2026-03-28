import json
import urllib.request
import os

QUESTION_FRAMEWORK = {
    "Texting": ["communication frequency", "who initiates", "response time", "emotional tone"],
    "Mixed Signals": ["behavioral patterns", "verbal vs. action mismatches", "hot/cold cycles"],
    "Conflict": ["argument triggers", "resolution patterns", "emotional safety", "repair attempts"],
    "Ex": ["breakup reason", "current contact", "unresolved feelings", "what user wants now"],
    "Situationship": ["label avoidance", "exclusivity", "future plans", "emotional investment"],
}

GEMINI_API_KEY = "API"
# Try this first
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"

import time

def get_questions(issue):
    dimensions = QUESTION_FRAMEWORK.get(issue, ["general relationship dynamics"])
    prompt = (
        f"You are a relationship analyst. Generate exactly 5 short, direct, non-judgmental questions "
        f"for someone dealing with a '{issue}' dating issue. "
        f"The questions should explore these dimensions: {', '.join(dimensions)}. "
        "Return ONLY a JSON array of 5 question strings. No preamble, no markdown, no backticks."
    )

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    # NO req here, only inside the loop
    def get_questions(issue):
        print(f"DEBUG - issue received: '{issue}'")  # check what's coming in
        
        dimensions = QUESTION_FRAMEWORK.get(issue, ["general relationship dynamics"])
        print(f"DEBUG - dimensions: {dimensions}")  # check dimensions
        
        prompt = (
            f"You are a relationship analyst. Generate exactly 5 short, direct, non-judgmental questions "
            f"for someone dealing with a '{issue}' dating issue. "
            f"The questions should explore these dimensions: {', '.join(dimensions)}. "
            "Return ONLY a JSON array of 5 question strings. No preamble, no markdown, no backticks."
        )
        print(f"DEBUG - prompt: {prompt}")  # check full prompt
        print(f"DEBUG - URL: {GEMINI_URL}")  # check URL has real key not 'secret'

    # rest of the code...
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
                raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                raw = raw.replace("```json", "").replace("```", "").strip()
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(10)
            else:
                # Read the actual error message from Gemini
                error_body = e.read().decode("utf-8")
                print(f"HTTP {e.code} error body: {error_body}")
                raise