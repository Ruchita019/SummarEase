#import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


#load the environment
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = '''Answer the question as detailed as possible from the provided context, 
                        make sure to provide all the details, if the answer is not in the provided context just say, 
                        "answer is not available in the context", don't provide the wrong answer 
                        Context: \n {context}? \n
                        Question: \n {question}? \n
                        
                        Answer: '''
     
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    
    prompt1 = PromptTemplate(template=prompt_template, input_variables=['context','question'])
    chain = load_qa_chain(model,chain_type="stuff", prompt=prompt1)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model= 'models/embedding-001')

    new_db = FAISS.load_local('faiss_index',embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents":docs, "question": user_question}, return_only_outputs=True
    )

    # print(response)
    st.write("Reply: ", response['output_text'])

prompt = '''You are a expert text summarizer. You would be given a transcripts and you have to summarize it in 250 words.
            Provide important points from the pdf.  '''

#Create function to generate the summary from transcript 
def text_summarizer(transcript, prompt):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt + transcript)
    return response.text

def PDF_Summarizer():
    st.header("PDF Summarizer")
    pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            st.success("Done")
    
    user_question = st.text_input("Ask a Question from the PDF Files")
    
    if user_question:
        user_input(user_question)


    if st.button("Get Summary"):
        text =  get_pdf_text(pdf_docs)
        
        if text:
            summary= text_summarizer(text, prompt)
            st.markdown('## Detailed Notes: ')
            st.write(summary)


