import os
import json
from pathlib import Path

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

from ingestion.resume_processor import (
    extract_text_from_pdf,
    parse_resume_with_gemini,
    build_in_memory_vector_store,
    query_resume_rag,
    extract_jd_skills_with_gemini,
)

# ==========================
# CONFIG & INITIALIZATION
# ==========================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY is not set. Please check your `.env` file.")
    st.stop()

client = genai.Client(api_key=api_key)

icon_path = BASE_DIR / "images" / "image.png"
icon = Image.open(icon_path) if icon_path.exists() else None

st.set_page_config(
    page_title="Agentic Resume Coach",
    page_icon=icon if icon else "📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .badge-matched {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #16a34a;
        padding: 4px 12px;
        border-radius: 16px;
        margin: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-missing {
        display: inline-block;
        background-color: rgba(239, 68, 68, 0.15);
        color: #dc2626;
        padding: 4px 12px;
        border-radius: 16px;
        margin: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .card-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "resume_loaded" not in st.session_state:
    st.session_state.resume_loaded = False
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = "Candidate"
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "qdrant_client" not in st.session_state:
    st.session_state.qdrant_client = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ==========================
# SIDEBAR: RESUME UPLOADER
# ==========================

with st.sidebar:
    if icon:
        st.image(icon, width=70)
    st.title("📄 Resume Ingestion")
    st.write("Upload any candidate's resume (PDF) to start.")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a resume PDF to parse and index."
    )

    sample_pdf_path = BASE_DIR / "data" / "My_Resume (1).pdf"
    load_sample_btn = False
    if sample_pdf_path.exists() and not st.session_state.resume_loaded:
        if st.button("📁 Load Default Sample Resume"):
            load_sample_btn = True

    # Process new PDF upload or sample
    if uploaded_pdf is not None and st.session_state.uploaded_file_name != uploaded_pdf.name:
        with st.spinner("Extracting & Indexing Resume..."):
            pdf_bytes = uploaded_pdf.read()
            raw_text = extract_text_from_pdf(pdf_bytes)
            parsed = parse_resume_with_gemini(raw_text, client)
            qdrant = build_in_memory_vector_store(parsed.get("sections", []), client)

            st.session_state.resume_loaded = True
            st.session_state.resume_text = raw_text
            st.session_state.candidate_name = parsed.get("candidate_name", "Candidate")
            st.session_state.parsed_data = parsed
            st.session_state.qdrant_client = qdrant
            st.session_state.uploaded_file_name = uploaded_pdf.name
            st.session_state.chat_messages = [
                {"role": "assistant", "content": f"Hello! I am {st.session_state.candidate_name}'s AI Resume Coach. Ask me anything about their experience, education, skills, or projects!"}
            ]
            st.success("✅ Resume indexed successfully!")

    elif load_sample_btn:
        with st.spinner("Loading Sample Resume..."):
            with open(sample_pdf_path, "rb") as f:
                pdf_bytes = f.read()
            raw_text = extract_text_from_pdf(pdf_bytes)
            parsed = parse_resume_with_gemini(raw_text, client)
            qdrant = build_in_memory_vector_store(parsed.get("sections", []), client)

            st.session_state.resume_loaded = True
            st.session_state.resume_text = raw_text
            st.session_state.candidate_name = parsed.get("candidate_name", "Nuthan")
            st.session_state.parsed_data = parsed
            st.session_state.qdrant_client = qdrant
            st.session_state.uploaded_file_name = "Sample_Resume.pdf"
            st.session_state.chat_messages = [
                {"role": "assistant", "content": f"Hello! I am {st.session_state.candidate_name}'s AI Resume Coach. Ask me anything about their experience, education, skills, or projects!"}
            ]
            st.success("✅ Sample resume loaded!")

    st.divider()

    if st.session_state.resume_loaded:
        st.markdown(f"### 👤 **{st.session_state.candidate_name}**")
        skills_count = len(st.session_state.parsed_data.get("skills", []))
        sections_count = len(st.session_state.parsed_data.get("sections", []))
        st.caption(f"📁 **File**: `{st.session_state.uploaded_file_name}`")
        st.caption(f"🛠️ **Detected Skills**: {skills_count}")
        st.caption(f"📑 **Indexed Sections**: {sections_count}")

        if st.button("🔄 Reset / Clear Resume"):
            st.session_state.resume_loaded = False
            st.session_state.resume_text = ""
            st.session_state.candidate_name = "Candidate"
            st.session_state.parsed_data = {}
            st.session_state.qdrant_client = None
            st.session_state.chat_messages = []
            st.session_state.uploaded_file_name = None
            st.rerun()

# ==========================
# MAIN CONTENT HEADER
# ==========================

col_logo, col_heading = st.columns([1, 8])
with col_logo:
    if icon:
        st.image(icon, width=85)
with col_heading:
    st.markdown("<h1 class='main-title'>Agentic Resume Coach</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Universal AI Career Assistant • RAG Semantic Search • ATS Optimization</p>", unsafe_allow_html=True)

# Guard against un-uploaded state
if not st.session_state.resume_loaded:
    st.info("👈 **Please upload a resume (PDF) using the sidebar to get started**, or click **'Load Default Sample Resume'**.")
    st.stop()

# ==========================
# TABS
# ==========================

tab1, tab2, tab3 = st.tabs([
    "💬 Resume Chat",
    "📊 Skill Gap Analyzer",
    "🚀 Resume Improvement"
])

# ==================================================
# TAB 1 : RESUME CHAT (RAG)
# ==================================================

with tab1:
    st.header("Resume Chat (RAG Assistant)")
    st.caption("Ask questions about candidate background, publications, project technologies, or academic achievements.")

    # Suggested Prompts
    st.markdown("**Quick Suggestions:**")
    prompt_cols = st.columns(4)
    quick_q = None
    if prompt_cols[0].button("🎓 Education & CGPA"):
        quick_q = "What is the candidate's educational background and CGPA?"
    if prompt_cols[1].button("🛠️ Technical Skills"):
        quick_q = "List all core technical skills and programming languages."
    if prompt_cols[2].button("💻 Key Projects"):
        quick_q = "Summarize the key projects the candidate has built."
    if prompt_cols[3].button("📜 Certifications & Research"):
        quick_q = "What research publications or certifications does the candidate have?"

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Ask anything about the resume...")
    target_query = quick_q if quick_q else user_input

    if target_query:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": target_query})
        with st.chat_message("user"):
            st.markdown(target_query)

        # Generate RAG response
        with st.chat_message("assistant"):
            with st.spinner("Searching resume context..."):
                answer = query_resume_rag(
                    st.session_state.qdrant_client,
                    client,
                    target_query,
                    candidate_name=st.session_state.candidate_name
                )
                st.markdown(answer)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})

# ==================================================
# TAB 2 : SKILL GAP ANALYZER
# ==================================================

with tab2:
    st.header("Skill Gap Analyzer")
    st.write("Compare the candidate's skills against any target Job Description.")

    jd_input = st.text_area(
        "Target Job Description:",
        height=200,
        placeholder="Paste target job requirements and qualifications here...",
        key="gap_jd"
    )

    if st.button("🔍 Analyze Skills", type="primary"):
        if not jd_input.strip():
            st.warning("Please paste a Job Description first.")
        else:
            with st.spinner("Extracting JD requirements and comparing skills..."):
                candidate_skills = [s.strip() for s in st.session_state.parsed_data.get("skills", []) if s.strip()]
                jd_skills = extract_jd_skills_with_gemini(jd_input, client)

                cand_skills_lower = {s.lower(): s for s in candidate_skills}
                jd_skills_lower = {s.lower(): s for s in jd_skills}

                matched_lower = set(cand_skills_lower.keys()).intersection(set(jd_skills_lower.keys()))
                missing_lower = set(jd_skills_lower.keys()) - set(cand_skills_lower.keys())

                matched_skills = [jd_skills_lower[k] for k in matched_lower]
                missing_skills = [jd_skills_lower[k] for k in missing_lower]

                score = (len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0.0

                # Metric Display
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Match Score", f"{score:.1f}%")
                m_col2.metric("Matched Skills", len(matched_skills))
                m_col3.metric("Missing Skills", len(missing_skills))

                st.progress(min(1.0, score / 100.0))

                col_match, col_miss = st.columns(2)
                with col_match:
                    st.subheader("✅ Matched Skills")
                    if matched_skills:
                        html_badges = "".join([f"<span class='badge-matched'>✓ {s}</span>" for s in sorted(matched_skills)])
                        st.markdown(html_badges, unsafe_allow_html=True)
                    else:
                        st.info("No exact matching skills detected.")

                with col_miss:
                    st.subheader("❌ Missing Skills")
                    if missing_skills:
                        html_badges = "".join([f"<span class='badge-missing'>✗ {s}</span>" for s in sorted(missing_skills)])
                        st.markdown(html_badges, unsafe_allow_html=True)
                    else:
                        st.success("All target skills are covered by the resume!")

                # AI Learning Roadmap
                if missing_skills:
                    st.markdown("---")
                    st.subheader("🧭 AI Roadmap & Upskilling Advice")
                    with st.spinner("Generating personalized learning recommendations..."):
                        roadmap_prompt = f"""
You are an expert AI Career Coach.
Candidate Skills: {candidate_skills}
Missing Job Requirements: {missing_skills}

Provide:
1. Fast-track learning roadmap for missing skills (resources/steps).
2. Bridge project recommendation to demonstrate these missing skills.
3. How to position current strengths for this role.
"""
                        roadmap_res = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=roadmap_prompt
                        )
                        st.markdown(roadmap_res.text)

# ==================================================
# TAB 3 : RESUME IMPROVEMENT AGENT (ATS)
# ==================================================

with tab3:
    st.header("ATS Resume Reviewer & Improvement Agent")
    st.write("Get comprehensive ATS scoring, high-impact bullet point rewrites, and keyword recommendations.")

    target_jd = st.text_area(
        "Target Job Description for ATS Optimization:",
        height=220,
        placeholder="Paste target Job Description here...",
        key="ats_jd"
    )

    if st.button("🚀 Analyze & Optimize Resume", type="primary"):
        if not target_jd.strip():
            st.warning("Please paste a target Job Description.")
        else:
            with st.spinner("Evaluating ATS compatibility and rewriting bullet points..."):
                prompt = f"""
You are an elite ATS Resume Reviewer and AI Technical Recruiter.

Resume Text:
{st.session_state.resume_text}

Target Job Description:
{target_jd}

Provide a structured, highly actionable report in Markdown format with the following sections:

## 1. ATS Compatibility Score (out of 100) & Verdict
- Overall Score
- Key Strengths & Alignment

## 2. Critical Missing Keywords
- List essential missing tools, technical frameworks, or domain terminology that should be incorporated.

## 3. Resume Weaknesses & Red Flags
- Specific bullet points or sections that lack quantifiable metrics, clarity, or strong impact verbs.

## 4. Rewritten High-Impact Bullet Points
- Provide 3 to 5 rewritten bullet points using the STAR method (Situation, Task, Action, Result) with quantified achievements (e.g., % improvement, latency reduction, scale).

## 5. Recommended Project / Section Additions
- Suggestions on how to frame existing projects or create a quick targeted side project.

## 6. Final Hiring Recommendation
- Honest hiring verdict (Strong Fit / Moderate Fit / Needs Upskilling) with next steps.
"""
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.markdown(response.text)