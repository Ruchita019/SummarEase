import streamlit as st

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

# from streamlit_lottie import st_lottie 
from st_on_hover_tabs import on_hover_tabs


from menu.youtube import Youtube_Summarizer 
from menu.blog import Blog_Summarizer
from menu.pdf import PDF_Summarizer


def home():
    st.title(" Welcome to SummarEase")
    st.write("There are different types of summarizer in this web-app like Youtube summarizer, Blog Summarizer and PDF Summarizer")


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