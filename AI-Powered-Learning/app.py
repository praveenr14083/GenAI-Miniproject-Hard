import streamlit as st
from groq import Groq
from config import GROQ_API_KEY
from prompts import (
    learning_material_prompt,
    practice_questions_prompt,
)
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI-Powered Learning Platform", layout="wide")

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=GROQ_API_KEY)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("learning_content", "")
st.session_state.setdefault("translated_learning", "")
st.session_state.setdefault("mcqs", [])


# ---------------- AI FUNCTION ----------------
def generate_ai_content(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=1500,
    )
    return response.choices[0].message.content


# ---------------- SAFE JSON PARSER ----------------
def safe_json_parse(text: str):
    try:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
        return json.loads(text)
    except Exception:
        return None


# ---------------- UI ----------------
st.title("📖 AI-Powered Learning Platform")
st.write("Learn any topic with AI-generated content and MCQ practice.")

# ---------------- SIDEBAR (ONLY TOPIC INPUT) ----------------
st.sidebar.header("🔍 Topic Input")

topic = st.sidebar.text_input(
    "Enter Topic / Chapter",
    placeholder="Eg: Operating System - Deadlock",
)

generate_btn = st.sidebar.button("🚀 Generate", width=300)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["📚 Learning Material", "📝 Practice Questions"])


# ---------------- GENERATE CONTENT ----------------
if generate_btn and topic:
    with st.spinner("Generating AI content..."):

        # -------- Learning Material (ENGLISH ONLY) --------
        learning_raw = generate_ai_content(learning_material_prompt(topic))

        st.session_state.learning_content = learning_raw
        st.session_state.translated_learning = learning_raw  # default English

        # -------- Generate MCQs (ENGLISH ONLY) --------
        mcq_raw = generate_ai_content(practice_questions_prompt(topic))

        parsed = safe_json_parse(mcq_raw)
        if not parsed or "questions" not in parsed:
            st.error("❌ MCQ generation failed. Please click Generate again.")
            st.stop()

        st.session_state.mcqs = parsed["questions"]


# ---------------- LEARNING MATERIAL TAB ----------------
with tab1:
    # 🔹 Language selector ONLY for learning material
    language = st.selectbox(
        "Translate Learning Material to:",
        ["English", "Tamil", "Hindi"],
    )
    st.subheader("📚 Learning Material")

    if st.session_state.learning_content:
        if language == "English":
            st.write(st.session_state.learning_content)
        else:
            if language:
                translated = generate_ai_content(
                    f"Translate this into {language}:\n\n{st.session_state.learning_content}"
                )
                st.session_state.translated_learning = translated

            st.write(st.session_state.translated_learning)

    else:
        st.info("👈 Enter a topic and click Generate.")


# ---------------- PRACTICE QUESTIONS TAB (ENGLISH ONLY) ----------------
with tab2:
    st.subheader("📝 Practice Questions")

    if st.session_state.mcqs:
        user_answers = {}

        for idx, q in enumerate(st.session_state.mcqs):
            st.markdown(f"### Q{idx + 1}. {q['question']}")

            user_answers[idx] = st.radio(
                "Choose your answer:",
                ["A", "B", "C", "D"],
                format_func=lambda x: f"{x}. {q['options'][x]}",
                key=f"q_{idx}",
            )

        if st.button("✅ Submit"):
            score = 0
            st.divider()
            st.subheader("📊 Result & Explanation")

            for idx, q in enumerate(st.session_state.mcqs):
                selected = user_answers[idx]
                correct = q["answer"]

                if selected == correct:
                    score += 1
                    st.success(f"Q{idx + 1}: Correct ✅")
                else:
                    st.error(f"Q{idx + 1}: Incorrect ❌")

                st.write(f"**Correct Answer:** {correct}")
                st.info(f"📘 Explanation: {q['explanation']}")
                st.divider()

            st.subheader(f"🎯 Final Score: {score} / 5")

    else:
        st.info("👈 Generate a topic to start practice.")
