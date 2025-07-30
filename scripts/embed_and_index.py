# scripts/embed_and_index.py

"""
This script performs the following preprocessing tasks for RAG-based systems:

1. Loads preprocessed text chunks from an Excel file.
2. Generates vector embeddings using Azure OpenAI's embedding API.
3. Builds and saves a FAISS index for similarity search.
4. Saves metadata and raw embedding vectors for future use.

Requirements:
- Environment variables must be defined in a `.env` file.
- Input Excel file must include a 'TextChunk' column.

Usage:
    python scripts/embed_and_index.py
"""

import os
import faiss
import numpy as np
import pandas as pd
from tqdm import tqdm
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# File paths from .env
input_file = os.getenv("INPUT_FILE")
output_index = os.getenv("OUTPUT_INDEX")
output_metadata = os.getenv("OUTPUT_METADATA")
output_embeddings = os.getenv("CHUNK_EMBEDDINGS_PATH")

# Load preprocessed input data
df = pd.read_excel(input_file)
text_chunks = df["TextChunk"].tolist()


def get_embedding(text: str) -> list:
    """
    Generate an embedding for a given text chunk using Azure OpenAI.

    Args:
        text (str): Input string to be embedded.

    Returns:
        list: Embedding vector (float list).
    """
    response = client.embeddings.create(
        input=[text],
        model=DEPLOYMENT_NAME
    )
    return response.data[0].embedding


# Generate embeddings with progress tracking and fallback for failures
embeddings = []
for chunk in tqdm(text_chunks, desc="🔄 Generating embeddings"):
    try:
        embedding = get_embedding(chunk)
    except Exception as e:
        print(f"⚠️ Error embedding: {chunk[:60]}... | Reason: {e}")
        embedding = [0.0] * 1536  # Fallback: zero vector
    embeddings.append(embedding)

# Convert to NumPy array
embedding_matrix = np.array(embeddings).astype("float32")

# Build FAISS index from embeddings
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)

# Save FAISS index
faiss.write_index(index, output_index)

# Save metadata
df.to_csv(output_metadata, index=False)

# Save raw embeddings to .npy
np.save(output_embeddings, embedding_matrix)

print("✅ Embeddings generated and saved. FAISS index and metadata exported.")
