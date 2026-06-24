def build_evaluation_prompt(question_text: str, answer_text: str, resume_analysis: dict) -> str:
    """Constructs a strict JSON-returning evaluation prompt.

    The model must return JSON only with the following fields:
    - score: integer 0-10
    - strengths: list of strings
    - weaknesses: list of strings
    - suggestions: list of strings
    - ideal_answer: string
    - category: one of [DSA,OOP,DBMS,OS,AI_ML,PROJECTS,BEHAVIORAL]
    """
    skills = ', '.join(resume_analysis.get('skills', []))
    projects = ', '.join(resume_analysis.get('projects', []))
    prompt = (
        "You are an expert interviewer and evaluator.\n"
        f"Question: {question_text}\n"
        f"Candidate answer: {answer_text}\n"
        f"Resume analysis: skills: {skills}; projects: {projects}\n"
        "Evaluate the answer on: Technical Accuracy, Depth, Clarity, Communication, Completeness.\n"
        "Return JSON ONLY with the fields: score (0-10), strengths (list), weaknesses (list), suggestions (list), ideal_answer (string), category (one of DSA,OOP,DBMS,OS,AI_ML,PROJECTS,BEHAVIORAL)."
    )
    return prompt
