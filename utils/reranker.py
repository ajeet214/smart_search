import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def rerank_chunks(query_embedding, chunks, chunk_embeddings, top_n=3):
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
    sorted_indices = np.argsort(similarities)[::-1]

    top_chunks = [chunks[i] for i in sorted_indices[:top_n]]
    return top_chunks
