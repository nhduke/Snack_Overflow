import json
import time
from google import genai


QUESTION_FRAMEWORK = {
    "Texting": ["communication frequency", "who initiates", "response time", "emotional tone"],
    "Mixed Signals": ["behavioral patterns", "verbal vs. action mismatches", "hot/cold cycles"],
    "Conflict": ["argument triggers", "resolution patterns", "emotional safety", "repair attempts"],
    "Ex": ["breakup reason", "current contact", "unresolved feelings", "what user wants now"],
    "Situationship": ["label avoidance", "exclusivity", "future plans", "emotional investment"],
}

client = genai.Client(api_key="API")


def get_questions(issue):
    dimensions = QUESTION_FRAMEWORK.get(issue, ["general relationship dynamics"])

    prompt = (
        f"You are a relationship analyst. Generate exactly 8 short, direct, non-judgmental questions "
        f"for someone dealing with a '{issue}' dating issue. "
        f"Explore these dimensions: {', '.join(dimensions)}. "
        "Return ONLY a raw JSON array of strings. No markdown, no backticks, no preamble."
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            raw = response.text.strip()

            # Clean markdown if Gemini adds it anyway
            raw = raw.replace("```json", "").replace("```", "").strip()

            questions = json.loads(raw)

            if not isinstance(questions, list):
                raise ValueError("Response is not a JSON array")

            return questions

        except Exception as e:
            if attempt < 2:
                print(f"Error, retrying... ({e})")
                time.sleep(2)
            else:
                print(f"Failed after 3 attempts: {e}")
                return None


# Test it out
# questions = get_questions("Texting")
# print(json.dumps(questions, indent=2))