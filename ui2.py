import os
import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import tempfile
from scorer import score_resume
from rag_agent import analyze_resume_with_rag
from pdf_generator_feedback import save_feedback_pdf

# === Helper: Generate persona prompt for RAG ===
def generate_persona_prompt(role):
    return f"""
You are a resume evaluation assistant for a hiring manager looking to fill the role of {role}.
Provide constructive, detailed feedback for the candidate on how they can better tailor their resume to this role.
Focus on:
- Relevant technical and soft skills
- Achievements or metrics
- Missing keywords
- Alignment with role expectations
"""

# === Helper: Extract text from uploaded files ===
def extract_text(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            with fitz.open(tmp_path) as doc:
                return "\n".join([page.get_text() for page in doc])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            return docx2txt.process(tmp_path)
        elif uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Text extraction error: {e}")
    return None

# === Page Setup ===
st.set_page_config(page_title="Resume Analyzer & Ranker", layout="wide")
st.title("Resume Analyzer, Ranker & Feedback Generator")

# === Tabs ===
tab1, tab2, tab3 = st.tabs(["Single Resume Analysis", "Free-Form RAG Q&A", "Batch Resume Ranking"])

# === Tab 1: Single Resume Analysis ===
with tab1:
    st.header("Upload Resume & JD for Role-Based Feedback")

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], key="resume_single")
    with col2:
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"], key="jd_single")

    if resume_file and jd_file:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text(resume_file)
            jd_text = extract_text(jd_file)

            if resume_text and jd_text:
                role = jd_file.name.split(".")[0] or "this role"
                persona_prompt = generate_persona_prompt(role)

                score, matched_skills = score_resume(resume_text, jd_text)
                feedback = analyze_resume_with_rag(resume_text, persona_prompt)

                st.subheader("Match Score")
                st.metric("Score", f"{score:.2f} / 1.0")

                st.subheader("Matched Skills")
                st.write(matched_skills or "No relevant skills matched.")

                st.subheader("AI Feedback")
                st.write(feedback)

                resume_name = resume_file.name.split(".")[0]
                save_feedback_pdf(resume_name, feedback)

                with open(f"pdf_feedback/{resume_name}_feedback.pdf", "rb") as f:
                    st.download_button("Download Feedback PDF", f, file_name=f"{resume_name}_feedback.pdf")
            else:
                st.error("Text extraction failed from one of the files.")

# === Tab 2: Free-Form RAG Q&A ===
with tab2:
    st.header("Ask AI About Any Resume (No JD Required)")

    resume_file = st.file_uploader("Upload Resume for Query", type=["pdf", "docx", "txt"], key="resume_qna")
    query = st.text_input("Ask a question (e.g., What are the candidate's strengths?)")

    if resume_file and query:
        resume_text = extract_text(resume_file)
        if resume_text:
            with st.spinner("Generating AI response..."):
                rag_response = analyze_resume_with_rag(resume_text, query)
                st.subheader("AI Response")
                st.write(rag_response)
        else:
            st.error("Failed to extract text from the resume.")

# === Tab 3: Batch Resume Ranking ===
with tab3:
    st.header("Batch Ranking of Multiple Resumes Against a Single JD")

    uploaded_resumes = st.file_uploader("Upload Resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    uploaded_jd = st.file_uploader("Upload JD File", type=["pdf", "docx", "txt"], key="jd_batch")

    if uploaded_resumes and uploaded_jd and st.button("Start Batch Ranking"):
        with st.spinner("Processing resumes..."):
            jd_text = extract_text(uploaded_jd)
            role = uploaded_jd.name.split(".")[0] or "this role"
            persona_prompt = generate_persona_prompt(role)

            batch_results = []
            for resume_file in uploaded_resumes:
                resume_text = extract_text(resume_file)
                if not resume_text:
                    continue

                score, matched_skills = score_resume(resume_text, jd_text)
                feedback = analyze_resume_with_rag(resume_text, persona_prompt)

                resume_name = resume_file.name.split(".")[0]
                save_feedback_pdf(resume_name, feedback)

                batch_results.append({
                    "name": resume_name,
                    "score": score,
                    "skills": matched_skills,
                    "feedback": feedback
                })

            # Sort and rank
            batch_results.sort(key=lambda x: x["score"], reverse=True)

            for rank, result in enumerate(batch_results, start=1):
                st.markdown(f"### Rank {rank}: {result['name']}")
                st.metric("Score", f"{result['score']:.2f} / 1.0")

                st.markdown("**Matched Skills:**")
                st.write(result["skills"] or "No relevant skills matched.")

                st.markdown("**AI Feedback:**")
                st.write(result["feedback"])

                pdf_path = f"pdf_feedback/{result['name']}_feedback.pdf"
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label=f"Download Feedback for {result['name']}",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            key=f"download_{result['name']}"
                        )
