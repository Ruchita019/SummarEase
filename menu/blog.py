#import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import base64
from io import BytesIO

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

# Remove punctuation from text
def remove_punctuation(text):
    return text.replace('*', '')

# Text-to-Speech
def text_to_speech(text, lang='en'):
    text = remove_punctuation(text)
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio_base64 = base64.b64encode(audio_fp.read()).decode()
    return audio_base64


def Blog_Summarizer():
    st.header("Blog Summarizer")
    blog_url = st.text_input("Enter the blog link:")

    
    if st.button("Get Summary"):
        with st.spinner("Processing..."):
            blog_text = fetch_blog_content(blog_url)
        
            if blog_text:
                summary= text_summarizer(blog_text, prompt)
                st.markdown('## Detailed Notes: ')
                st.write(summary)
            st.success("Your summary is here!! ")

        with st.spinner("Processing..."):
            audio_base64 = text_to_speech(summary)
            audio_html = f"""
            <audio controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            st.markdown("## Audio File")
            st.markdown(audio_html, unsafe_allow_html=True)
            st.success("Here is your Audio Summary")

