def get_questions(issue):

    base_questions = [
        "What happened?",
        "Who usually texts first?",
        "How often do they reply?",
        "What outcome do you want?"
    ]

    if issue == "Conflict":
        base_questions.append("How do arguments usually end?")

    if issue == "Ex":
        base_questions.append("Why did the relationship end?")

    return base_questions