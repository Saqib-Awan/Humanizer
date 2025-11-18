# main.py
import streamlit as st
from pages.humanize_text import show_humanize_page

def main():
    st.set_page_config(
        page_title="AI Text Humanizer - Make AI Content Undetectable",
        layout="wide", 
        initial_sidebar_state="collapsed",
        page_icon="✍️"
    )

    # Custom CSS to remove sidebar and style the app
    st.markdown("""
        <style>
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Remove default padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Style buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Style text areas */
        .stTextArea > div > div > textarea {
            border-radius: 8px;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Always show humanize page
    show_humanize_page()

if __name__ == "__main__":
    main()