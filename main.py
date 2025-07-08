import base64
import streamlit as st
import requests
import io
import PyPDF2 
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

def autoplay_video(path):
    with open(path, "rb") as video_file:
        video_bytes = video_file.read()
        encoded = base64.b64encode(video_bytes).decode()

        video_html = f"""
        <video width="100%" height="auto" autoplay muted loop playsinline style="border-radius: 10px;">
            <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)

autoplay_video("cv.mp4")

# Main title and description
st.title("AI RESUME ANALYZER")
st.markdown("Upload your resume and get AI-powered feedback tailored to your job!")

# Upload and input
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")

# PDF text extraction
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def extract_name_from_resume(resume_text):
    lines = resume_text.strip().split("\n")
    for line in lines:
        if line.strip():  
            return line.strip()
    return "Candidate"

# Resume analysis
if analyze and uploaded_file:
    resume_text = extract_text(uploaded_file)

    if not resume_text.strip():
        st.error("Resume appears empty or unreadable.")
        st.stop()

    candidate_name = extract_name_from_resume(resume_text)

    prompt = f"""
    Analyze the resume of {candidate_name}.
    
    Please provide clear and structured feedback on the following aspects:
    1. Content clarity and structure
    2. Skills presentation
    3. Experience section quality
    4. Suggestions for improving this resume to apply for {job_role or 'general job roles'}

    Resume content:
    {resume_text}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            st.markdown(f"### 📋 Resume Feedback for **{candidate_name}**")
            st.markdown(reply)
        else:
            st.error(f"Failed to get response: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")
