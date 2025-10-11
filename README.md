# 📄 Resume Analyzer (Resume Expert)

A lightweight Streamlit app that helps evaluate and compare resumes against a job description using Google's Gemini LLM.

## 🚀 What It Does
- Single Resume Review: Get an AI-generated evaluation, improvement suggestions, missing keywords, and a percentage match.
- Multi-Resume Comparison: Upload multiple PDFs and rank candidates by relevance to a job description.
- Custom Queries: Ask ad‑hoc questions about a specific resume in context of the job.

## 🧰 Tech Stack
- Streamlit (UI)
- Google Gemini (google-generativeai)
- PyMuPDF / fitz (PDF text extraction)
- pdf2image & PIL (PDF handling, optional display)
- python-dotenv (API key management)

## 📁 Folder Snapshot
- `appv2.py` – Main enhanced app (sidebar navigation + comparison)
- `app.py` – Earlier / baseline version
- `requirements.txt` – Python dependencies
- `.env` – Stores `GOOGLE_API_KEY`

---
⭐ *Resume Expert – Making Job Applications Easier* ⭐
