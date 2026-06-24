def build_question_prompt(company: str, role: str, resume_analysis: dict) -> str:
    skills = ', '.join(resume_analysis.get('skills', []))
    projects = ', '.join(resume_analysis.get('projects', []))
    tech = ', '.join(resume_analysis.get('technologies', []))

    prompt = (
        f"You are an interviewer for {company} hiring for {role}.\n"
        f"Resume skills: {skills}\n"
        f"Projects: {projects}\n"
        f"Technologies: {tech}\n"
        "Generate a set of structured interview questions covering: DSA, OOP, DBMS, OS, Projects, and Behavioral areas."
    )
    return prompt
