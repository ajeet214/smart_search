# utils/theme.py

"""
Module: theme
-------------
Handles dynamic theme switching between Light and Dark modes
by injecting custom CSS into the Streamlit app.
"""

import streamlit as st


def apply_theme_css(theme: str):
    """
    Applies custom CSS styles based on the selected theme.

    Args:
        theme (str): Either "Light" or "Dark" to determine which theme to apply.
    """
    if theme == "Dark":
        # Custom dark mode styles
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
        # Custom light mode styles
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
