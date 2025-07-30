# utils/theme.py
import streamlit as st


def apply_theme_css(theme):
    if theme == "Dark":
        dark_css = """
        <style>
            body {
                background-color: #0e1117;
                color: white;
            }
            .stButton > button {
                background-color: #333;
                color: white;
            }
            .stTextInput > div > div > input {
                background-color: #222;
                color: white;
            }
            .st-expanderHeader {
                color: white !important;
            }
            .block-container {
                background-color: #0e1117;
            }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    else:
        light_css = """
        <style>
            body {
                background-color: white;
                color: black;
            }
            .st-expanderHeader {
                color: black !important;
            }
        </style>
        """
        st.markdown(light_css, unsafe_allow_html=True)
