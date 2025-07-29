import faiss
import pandas as pd
import numpy as np
from utils.config import CHUNK_EMBEDDINGS_PATH, OUTPUT_METADATA_PATH, OUTPUT_INDEX_PATH
from utils.reranker import rerank_chunks
from utils.embedder import get_query_embedding


# Load all chunk embeddings once
df_embeddings = np.load(CHUNK_EMBEDDINGS_PATH)

# Load FAISS index and metadata
index = faiss.read_index(OUTPUT_INDEX_PATH)
df = pd.read_csv(OUTPUT_METADATA_PATH)


def search_top_k(query: str, k: int = 10, rerank_top_n=5):

    # Get embedding for query and ensure correct shape for FAISS
    query_embedding = get_query_embedding(query)
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

    # Search FAISS for top-k
    _, I = index.search(query_embedding, k)

    matched_rows = df.iloc[I[0]]

    # Get chunks and embeddings
    chunks = matched_rows["TextChunk"].tolist()

    # Use precomputed chunk embeddings for reranking
    chunk_embeddings = df_embeddings[I[0]]

    # Re-rank chunks using cosine similarity
    reranked_chunks = rerank_chunks(query_embedding[0], chunks, chunk_embeddings, top_n=rerank_top_n)

    # Return top-N as DataFrame
    return pd.DataFrame({"TextChunk": reranked_chunks})

