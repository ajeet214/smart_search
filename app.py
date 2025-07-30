# app.py

import time
import streamlit as st
from utils.search_engine import search_top_k
from utils.answer_generator import build_prompt, generate_answer
from utils.examples import get_example_prompts
from utils.onboarding import show_onboarding
from utils.theme import apply_theme_css


# ------------------ Helper Functions ------------------ #
def load_local_css(file_paths):
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def set_example_query(example: str):
    """Set example query into the session input field."""
    st.session_state.query_input = example


# ------------------ Page Config & Setup ------------------ #
st.set_page_config(
    page_title="Smart Search with GenAI",
    page_icon="data/logo/favicon.ico",
    layout="wide"
)

# Load modularized CSS
load_local_css([
    "styles/base.css",
    "styles/theme.css",
    "styles/buttons.css",
    "styles/loader.css",
    "styles/animations.css",
])
# Sidebar theme toggle
theme = st.sidebar.radio("🌓 Theme", ("Light", "Dark"))
st.session_state["theme"] = theme
apply_theme_css(theme)

# Inject body class for styling
theme_class = "light-theme" if theme == "Light" else "dark-theme"
st.markdown(f"<body class='{theme_class}'>", unsafe_allow_html=True)

# ------------------ Title & Onboarding ------------------ #
st.title("🔍 Smart Search - GenAI Powered")
show_onboarding()

# ------------------ Session State Initialization ------------------ #
st.session_state.setdefault("query_input", "")
st.session_state.setdefault("last_query", "")
st.session_state.setdefault("last_result", None)

# ------------------ Input Area ------------------ #
st.text_input("Enter your query:", key="query_input")

# ------------------ Suggested Example Prompts ------------------ #
st.markdown("##### 💡 Try an example prompt:")
example_prompts = get_example_prompts()
buttons_per_row = 5

for i in range(0, len(example_prompts), buttons_per_row):
    row_prompts = example_prompts[i:i + buttons_per_row]
    cols = st.columns(buttons_per_row)
    for j, prompt in enumerate(row_prompts):
        cols[j].button(
            prompt,
            use_container_width=True,
            on_click=set_example_query,
            args=(prompt,)
        )

# ------------------ Search Execution ------------------ #
query = st.session_state.query_input.strip()

if query and query != st.session_state.last_query:
    with st.container():
        progress_placeholder = st.empty()

        # Step 1: Retrieve
        progress_placeholder.markdown("""
            <div class="loader"></div>
            <p style="text-align:center;">🔍 Retrieving top-k chunks...</p>
        """, unsafe_allow_html=True)
        results = search_top_k(query, k=5)
        time.sleep(0.5)

        # Step 2: Rerank
        progress_placeholder.markdown("""
            <div class="loader"></div>
            <p style="text-align:center;">🔁 Reranking chunks by relevance...</p>
        """, unsafe_allow_html=True)
        chunks = results["TextChunk"].tolist()
        st.session_state["chunks"] = chunks
        prompt = build_prompt(chunks, query)
        time.sleep(0.5)

        # Step 3: Answer with LLM
        progress_placeholder.markdown("""
            <div class="loader"></div>
            <p style="text-align:center;">💬 Generating LLM answer...</p>
        """, unsafe_allow_html=True)
        answer = generate_answer(prompt)
        progress_placeholder.empty()

        # Cache for display
        st.session_state.last_query = query
        st.session_state.last_result = {
            "chunks": chunks,
            "answer": answer
        }

# ------------------ Display Answer ------------------ #
if st.session_state.last_result:
    st.subheader("🤖 Answer")
    st.markdown(st.session_state.last_result["answer"])

    if "chunks" in st.session_state:
        chunks = st.session_state["chunks"]
        with st.expander("📚 Context used"):
            for i, chunk in enumerate(chunks, start=1):
                st.markdown(f"""
                    <div style="
                        background-color: #f1f1f1;
                        border-left: 6px solid #8bb7f0;
                        padding: 1rem;
                        border-radius: 12px;
                        margin-bottom: 0.75rem;
                        font-size: 0.95rem;
                        line-height: 1.5;
                    ">
                        <strong>{i}.</strong> {chunk}
                    </div>
                """, unsafe_allow_html=True)
