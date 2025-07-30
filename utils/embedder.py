# utils/embedder.py

"""
Module: embedder
----------------
Provides a utility function to generate embeddings for a query
using the Azure OpenAI embedding model.
"""

import numpy as np
from utils.azure_openai_client import client
from utils.config import DEPLOYMENT_EMBEDDING


def get_query_embedding(query: str) -> np.ndarray:
    """
    Generates an embedding vector for a given query string using Azure OpenAI.

    Args:
        query (str): The natural language query string.

    Returns:
        np.ndarray: A float32 numpy array containing the embedding vector (shape: 1 x embedding_dim).
    """
    response = client.embeddings.create(
        input=[query],
        model=DEPLOYMENT_EMBEDDING
    )
    return np.array([response.data[0].embedding], dtype="float32")
