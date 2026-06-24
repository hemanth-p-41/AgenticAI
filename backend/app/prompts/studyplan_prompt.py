def build_studyplan_prompt(weak_categories: list, recent_scores: list) -> str:
    prompt = (
        f"Create personalized study plans focusing on these weak categories: {', '.join(weak_categories)}.\n"
        f"Recent scores: {recent_scores}.\n"
        "Return structured day-by-day plans for 3, 7, and 30 days. Include topics, practice tasks, and resources. Return JSON only."
    )
    return prompt
