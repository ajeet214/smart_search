# scripts/search.py
"""
search.py

A standalone script for performing semantic search over a FAISS index
using Azure OpenAI's embedding service.

This script:
- Loads a FAISS index and corresponding metadata file
- Embeds user-provided natural language queries
- Retrieves the top-k most relevant text chunks
- Displays matched results in the terminal

This is useful for testing retrieval performance in isolation from the full RAG pipeline.

Usage:
    python scripts/search.py
"""

import os
import faiss
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# File paths
INDEX_PATH = os.getenv("OUTPUT_INDEX")       # e.g., "embeddings/faiss_index_people_data.index"
METADATA_PATH = os.getenv("OUTPUT_METADATA") # e.g., "embeddings/metadata.csv"

# Load FAISS index and metadata
index = faiss.read_index(INDEX_PATH)
df = pd.read_csv(METADATA_PATH)


def get_query_embedding(query: str) -> list:
    """Generate an embedding for the user query using Azure OpenAI."""
    response = client.embeddings.create(
        input=[query],
        model=DEPLOYMENT_NAME
    )
    return response.data[0].embedding


def search(query: str, k: int = 5) -> pd.DataFrame:
    """
    Perform top-k similarity search against the FAISS index.

    Args:
        query (str): Natural language input
        k (int): Number of top results to return

    Returns:
        pd.DataFrame: Retrieved rows with top-matching TextChunks
    """
    query_vec = np.array([get_query_embedding(query)], dtype="float32")
    _, I = index.search(query_vec, k)
    return df.iloc[I[0]]


if __name__ == "__main__":
    while True:
        query = input("\n🔍 Enter your search query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break

        results_df = search(query, k=5)
        for i, row in results_df.iterrows():
            print(f"\n🎯 Match {i+1}: {row['TextChunk']}")
