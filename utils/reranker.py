# utils/reranker.py

"""
Module: reranker
----------------
Reranks retrieved text chunks based on cosine similarity
between their embeddings and the query embedding.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def rerank_chunks(query_embedding, chunks, chunk_embeddings, top_n=3):
    """
    Reranks the retrieved chunks based on their similarity to the query embedding.

    Args:
        query_embedding (np.ndarray): The embedding of the user's query (1D vector).
        chunks (List[str]): Original list of retrieved text chunks.
        chunk_embeddings (np.ndarray): Embeddings for all chunks (2D array).
        top_n (int): Number of top chunks to return based on similarity.

    Returns:
        List[str]: Top-N reranked chunks most relevant to the query.
    """
    # Compute cosine similarities between query and all chunks
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]

    # Sort indices based on descending similarity
    sorted_indices = np.argsort(similarities)[::-1]

    # Select top-N most similar chunks
    top_chunks = [chunks[i] for i in sorted_indices[:top_n]]
    return top_chunks
