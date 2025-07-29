# scripts/embed_and_index.py
import pandas as pd
from openai import AzureOpenAI
import faiss
import numpy as np
from tqdm import tqdm
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Azure OpenAI Config
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Paths
input_file = os.getenv("INPUT_FILE")
output_index = os.getenv("OUTPUT_INDEX")
output_metadata = os.getenv("OUTPUT_METADATA")
output_embeddings = os.getenv("CHUNK_EMBEDDINGS_PATH")

# Load processed Excel Data
df = pd.read_excel(input_file)
text_chunks = df["TextChunk"].tolist()

client = AzureOpenAI(
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
  azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# Generate Embeddings using Azure OpenAI embedding
def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model=DEPLOYMENT_NAME,
    )
    return response.data[0].embedding


# Generate embeddings
embeddings = []
for chunk in tqdm(text_chunks, desc="Generating embeddings"):
    try:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
    except Exception as e:
        print(f"Error embedding text: {chunk[:60]}... | Error: {e}")
        embeddings.append([0.0] * 1536)  # fallback zero vector

# Convert to numpy array
embedding_matrix = np.array(embeddings).astype("float32")

# Build FAISS Index
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)

# Save FAISS index
faiss.write_index(index, output_index)

# Save metadata (map index to original data)
df.to_csv(output_metadata, index=False)

# Save chunk embeddings separately
np.save(output_embeddings, embedding_matrix)

print("Embeddings generated and FAISS index + embedding matrix saved successfully.")
