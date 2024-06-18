#import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

#load the environment
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#Create a function to get the transcript from youtube URL
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e
    
prompt = '''You are a expert text summarizer. You would be given a transcripts and you have to summarize it in 250 words.
            Provide important points from the video.  '''

#Create function to generate the summary from transcript 
def text_summarizer(transcript, prompt):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt + transcript)
    return response.text

def Youtube_Summarizer():
    st.title("Youtube Video Summarizer")
    yt_url = st.text_input("Enter the youtube link:")


    if yt_url:
        video_id = yt_url.split("=")[1]
        st.image(f'https://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(yt_url)

        if transcript_text:
            summary= text_summarizer(transcript_text, prompt)
            st.markdown('## Detailed Notes: ')
            st.write(summary)


