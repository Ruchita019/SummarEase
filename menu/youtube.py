# import necessary libraries
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from gtts import gTTS
import base64
from io import BytesIO


# load the environment
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Create a function to get the transcript from youtube URL
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

# Create function to generate the summary from transcript 
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

def Youtube_Summarizer():
    st.header("Youtube Video Summarizer")
    yt_url = st.text_input("Enter the youtube link:")

    if st.button("Get Summary"):
        with st.spinner("Processing..."):
            transcript_text = extract_transcript_details(yt_url)

            if transcript_text:
                summary = text_summarizer(transcript_text, prompt)
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

    


