#import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

#load the environment
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

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
            pass
        
        # if transcript_text:
        #     summary= text_summarizer(transcript_text, prompt)
        #     st.markdown('## Detailed Notes: ')
        #     st.write(summary)
