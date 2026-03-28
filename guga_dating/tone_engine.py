def style_output(advice, tone):

    tones = {
        "honest": advice,

        "brutal": {
            "You are carrying most of the interaction right now.": "You are doing the work and calling it chemistry.",
            "Their response pattern suggests you are not their current priority.": "If they wanted stronger presence, you would not feel this confused.",
            "Repeated unresolved conflict usually points to deeper incompatibility.": "Same fight, different day usually means the problem is structural.",
            "Look at repeated behavior more than isolated words.": "Patterns do not lie."
        },

        "calm": {
            "You are carrying most of the interaction right now.": "The effort currently appears uneven.",
            "Their response pattern suggests you are not their current priority.": "Their current engagement level appears limited.",
            "Repeated unresolved conflict usually points to deeper incompatibility.": "The conflict pattern suggests unresolved differences.",
            "Look at repeated behavior more than isolated words.": "Long-term patterns matter most."
        },

        "slightly_toxic": {
            "You are carrying most of the interaction right now.": "You are sending energy where little is returning.",
            "Their response pattern suggests you are not their current priority.": "Confusion usually arrives when clarity is absent.",
            "Repeated unresolved conflict usually points to deeper incompatibility.": "Peace should not require constant repair.",
            "Look at repeated behavior more than isolated words.": "Potential is not reality."
        }
    }

    if tone == "honest":
        return advice

    return tones.get(tone, {}).get(advice, advice)