def learning_material_prompt(topic: str) -> str:
    return f"""
    Explain the topic "{topic}" in a clear and beginner-friendly way.
    Use:
    - Simple language
    - Bullet points
    - Examples
    """


def practice_questions_prompt(topic: str) -> str:
    return f"""
    Create 5 practice questions based on the topic "{topic}".
    Mix:
    - Conceptual questions
    - Short answer questions
    """


def translation_prompt(language: str, content: str) -> str:
    return f"""
    Translate the following content into {language}.
    Keep it simple and easy to understand.

    Content:
    {content}
    """
