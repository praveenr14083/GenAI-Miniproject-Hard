import streamlit as st
from groq import Groq
from config import GROQ_API_KEY
from prompts import (
    learning_material_prompt,
    practice_questions_prompt,
    translation_prompt,
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI-Powered Learning Platform", layout="wide")

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=GROQ_API_KEY)


# ---------------- AI FUNCTION ----------------
def generate_ai_content(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=800,
    )
    return response.choices[0].message.content


# ---------------- UI ----------------
st.title("📘 AI-Powered Learning Platform")
st.write("Learn any topic with AI-generated material and practice questions.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📌 Topic Input")

topic = st.sidebar.text_input(
    "Enter Topic / Chapter", placeholder="Eg: Operating System - Deadlock"
)

language = st.sidebar.selectbox("Select Language", ["English", "Tamil", "Hindi"])

generate_btn = st.sidebar.button("🚀 Generate")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["📚 Learning Material", "📝 Practice Tasks"])

if generate_btn:
    if not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("Generating content using AI..."):

            # Learning material
            learning_prompt = learning_material_prompt(topic)
            learning_content = generate_ai_content(learning_prompt)

            # Practice questions
            task_prompt = practice_questions_prompt(topic)
            practice_content = generate_ai_content(task_prompt)

            # Translation
            if language != "English":
                learning_content = generate_ai_content(
                    translation_prompt(language, learning_content)
                )
                practice_content = generate_ai_content(
                    translation_prompt(language, practice_content)
                )

        # ---------------- DISPLAY ----------------
        with tab1:
            st.subheader("📘 Learning Material")
            st.write(learning_content)

        with tab2:
            st.subheader("📝 Practice Questions")
            st.write(practice_content)
