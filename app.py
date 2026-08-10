import os
import json

from pathlib import Path

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

from retrieval.ask_resume_structured import ask_resume

# ==========================
# CONFIG
# ==========================

BASE_DIR = Path(__file__).parent

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

icon = Image.open(
    BASE_DIR / "images" / "image.png"
)

st.set_page_config(
    page_title="Agentic Resume Coach",
    page_icon=icon,
    layout="wide"
)
# ==========================
# HEADER
# ==========================

col1, col2 = st.columns([1, 6])

with col1:
    st.image(icon, width=100)

with col2:
    st.markdown(
        """
        <h1 style='margin-top:20px;'>
        Agentic Resume Coach
        </h1>
        """,
        unsafe_allow_html=True
    )

# ==========================
# TABS
# ==========================

tab1, tab2, tab3 = st.tabs(
    [
        "Resume Chat",
        "Skill Gap Analyzer",
        "Resume Improvement"
    ]
)

# ==================================================
# TAB 1 : RESUME CHAT
# ==================================================

with tab1:

    st.header("Resume Chat")

    question = st.text_input(
        "Ask anything about the resume"
    )

    if st.button("Ask Resume"):

        if question:

            answer = ask_resume(question)

            st.success(answer)

# ==================================================
# TAB 2 : SKILL GAP ANALYZER
# ==================================================

with tab2:

    st.header("Skill Gap Analyzer")

    jd = st.text_area(
        "Paste Job Description",
        height=250
    )

    if st.button("Analyze Skills"):

        with open(
            BASE_DIR / "jobs" / "resume_skills.json",
            "r",
            encoding="utf-8"
        ) as f:

            resume = json.load(f)

        resume_skills = set(
            skill.lower()
            for skill in resume["skills"]
        )

        keywords = [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Docker",
            "AWS",
            "LangChain",
            "RAG",
            "Vector Databases",
            "Git",
            "GitHub"
        ]

        jd_skills = []

        for skill in keywords:

            if skill.lower() in jd.lower():

                jd_skills.append(skill.lower())

        matched = resume_skills.intersection(jd_skills)

        missing = set(jd_skills) - resume_skills

        score = (
            len(matched) / len(jd_skills) * 100
            if jd_skills
            else 0
        )

        st.metric(
            "Match Score",
            f"{score:.1f}%"
        )

        st.subheader("Matched Skills")

        for skill in matched:
            st.success(f"✓ {skill}")

        st.subheader("Missing Skills")

        for skill in missing:
            st.error(f"✗ {skill}")

# ==================================================
# TAB 3 : RESUME IMPROVEMENT AGENT
# ==================================================

with tab3:

    st.header("Resume Improvement Agent")

    jd = st.text_area(
        "Paste Target Job Description",
        height=250,
        key="improve_jd"
    )

    if st.button("Improve Resume"):

        import json

        with open(
            BASE_DIR / "data" / "structured_resume.json",
            "r",
            encoding="utf-8"
        ) as f:

            resume_data = json.load(f)

        resume_text = "\n\n".join(
            section["text"]
            for section in resume_data
        )

        prompt = f"""
You are a professional ATS Resume Reviewer.

Resume:
{resume_text}

Target Job Description:
{jd}

Provide:

1. ATS Score (/100)
2. Missing Keywords
3. Resume Weaknesses
4. Suggested Improvements
5. Rewritten Resume Bullet Points
6. Final Hiring Recommendation
"""

        with st.spinner("Analyzing Resume..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        st.markdown(response.text)