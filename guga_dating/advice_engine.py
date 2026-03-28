def analyze_dimensions(answers):

    combined = " ".join(answers.values()).lower()

    scores = {
        "effort": 0,
        "clarity": 0,
        "consistency": 0,
        "emotional_safety": 0,
        "intent": 0
    }

    # Effort
    if "i text first" in combined or "always me" in combined:
        scores["effort"] -= 2

    if "they start conversation" in combined:
        scores["effort"] += 2

    # Clarity
    if "unclear" in combined or "mixed" in combined:
        scores["clarity"] -= 2

    if "clear" in combined or "direct" in combined:
        scores["clarity"] += 2

    # Consistency
    if "sometimes" in combined or "random" in combined:
        scores["consistency"] -= 2

    if "consistent" in combined:
        scores["consistency"] += 2

    # Emotional safety
    if "afraid" in combined or "cannot talk" in combined:
        scores["emotional_safety"] -= 2

    if "comfortable" in combined:
        scores["emotional_safety"] += 2

    # Intent
    if "avoid plans" in combined:
        scores["intent"] -= 2

    if "future plans" in combined:
        scores["intent"] += 2

    return scores


def generate_advice(scores):

    advice_parts = []

    # Effort
    if scores["effort"] < 0:
        advice_parts.append(
            "The effort currently looks uneven. One person appears to be carrying more of the interaction."
        )

    elif scores["effort"] > 0:
        advice_parts.append(
            "There appears to be mutual effort in maintaining contact."
        )

    # Clarity
    if scores["clarity"] < 0:
        advice_parts.append(
            "The communication pattern suggests uncertainty or mixed signaling."
        )

    elif scores["clarity"] > 0:
        advice_parts.append(
            "The communication seems relatively direct."
        )

    # Consistency
    if scores["consistency"] < 0:
        advice_parts.append(
            "Inconsistency often creates emotional confusion because positive moments become difficult to interpret."
        )

    # Emotional Safety
    if scores["emotional_safety"] < 0:
        advice_parts.append(
            "If speaking honestly feels risky, that usually weakens trust over time."
        )

    # Intent
    if scores["intent"] < 0:
        advice_parts.append(
            "Avoiding concrete plans often signals uncertainty about commitment."
        )

    elif scores["intent"] > 0:
        advice_parts.append(
            "Future-oriented behavior usually indicates stronger relational intent."
        )

    if not advice_parts:
        advice_parts.append(
            "The situation has mixed signals and needs more concrete examples."
        )

    return " ".join(advice_parts)