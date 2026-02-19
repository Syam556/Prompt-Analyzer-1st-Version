def rule_based_score(prompt):
    score = 0
    feedback = []

    if "you are" in prompt.lower():
        score += 10
    else:
        feedback.append("Define a clear role (e.g., 'You are a...')")

    if "format" in prompt.lower():
        score += 10
    else:
        feedback.append("Specify the output format.")

    if len(prompt.split()) > 40:
        score += 10
    else:
        feedback.append("Provide more detailed instructions.")

    if "step" in prompt.lower() or "explain" in prompt.lower():
        score += 10
    else:
        feedback.append("Clarify expected depth of response.")

    return score, feedback
