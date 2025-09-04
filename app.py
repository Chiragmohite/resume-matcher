# app.py — Simple Resume vs Job matcher using Streamlit + PyPDF2
import streamlit as st
from PyPDF2 import PdfReader

# --- Default job description (editable in UI) ---
DEFAULT_JOB = """We are looking for a Data Analyst with experience in Python, SQL,
Machine Learning, and Data Visualization. Knowledge of Java and Cloud platforms is a plus."""

# --- Default required skills (editable in sidebar) ---
DEFAULT_SKILLS = ["Python", "SQL", "Machine Learning", "Data Visualization", "Java", "Cloud"]

def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file using PyPDF2."""
    try:
        reader = PdfReader(uploaded_file)
        text_pages = []
        for p in reader.pages:
            txt = p.extract_text()
            if txt:
                text_pages.append(txt)
        return "\n".join(text_pages)
    except Exception as e:
        return f"[Error reading PDF: {e}]"

def match_skills(resume_text, required_skills):
    """
    Return (matched_skills, missing_skills, score_percent).
    Matching is case-insensitive simple substring match (fast & simple).
    """
    if not required_skills:
        return [], [], 0
    rt = resume_text.lower()
    matched = [s for s in required_skills if s.lower() in rt]
    missing = [s for s in required_skills if s not in matched]
    score = round((len(matched) / len(required_skills)) * 100)
    return matched, missing, score

def main():
    st.set_page_config(page_title="Resume → Job Matcher", layout="centered")
    st.title("📄 Resume → Job Matcher")
    st.write("Upload a resume PDF and compare it to a job description.")

    # Sidebar: editable skills
    st.sidebar.header("Settings")
    skills_text = st.sidebar.text_area("Required skills (comma separated)", 
                                       value=", ".join(DEFAULT_SKILLS), height=120)
    required_skills = [s.strip() for s in skills_text.split(",") if s.strip()]

    # Job description textarea (editable)
    job_description = st.text_area("Job description (paste or edit)", value=DEFAULT_JOB, height=150)

    uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    if uploaded:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded)
        st.subheader("Extracted resume text (first 1500 chars)")
        st.text_area("Resume text", value=resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""), height=200)

        matched, missing, score = match_skills(resume_text, required_skills)

        st.subheader("Match Results")
        st.metric(label="Match Score", value=f"{score}%")
        st.write("**Matched skills:**", ", ".join(matched) if matched else "None")
        st.write("**Missing skills:**", ", ".join(missing) if missing else "None")

        # Show job description in an expander for reference
        with st.expander("Job description"):
            st.write(job_description)

        # Tip to improve
        st.caption("Tip: Edit required skills in the sidebar, or paste a more complete job description above.")

    else:
        st.info("Upload a resume PDF to start matching.")

if __name__ == "__main__":
    main()
