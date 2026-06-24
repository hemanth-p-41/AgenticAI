def build_followup_prompt(question_text: str, answer_text: str) -> str:
    return f"Given the question: '{question_text}' and the candidate answer: '{answer_text}', provide a single thoughtful follow-up question to probe depth or clarity." 
