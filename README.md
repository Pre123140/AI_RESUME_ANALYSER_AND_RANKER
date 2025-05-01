# 🧠 AI Resume Analyzer & Ranker (Local GenAI + RAG + Streamlit)

A private, local-first application that scores resumes against job descriptions, generates tailored improvement suggestions, and enables batch ranking of multiple resumes — all powered by Retrieval-Augmented Generation (RAG) and local LLMs like Mistral.

## 🚀 Features

- Real-time resume scoring using TF-IDF + cosine similarity
- Local LLM (Mistral via Ollama) for feedback and resume insights
- RAG-based Q&A for intelligent resume querying
- Persona-specific feedback generation
- Batch resume ranking with downloadable PDF reports
- OCR support for scanned or image-based resumes
- Fully local, no API key or internet required

---

## 📂 Folder Structure


AI_Resume_Analyzer_Ranker/
│
├── data/                         # (Optional) Sample resume/JD files if needed
│
├── models/                      # Local LLM model files (e.g., mistral-7b)
│   └── mistral-7b-openorca.Q4_K_M.gguf
│
├── src/                         # All source code scripts
│   ├── ui2.py                             # Streamlit UI for end-to-end analysis
│   ├── scorer.py                          # TF-IDF scoring + feedback generator
│   ├── rag_agent.py                       # RAG agent using LangChain + FAISS
│   ├── llm_agent.py                       # Mistral/Ollama LLM prompt handler
│   ├── pdf_generator_feedback.py          # Feedback PDF export logic
│   ├── batch_ranker.py                    # Batch processing CLI script
│   ├── vector_search.py                   # FAISS-based vector index creation
│
├── README.md                  # Project overview and instructions
├── LICENSE                    # (Optional) License file
├── requirements.txt           # Python dependencies


---

## 🛠️ Tech Stack

- **Streamlit** – Web interface
- **LangChain** – Prompt chaining, RetrievalQA
- **scikit-learn** – TF-IDF, cosine similarity
- **PyMuPDF** – PDF parsing
- **docx2txt** – Word document reading
- **pdf2image + EasyOCR** – OCR fallback for scanned resumes
- **FAISS** – Vector search for RAG
- **Ollama** – Local LLM runtime (Mistral)
- **FPDF** – PDF generation
- **pandas** – Tabular result generation
- **tempfile & tkinter** – Local batch file handling

---

## ⚙️ How It Works

### 1. Resume Analysis
- Upload resume + job description
- Resume is compared to JD using TF-IDF + cosine similarity
- Matching score is shown
- AI feedback is generated using local LLM

### 2. Resume Q&A
- Upload only a resume
- Ask a question like: “What are the top technical skills?”
- RAG pipeline retrieves relevant parts and LLM answers

### 3. Batch Resume Ranking
- Upload multiple resumes and one JD
- Each resume is:
  - Scored
  - Given LLM-based feedback
  - Assigned a rank
  - Saved as a downloadable PDF

---

## 📥 Sample Usage

To run the main app:

```bash
cd src/
streamlit run ui2.py


Make sure mistral is running via Ollama:
ollama run mistral

Deliverables
✅ Resume Match Score
✅ Matched Skills Extraction
✅ Persona-Based LLM Feedback
✅ Downloadable PDF Reports
✅ Batch Resume Ranking + Ranking Labels
✅ Resume Q&A via RAG

Possible Next Steps
Add ranking summary CSV download
Add role-specific scoring templates
Add interview Q&A simulation mode
Export to ATS-compatible JSON/XML


📘 Want to explore the strategy behind the solution?
Read the detailed Conceptual Study for insights into the architecture, reasoning, and real-world impact.

📄 License & Credits
This project is open for educational and illustrative use. Please do not commercialize or republish without permission.

Made with ❤️ using open-source LLMs and local tools.
