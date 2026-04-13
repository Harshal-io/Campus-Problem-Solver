import streamlit as st
import os

def load_css():
    """Reads the custom CSS file and injects it into the Streamlit app"""
    css_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'style.css')
    try:
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        print(f"Warning: Could not load CSS file: {e}")
