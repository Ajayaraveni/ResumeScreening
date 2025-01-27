
import streamlit as st
from transformers import pipeline
import fitz
from docx import Document

# Load the pre-trained model from Hugging Face
model = pipeline('fill-mask', model='bert-base-uncased')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf = fitz.open(pdf_file)
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "
"
    return text

# Streamlit app
st.title("AI-Based Resume Screener")
st.markdown("### Upload your resume (in .txt, .pdf, or .docx format)")

# File uploader
resume_file = st.file_uploader("Choose a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])

if resume_file:
    # Determine file type and extract text accordingly
    file_type = resume_file.name.split('.')[-1].lower()
    if file_type == 'txt':
        resume_text = resume_file.read().decode("utf-8")
    elif file_type == 'pdf':
        resume_text = extract_text_from_pdf(resume_file)
    elif file_type == 'docx':
        resume_text = extract_text_from_docx(resume_file)
    
    # Show the resume text
    st.text_area("Your Resume", resume_text, height=300)
    
    # Provide AI Feedback on the resume
    st.markdown("### AI Feedback on Your Resume:")
    
    # This is a basic feedback generator based on filling in missing words (masking)
    try:
        # We process only the first 512 tokens of the text as BERT has a token limit
        feedback = model(resume_text[:512])  # Adjust token length if necessary
        st.write("Here’s some feedback on your resume:")
        st.write(f"Suggested improvements based on your resume: {feedback}")
    except Exception as e:
        st.write("There was an issue with processing the text for feedback.")
        st.write(f"Error: {e}")

else:
    st.warning("Please upload a valid resume file (.txt, .pdf, or .docx).")
