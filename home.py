import streamlit as st
from streamlit_lottie import st_lottie
import json

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

from st_on_hover_tabs import on_hover_tabs

from menu.youtube import Youtube_Summarizer 
from menu.blog import Blog_Summarizer
from menu.pdf import PDF_Summarizer

def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
lottie_filepath = "src/home.json"
lottie_json = load_lottie_file(lottie_filepath)

def home():
    st.markdown("<h1 style='text-align: center;'>SummarEase</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; text-align: center;'>Welcome to the SummarEase, a Text-Summarization WebApp</p>", unsafe_allow_html=True)
    st_lottie(lottie_json, height=300, key="example")
    st.markdown("<p style='font-size:20px;'></p>", unsafe_allow_html=True)


def main():
    with st.sidebar:
        
        tabs = on_hover_tabs(tabName=['Home', 'Youtube Summarizer', 'Blog Summarizer', 'PDF Summarizer'], 
                            iconName=['home','work' , 'edit', 'article' ], 
                            default_choice=0)

    menu = {
        
        'Home': home,
        'Youtube Summarizer': Youtube_Summarizer,
        'Blog Summarizer': Blog_Summarizer,
        'PDF Summarizer': PDF_Summarizer,

    }
    
    menu[tabs]()

if __name__ == "__main__":
    main()