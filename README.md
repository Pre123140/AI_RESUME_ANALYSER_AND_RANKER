# AI Resume Analyzer & Ranker (Local GenAI + RAG + Streamlit)


An end-to-end, offline, privacy-first tool that empowers users to analyze, rank, and optimize resumes against job descriptions using Retrieval-Augmented Generation (RAG), local LLMs (like Mistral), and traditional NLP methods. Built for job seekers, recruiters, and AI researchers, this app goes beyond basic keyword matching and delivers AI-generated improvement insights, intelligent querying, and batch processing support.

---

## Project Objective
- Enable **private and smart resume analysis** using GenAI, without sending data to external servers.
- Offer **explainable scoring** and detailed improvement suggestions.
- Support **batch resume screening** and ranking for recruiters.
- Allow **intelligent Q&A** over resumes using Retrieval-Augmented Generation (RAG).

---

## Features

- ✅ Real-time resume scoring using TF-IDF + cosine similarity
- ✅ Local LLM (Mistral via Ollama) for AI-driven feedback and suggestions
- ✅ RAG-based Q&A system for resume insights
- ✅ Persona-specific resume improvement suggestions
- ✅ Batch resume ranking with PDF exports for each
- ✅ OCR fallback for scanned or image resumes (PDF/Image)
- ✅ Fully offline execution (no API or internet needed)

---

## Conceptual Study
Want to explore the thought process behind this solution?
👉 [Read the Full Conceptual Study →](https://github.com/Pre123140/AI_Resume_Analyzer_Ranker/blob/main/AI_Resume_Analyzer_Ranker.pdf)

Includes:
- Architecture breakdown
- Design decisions and component interactions
- Use case scenarios (recruiters, job seekers, consultants)
- AI + NLP rationale and benchmarks
- Expansion roadmap

---

##  Tech Stack

- `Streamlit` – Web UI
- `LangChain` – RAG and prompt orchestration
- `scikit-learn` – TF-IDF, cosine similarity
- `PyMuPDF` – PDF parsing
- `docx2txt` – Word document reader
- `FAISS` – Local vector search
- `EasyOCR`, `pdf2image` – OCR for image resumes
- `Ollama` – Mistral 7B LLM runtime
- `FPDF` – Feedback PDF generation
- `pandas`, `tempfile`, `tkinter` – Output processing

---

## Folder Structure
```
AI_Resume_Analyzer_Ranker/
├── data/                         # (Optional) Sample resumes and JDs
├── models/                      # Local model files
│   └── mistral-7b-openorca.Q4_K_M.gguf
├── src/                         # Source code
│   ├── ui2.py                     # Streamlit UI
│   ├── scorer.py                  # TF-IDF + cosine scoring
│   ├── rag_agent.py               # RAG pipeline
│   ├── llm_agent.py               # Prompt handler
│   ├── pdf_generator_feedback.py  # Feedback PDF writer
│   ├── batch_ranker.py            # Batch scoring
│   ├── vector_search.py           # FAISS embeddings
├── README.md
├── requirements.txt
```

---

## How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.  Start Ollama with Mistral Model
```bash
ollama run mistral
```

### 3.  Launch the App
```bash
cd src/
streamlit run ui2.py
```

### Optional: Run Batch Ranking Script
```bash
python batch_ranker.py
```

---

## Key Functional Modules

### Resume Scoring
- TF-IDF + cosine similarity
- Extracts job-relevant matches
- Generates improvement feedback via LLM

### Resume Q&A
- Upload resume → ask questions like:
  > "What are the candidate's top 3 technical skills?"
- Uses RAG: FAISS vector index + Mistral LLM

### Batch Resume Ranking
- Upload folder of resumes + 1 JD
- Score each resume
- Generate personalized feedback PDFs
- Assign match scores and ranks

---

## Deliverables
- ✅ Resume Match Score
- ✅ Extracted Matching Keywords
- ✅ Persona-Based Suggestions
- ✅ Downloadable Feedback PDFs
- ✅ Ranked Resume Batch Processing
- ✅ Resume Q&A with Contextual Answers

---

##  Potential Next Steps
- CSV summary of batch rankings
- Role-specific resume templates
- Simulated Interview Q&A module
- Export to JSON/XML (ATS compatible)
- Email/Slack alert integration

---
##  License

This project is open for educational use only. For commercial deployment, contact the author.

---

## Contact
If you'd like to learn more or collaborate on projects or other initiatives, feel free to connect on [LinkedIn](https://www.linkedin.com/in/prerna-burande-99678a1bb/) or check out my [portfolio site](https://youtheleader.com/).
