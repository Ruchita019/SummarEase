#import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

#load the environment
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#Fetching the Blog Content
def fetch_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    blog_content = ' '.join([para.get_text() for para in paragraphs])
    return blog_content

prompt = '''You are a expert text summarizer. You would be given a transcripts and you have to summarize it in 250 words.
            Provide important points from the blog.  '''

#Create function to generate the summary from transcript 
def text_summarizer(transcript, prompt):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt + transcript)
    return response.text

def Blog_Summarizer():
    st.title("Blog Summarizer")
    blog_url = st.text_input("Enter the blog link:")

    if blog_url:
        if st.button("Get Summary"):
            blog_text = fetch_blog_content(blog_url)
        
            if blog_text:
                summary= text_summarizer(blog_text, prompt)
                st.markdown('## Detailed Notes: ')
                st.write(summary)
            else:
                st.write("Unable to fetch blog content. Please check the URL and try again.")
