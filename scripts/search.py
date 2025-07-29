import pandas as pd
import faiss
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# Azure OpenAI client setup
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Paths
INDEX_PATH = os.getenv("OUTPUT_INDEX")  # faiss_index_people_data.index
METADATA_PATH = os.getenv("OUTPUT_METADATA")  # people_data_with_embeddings.csv

# Load FAISS index and metadata
index = faiss.read_index(INDEX_PATH)
df = pd.read_csv(METADATA_PATH)


# Get query embedding
def get_query_embedding(query: str) -> list:
    response = client.embeddings.create(
        input=[query],
        model=DEPLOYMENT_NAME
    )
    return response.data[0].embedding


# Search top-k
def search(query: str, k: int = 5):
    query_vec = np.array([get_query_embedding(query)]).astype("float32")
    D, I = index.search(query_vec, k)
    results = df.iloc[I[0]]
    return results


# Example usage
if __name__ == "__main__":
    while True:
        query = input("\n🔍 Enter your search query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break

        results_df = search(query, k=5)
        for i, row in results_df.iterrows():
            print(f"\n🎯 Match: {row['TextChunk']}")
