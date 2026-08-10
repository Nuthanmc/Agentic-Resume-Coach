# 🚀 Agentic Resume Coach

An AI-powered Resume Intelligence Platform that combines Retrieval-Augmented Generation (RAG), Skill Gap Analysis, and Resume Optimization to help candidates evaluate and improve their resumes against target job descriptions.

---

## 📌 Overview

Agentic Resume Coach is designed to act as an intelligent career assistant by:

- Answering questions about a resume using RAG
- Comparing resumes against job descriptions
- Identifying missing skills and competency gaps
- Generating ATS-focused resume improvement suggestions
- Providing personalized career guidance

The system leverages Gemini LLMs, Qdrant Vector Database, and Streamlit to deliver an interactive experience.

---

## ✨ Features

### 🤖 Resume Chat Assistant

Ask natural language questions about a resume.

Example:

> What blockchain technologies does Nuthan know?

The system retrieves relevant resume sections using semantic search and generates grounded responses using Gemini.

---

### 📊 Skill Gap Analyzer

Compare a resume against a target job description.

Outputs:

- Match Score
- Matched Skills
- Missing Skills
- Career Readiness Insights

Example:

| Metric | Result |
|----------|----------|
| Match Score | 50% |
| Matched Skills | Python, ML, Git |
| Missing Skills | Docker, AWS, LangChain, RAG |

---

### 📝 Resume Improvement Agent

AI-powered ATS reviewer that provides:

- ATS Compatibility Score
- Missing Keywords
- Resume Weaknesses
- Improvement Suggestions
- Optimized Resume Bullet Points
- Hiring Recommendation

---

## 🏗️ System Architecture

```text
Resume PDF
     │
     ▼
Section Extraction
     │
     ▼
Gemini Embeddings
     │
     ▼
Qdrant Vector Database
     │
     ▼
Semantic Retrieval
     │
     ▼
Gemini LLM
     │
     ▼
Resume Chat / Skill Analysis / Resume Improvement
```

---

## 🛠️ Tech Stack

### AI & LLM

- Google Gemini 3.6 Flash
- Gemini Embedding Model

### Vector Database

- Qdrant

### Frontend

- Streamlit

### Backend

- Python

### Libraries

- google-genai
- qdrant-client
- python-dotenv
- PyMuPDF
- Pillow

---

## 📂 Project Structure

```text
Agentic-Resume-Coach/
│
├── app.py
├── requirements.txt
├── README.md
│
├── agents/
│   └── resume_improvement_agent.py
│
├── data/
│   └── structured_resume.json
│
├── images/
│   └── image.png
│
├── ingestion/
│   ├── extract_pdf.py
│   ├── extract_sections.py
│   └── store_structured_resume.py
│
├── retrieval/
│   ├── ask_resume_structured.py
│   ├── embed_resume.py
│   └── search_structured.py
│
├── matching/
│   ├── resume_match.py
│   ├── extract_resume_skills.py
│   ├── extract_jd_skills.py
│   └── skill_gap_analyzer.py
│
└── scripts/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Agentic-Resume-Coach.git
cd Agentic-Resume-Coach
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## 🎯 Future Enhancements

- Multi-resume comparison
- Resume ranking system
- Job recommendation engine
- LinkedIn profile analysis
- Resume PDF export
- Cloud deployment with authentication
- Multi-agent orchestration

---

## 👨‍💻 Author

**Nuthan M C**

MCA (Artificial Intelligence & Data Science)  
S-VYASA Deemed to be University

### Areas of Interest

- Artificial Intelligence
- Machine Learning
- Generative AI
- RAG Systems
- Vector Databases
- AI Agents

---

## 📜 License

This project is intended for educational, research, and portfolio purposes.
