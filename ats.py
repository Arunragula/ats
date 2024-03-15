import base64
import io

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import base64

import os
import io
from PIL  import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyCrlwJS-lK1tlRu1vdGa1SiAIk0RLxNsdw"))
def get_gemini_response(input,pdf_content,prompt):

    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    ## covert the pdf2image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]
        #convert to bytes
        img_byte_arr= io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
         {
          "mine_type":"image/jpeg",
          "data":base64.b64encode(img_byte_arr).decode()#encode t0 base64

         }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("no file uploaded")

#Streamlit App
st.set_page_config(page_title="ATS resume Expert")
st.header("Ats Tracking System")
input_text=st.text_area("job Description: ",key="input")
uploaded_file=st.file_uploader("upload your resume(PDF)...",type=["pdf"])
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
submit1 = st.button("Tell Me about the Resume")
#submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage match")
input_prompt1="""
You are an experienced HR With Tech Experience in the filed of Data Science, Full stack

Web development, Big Data Engineering, DEVOPS, Data Analyst, your task is to review

the provided resume against the job description for these profiles.

Please share your professional evaluation on whether the candidate's profile align- 
Highlight the strengths and weaknesses of the applicant in relation to the specified job
"""

input_prompt3="""
You are an skilled ATS (Applicant Tracking System) scanner with a deep under Web development, 
Big Data Engineering,DEVOPS,Data Analyst and 
deep ATS funct your task is to evaluate the resume against the provided job description. 
give the job description. First the output should come as percentage and then keyword.

"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("the Response is")
        st.write(response)
    else:
        st.write("Please the upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("the Response is")
        st.write(response)
    else:
        st.write("Please the upload the resume")










