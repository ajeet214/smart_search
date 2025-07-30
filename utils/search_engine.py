# utils/search_engine.py

"""
Module: search_engine
---------------------
Performs vector-based semantic search using FAISS and reranks
the results using cosine similarity for enhanced relevance.
"""

import faiss
import pandas as pd
import numpy as np

from utils.config import (
    CHUNK_EMBEDDINGS_PATH,
    OUTPUT_METADATA_PATH,
    OUTPUT_INDEX_PATH
)
from utils.reranker import rerank_chunks
from utils.embedder import get_query_embedding


# Preload all required data at module load time
df_embeddings = np.load(CHUNK_EMBEDDINGS_PATH)  # Precomputed chunk embeddings (Numpy array)
index = faiss.read_index(OUTPUT_INDEX_PATH)     # FAISS index for similarity search
df = pd.read_csv(OUTPUT_METADATA_PATH)          # Metadata for each chunk (e.g., source info, text)


def search_top_k(query: str, k: int = 10, rerank_top_n: int = 5) -> pd.DataFrame:
    """
    Perform semantic search and rerank retrieved chunks based on relevance.

    Args:
        query (str): User's natural language question or search query.
        k (int): Number of initial top-k results to retrieve from FAISS.
        rerank_top_n (int): Number of top results to return after reranking.

    Returns:
        pd.DataFrame: DataFrame containing the top-N reranked "TextChunk" results.
    """

    # Generate embedding for the query
    query_embedding = get_query_embedding(query)
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

    # Perform FAISS similarity search
    _, I = index.search(query_embedding, k)  # I is the list of indices of top-k similar chunks

    # Retrieve the top-k matching chunks from metadata
    matched_rows = df.iloc[I[0]]
    chunks = matched_rows["TextChunk"].tolist()

    # Select corresponding embeddings for reranking
    chunk_embeddings = df_embeddings[I[0]]

    # Rerank the top-k chunks using cosine similarity
    reranked_chunks = rerank_chunks(query_embedding[0], chunks, chunk_embeddings, top_n=rerank_top_n)

    # Return final top-N chunks in DataFrame
    return pd.DataFrame({"TextChunk": reranked_chunks})
