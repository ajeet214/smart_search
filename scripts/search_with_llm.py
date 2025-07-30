# scripts/search_with_llm.py

"""
An interactive command-line script that performs semantic search using a RAG (Retrieval-Augmented Generation) pipeline.

Steps:
1. Embeds a user query using Azure OpenAI Embedding API.
2. Retrieves top-k matching chunks from a FAISS vector index.
3. Constructs a prompt combining the query and retrieved context.
4. Sends the prompt to Azure OpenAI's Chat Completion API (e.g., GPT-4 or GPT-3.5).
5. Returns a generated answer and displays the supporting context.

Usage:
    Run the script and type natural language queries in the console.
    Type 'exit' or 'quit' to terminate.

Dependencies:
    - FAISS
    - Azure OpenAI SDK (`openai`)
    - Python-dotenv
    - Pandas
    - NumPy
"""

import os
import faiss
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI

# ---------------------- Environment Setup ---------------------- #
load_dotenv()

# Azure OpenAI Client Initialization
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Azure Model Deployment Configs
DEPLOYMENT_EMBEDDING = os.getenv("AZURE_OPENAI_DEPLOYMENT")
DEPLOYMENT_COMPLETION = os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT")

# File Paths
INDEX_PATH = os.getenv("OUTPUT_INDEX")
METADATA_PATH = os.getenv("OUTPUT_METADATA")
PROMPT_TEMPLATE_PATH = "prompts/prompt_v1.txt"

# ---------------------- Load Data ---------------------- #
index = faiss.read_index(INDEX_PATH)
df_metadata = pd.read_csv(METADATA_PATH)


# ---------------------- Helper Functions ---------------------- #
def get_query_embedding(query: str) -> list:
    """Get the embedding vector for a query string."""
    response = client.embeddings.create(input=[query], model=DEPLOYMENT_EMBEDDING)
    return response.data[0].embedding


def search_faiss(query: str, k: int = 5) -> pd.DataFrame:
    """Search top-k results from FAISS index using query embedding."""
    query_vec = np.array([get_query_embedding(query)], dtype=np.float32)
    _, indices = index.search(query_vec, k)
    return df_metadata.iloc[indices[0]]


def load_prompt_template(file_path: str = PROMPT_TEMPLATE_PATH) -> str:
    """Load the LLM prompt template from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(chunks: list[str], query: str) -> str:
    """Format the LLM prompt by injecting retrieved chunks and query."""
    context = "\n".join(chunks)
    return load_prompt_template().format(context=context, query=query)


def generate_answer(prompt: str) -> str:
    """Generate a response from the LLM based on the constructed prompt."""
    response = client.chat.completions.create(
        model=DEPLOYMENT_COMPLETION,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


def rag_search(query: str, k: int = 5) -> tuple[str, list[str]]:
    """RAG pipeline: Retrieve → Prompt → Answer."""
    results = search_faiss(query, k)
    chunks = results["TextChunk"].tolist()
    prompt = build_prompt(chunks, query)
    answer = generate_answer(prompt)
    return answer, chunks


# ---------------------- CLI Interface ---------------------- #
if __name__ == "__main__":
    while True:
        query = input("\n🔍 Enter your query (or type 'exit'): ").strip()
        if query.lower() in ("exit", "quit"):
            print("👋 Exiting Smart Search...")
            break

        answer, top_chunks = rag_search(query, k=5)

        print("\n🤖 LLM Answer:\n" + "-" * 60)
        print(answer)

        print("\n📚 Top Context Chunks:\n" + "-" * 60)
        for i, chunk in enumerate(top_chunks, start=1):
            print(f"{i}. {chunk}\n")
