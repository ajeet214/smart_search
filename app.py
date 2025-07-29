# app.py
import streamlit as st
from utils.search_engine import search_top_k
from utils.answer_generator import build_prompt, generate_answer
from utils.examples import get_example_prompts
from utils.onboarding import show_onboarding


# Load external CSS file
def load_local_css(path):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_local_css("styles/style.css")

st.set_page_config(page_title="Smart Search with GenAI", page_icon="🔍", layout="wide")
st.title("🔍 Smart Search - GenAI Powered")

# Show the onboarding modal
show_onboarding()

# Input
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

st.text_input("Enter your query:", key="query_input")

# Suggested prompts (as buttons)
st.markdown("##### 💡 Try an example prompt:")
example_prompts = get_example_prompts()
buttons_per_row = 5  # You can change to 2 or 4 depending on layout


def set_example_query(example):
    st.session_state.query_input = example


for i in range(0, len(example_prompts), buttons_per_row):
    row_prompts = example_prompts[i:i + buttons_per_row]
    cols = st.columns(buttons_per_row)
    for j, prompt in enumerate(row_prompts):
        cols[j].button(prompt, use_container_width=True, on_click=set_example_query, args=(prompt,))


# Run the search
query = st.session_state.query_input.strip()

if query:
    with st.spinner("Searching and generating answer..."):
        results = search_top_k(query, k=5)
        chunks = results["TextChunk"].tolist()
        prompt = build_prompt(chunks, query)
        answer = generate_answer(prompt)

    st.subheader("🤖 Answer")
    st.markdown(answer)

    with st.expander("📚 Context used"):
        for i, chunk in enumerate(chunks, start=1):
            st.markdown(f"**{i}.** {chunk}")
