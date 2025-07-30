# utils/onboarding.py

"""
Module: onboarding
------------------
Displays a welcome onboarding message when the app is first launched,
describing how users can interact with Smart Search.
"""

import streamlit as st
from utils.config import SHOW_ONBOARDING


def show_onboarding():
    """
    Renders an animated onboarding modal on app load.
    Shows helpful guidance on how to use the Smart Search app.

    The modal appears only once per session and can be disabled
    globally via the SHOW_ONBOARDING config flag.

    Blocks the rest of the app until dismissed.
    """
    if not SHOW_ONBOARDING:
        return  # Feature disabled via config

    # Initialize session state to show onboarding if not set
    if "show_tour" not in st.session_state:
        st.session_state.show_tour = True

    if st.session_state.show_tour:

        def dismiss_modal():
            """Callback to hide onboarding modal after user clicks dismiss button."""
            st.session_state.show_tour = False

        # Logo centered in a three-column layout
        with st.container():
            cols = st.columns([4, 1, 4])
            with cols[1]:
                st.image("data/logo/smart_search_logo.png", width=320)

            # Slide-in welcome message with usage instructions
            st.markdown(
                """
                <div class="slide-in-box" style='
                    background-color: rgba(240, 240, 240, 1);
                    border-radius: 12px;
                    padding: 2rem;
                    margin-top: 1rem;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
                    '>
                    <h3>👋 Welcome to Smart Search!</h3>
                    <p>Here’s how to get started:</p>
                    <ul style="line-height: 1.6;">
                        <li>Use the example prompts to explore the data</li>
                        <li>Or enter your own natural language query</li>
                        <li>The AI will search and summarize relevant results</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("")
            # Centered dismiss button
            cols = st.columns([1, 1, 1])
            with cols[1]:
                st.button("✅ Got it, let's start!", on_click=dismiss_modal)

            # Prevent further rendering until modal is dismissed
            st.stop()
