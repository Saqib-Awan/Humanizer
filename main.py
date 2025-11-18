import streamlit as st
from pages.humanize_text import show_humanize_page
from pages.ai_detection import show_pdf_detection_page

def main():
    st.set_page_config(
        page_title="AI Humanizer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # ALWAYS open Humanizer page
    show_humanize_page()


if __name__ == "__main__":
    main()
