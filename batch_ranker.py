import os
import pandas as pd
import PyPDF2
import docx2txt
import tkinter as tk
from tkinter import filedialog
from scorer import score_resume
from rag_agent import analyze_resume_with_rag as generate_feedback
from fpdf import FPDF

# === Helper to extract text ===
def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif file_path.endswith(".docx"):
            return docx2txt.process(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return ""

# === Helper to save feedback to PDF ===
def save_feedback_pdf(resume_name, feedback_text):
    try:
        os.makedirs("pdf_feedback", exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"Resume Feedback for: {resume_name}\n\n")
        pdf.multi_cell(0, 10, feedback_text)

        output_path = os.path.join("pdf_feedback", f"{resume_name}_feedback.pdf")
        pdf.output(output_path)
        print(f"✅ PDF saved: {output_path}")
    except Exception as e:
        print(f"❌ Error saving PDF for {resume_name}: {e}")

# === Load and Rank Resumes ===
def process_batch(resume_folder, jd_file_path):
    jd_text = extract_text(jd_file_path)
    if not jd_text:
        raise ValueError("Job description could not be extracted.")

    all_results = []

    for filename in os.listdir(resume_folder):
        filepath = os.path.join(resume_folder, filename)
        if not filename.lower().endswith((".pdf", ".docx", ".txt")):
            continue

        resume_text = extract_text(filepath)
        if not resume_text:
            continue

        score, matched_skills = score_resume(resume_text, jd_text)
        feedback = generate_feedback(resume_text, jd_text, query="How can this resume be improved to better match the JD?")

        all_results.append({
            "Resume File": filename,
            "Match Score": score,
            "Matched Skills": ", ".join(matched_skills),
            "Feedback": feedback
        })

        save_feedback_pdf(filename.split('.')[0], feedback)

    df = pd.DataFrame(all_results)
    df.to_csv("batch_ranking_results.csv", index=False)
    print("✅ Batch processing completed. Saved to batch_ranking_results.csv")
    print(df.head())
    return df

# === Main (Dynamic File Dialogs) ===
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    print("📂 Select Resume Folder")
    resume_folder = filedialog.askdirectory(title="Select Folder with Resumes")

    print("📄 Select Job Description File")
    jd_file_path = filedialog.askopenfilename(title="Select JD File", filetypes=[("PDF, DOCX, TXT", "*.pdf *.docx *.txt")])

    if resume_folder and jd_file_path:
        try:
            process_batch(resume_folder, jd_file_path)
        except Exception as e:
            print("❌ Error:", e)
    else:
        print("❌ Operation cancelled. No files selected.")
    # === Persona-Tailored Query Generator ===
def generate_persona_prompt(role):
    return f"""
You are a resume evaluation assistant for a hiring manager looking to fill the role of **{role}**.
Provide constructive, detailed feedback for the candidate on how they can better tailor their resume to this role.
Focus on:
- Relevant technical and soft skills
- Achievements or metrics
- Missing keywords
- Alignment with role expectations
"""
    
