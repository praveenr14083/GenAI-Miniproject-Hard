def learning_material_prompt(topic: str) -> str:
    return f"""
Explain the topic "{topic}" in full detail for a student.

Structure:
1. Definition
2. Key concepts
3. How it works / process
4. Advantages
5. Disadvantages
6. Real-world example
7. Summary points

Rules:
- Use clear headings
- Use bullet points where possible
- Keep each section concise (3–5 bullets max)
- Avoid long paragraphs
- No unnecessary introduction or conclusion
"""


def practice_questions_prompt(topic: str) -> str:
    return f"""
You are an API.

Return ONLY valid JSON.
No markdown.
No extra text.

Format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      }},
      "answer": "A",
      "explanation": "Short explanation"
    }}
  ]
}}

Create EXACTLY 5 MCQs on:
{topic}
"""


def translate_mcq_block_prompt(language: str, mcq: dict) -> str:
    return f"""
Translate the following MCQ into {language}.

Rules:
- Translate only question, options, explanation
- DO NOT change option keys (A, B, C, D)
- DO NOT change answer letter
- Return ONLY valid JSON
- No markdown

MCQ:
{mcq}
"""
