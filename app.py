from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process uploaded PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts, first_page
    else:
        raise FileNotFoundError("No file uploaded")

# ----------- Streamlit UI -------------
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

st.title("ATS Resume Expert 🚀")
st.write("An AI-powered Applicant Tracking System for Resume Analysis")

# Input Area
st.markdown("### 📌 Upload Your Resume & Job Description")
col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_area("Enter Job Description 📝", height=150)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    if uploaded_file:
        st.success("✅ Resume Uploaded Successfully!")
        pdf_content, first_page = input_pdf_setup(uploaded_file)
        st.image(first_page, caption="📄 Resume Preview", width=250)

# Buttons
col3, col4 = st.columns([1, 1])
with col3:
    submit1 = st.button("📊 Analyze Resume")
with col4:
    submit3 = st.button("📏 Percentage Match")

# AI Prompts
input_prompt1 = """
You are an experienced HR Manager. Review the provided resume against the job description.
Share insights on alignment, strengths, and weaknesses.
"""

input_prompt2 = """
You are an ATS scanner. Analyze the resume against the job description.
Provide a match percentage, missing keywords, and final thoughts.
"""

# Actions
if submit1:
    if uploaded_file and input_text:
        with st.spinner("Analyzing Resume... ⏳"):
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.success("✅ Analysis Complete!")
        st.subheader("📢 AI Feedback")
        st.write(response)
    else:
        st.error("⚠️ Please upload a resume and enter a job description.")

if submit3:
    if uploaded_file and input_text:
        with st.spinner("Calculating Match Percentage... ⏳"):
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.success("✅ Match Percentage Calculated!")
        st.subheader("🎯Match Results")
        st.write(response)
    else:
        st.error("⚠️ Please upload a resume and enter a job description.")
