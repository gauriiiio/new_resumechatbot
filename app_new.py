import os
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="Resume Q&A Bot", page_icon="📝")
st.title("Resume Chatbot")

# File upload
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

resume_text = ""

 # Extract text from PDF
def extract_text(file):

     text = ""
     with fitz.open(stream=file.read(), filetype="pdf") as doc:
         for page in doc:
             text += page.get_text()
     return text


if uploaded_file:
    resume_text = extract_text(uploaded_file)  # still extract text
    st.success("Resume uploaded successfully!")
    # Don't show st.text_area() to the user





    # Chatbot interface
    st.subheader("Ask something about the resume")
    user_input = st.text_input("Your question")

    if user_input:
        with st.spinner("Thinking..."):
            prompt = f"The resume content is:\n\n{resume_text}\n\nQuestion: {user_input}"
            try:
                response = model.generate_content(prompt)
                st.markdown("### Answer")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error from Gemini: {e}")
else:
    st.info("Please upload a resume PDF to begin.")
