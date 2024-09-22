from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
import fitz

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text_parts = [page.get_text() for page in document]
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")

def extract_percentage(response_text):
    try:
        # Extract the percentage match from the response text
        print(response_text)
        percentage_str = response_text.split('Job Description Percentage Match: ')[1].split('%')[0].strip()
        if percentage_str==0.0:
            percentage_str = response_text.split('**Job Description Percentage Match:** ')[1].split('%')[0].strip()
        print(percentage_str)
        return float(percentage_str)
    except (IndexError, ValueError):
        return 0.0

def compare_resumes(job_description, uploaded_files, prompt):
    results = []
    for uploaded_file in uploaded_files:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, prompt)
        percentage_match = extract_percentage(response)
        results.append((uploaded_file.name,percentage_match, response))
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    return results

### STREAMLIT APP ###

st.set_page_config(page_title="Resume Expert")

# Navigation
page = st.sidebar.selectbox("Choose a page", ["Resume Check", "Compare Resumes"])

if page == "Resume Check":
    st.header("RESUME CHECK")
    st.subheader('This Application helps you in your Resume Review with help of GEMINI AI [LLM]')
    input_text = st.text_input("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
    pdf_content = ""

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("How Can I Improvise my Skills")
    submit3 = st.button("What are the Keywords That are Missing")
    submit4 = st.button("Percentage match")
    input_promp = st.text_input("Queries: Feel Free to Ask here")
    submit5 = st.button("Answer My Query")

    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt2 = """
    You are an Technical Human Resource Manager with expertise in data science, 
    your role is to scrutinize the resume in light of the job description provided. 
    Share your insights on the candidate's suitability for the role from an HR perspective. 
    Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
    """

    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. As a Human Resource manager,
    assess the compatibility of the resume with the role. Give me what are the keywords that are missing.
    Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
    """

    input_prompt4 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
    """

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload a PDF file to proceed.")

    elif submit2:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload a PDF file to proceed.")

    elif submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload a PDF file to proceed.")

    elif submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload a PDF file to proceed.")

    elif submit5:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_promp, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload a PDF file to proceed.")

    # footer = """
    # *Resume Expert - Making Job Applications Easier*
    # """
    # st.markdown(footer, unsafe_allow_html=True)

elif page == "Compare Resumes":
    st.header("COMPARE RESUMES")
    st.subheader('Upload multiple resumes to compare and rank candidates based on job description')

    job_description = st.text_input("Job Description: ", key="job_description")
    uploaded_files = st.file_uploader("Upload Resumes(PDF)...", type=["pdf"], accept_multiple_files=True)

    # input_prompt5 = """
    # You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    # your task is to evaluate all the resumes against the provided job description. 
    # I need the percentage of match if the resume matches the job description.
    # The output should be in this format for each candidate:
    # CANDIDATE NAME: <name> 
    # Job Description Percentage Match: <percentage> 
    # Key Words Matched: <keywords> 
    # Strengths: <strengths> 
    # Weaknesses: <weaknesses> 
    # """

    input_prompt5 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 

    Your task is to evaluate each candidate based on the provided resume snippets and the job description. 

    For each candidate, provide a structured output in the following format:

    For strengths and weaknesses please have only 3 points max for each.

    Output should always maintain this format:

    * CANDIDATE NAME: <Candidate's Name>
    * Job Description Percentage Match: <Percentage Match>
    * Key Words Matched: <Comma-separated list of key words>
    * Strengths:
    * <Strength 1>
    * <Strength 2>
    * ...
    * Weaknesses:
    * <Weakness 1>
    * <Weakness 2>
    * ...

    Prioritize clarity, conciseness, and objectivity in your analysis.
    """

    if st.button("Compare Resumes"):
        if uploaded_files:
            results = compare_resumes(job_description, uploaded_files, input_prompt5)
            st.subheader("Comparison Results")
            # st.write(response)
            for idx, (file_name,percentage_match, response) in enumerate(results):
                st.write(f":blue-background[Rank {idx + 1}: {file_name}]")
                # st.write(f"Match Percentage: {percentage_match}%")
                st.write(response)
        else:
            st.write("Please upload PDF files to proceed.")

footer = """
*Resume Expert - Making Job Applications Easier*
"""
st.markdown(footer, unsafe_allow_html=True)
