def learning_material_prompt(topic: str) -> str:
    return f"""
You are an expert instructor and curriculum designer.

Generate a COMPLETE and DETAILED SYLLABUS for the topic:
"{topic}"

Target length:
- Around 1000 words (not less than 900, not more than 1100)

Structure the syllabus clearly using numbered headings and subtopics.

Required Syllabus Structure:

1. Introduction to the Topic
   - What the topic is
   - Why it is important
   - Where it is used

2. Prerequisites
   - Required background knowledge
   - Tools or technologies needed

3. Core Fundamentals
   - Basic concepts
   - Terminologies
   - Core principles

4. Intermediate Concepts
   - Key components
   - Internal working
   - Common patterns or methods

5. Advanced Concepts
   - Complex topics
   - Optimization techniques
   - Best practices

6. Practical Implementation
   - Step-by-step workflow
   - Common use cases
   - Hands-on examples (conceptual, no code unless necessary)

7. Tools and Ecosystem
   - Related libraries, frameworks, or tools
   - Industry-standard practices

8. Common Mistakes and Pitfalls
   - Beginner mistakes
   - Performance or design issues

9. Real-World Applications
   - Industry use cases
   - Case-study-style explanations

10. Career and Learning Path
    - Roles that use this topic
    - How it fits into a professional roadmap

11. Summary and Key Takeaways
    - Bullet-point recap of the entire syllabus

Rules:
- Use clear headings
- Use bullet points wherever possible
- Each section must be well-detailed (not shallow)
- Avoid long paragraphs (max 3–4 lines)
- No unnecessary filler content
- Output must be plain text (no markdown, no code blocks)
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
