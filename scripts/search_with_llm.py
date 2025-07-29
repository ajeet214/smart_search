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

DEPLOYMENT_EMBEDDING = os.getenv("AZURE_OPENAI_DEPLOYMENT")
DEPLOYMENT_COMPLETION = os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT")  # e.g., gpt-35-turbo or gpt-4

# Paths
INDEX_PATH = os.getenv("OUTPUT_INDEX")
METADATA_PATH = os.getenv("OUTPUT_METADATA")

# Load index and metadata
index = faiss.read_index(INDEX_PATH)
df = pd.read_csv(METADATA_PATH)


# Get query embedding
def get_query_embedding(query: str) -> list:
    response = client.embeddings.create(
        input=[query],
        model=DEPLOYMENT_EMBEDDING
    )
    return response.data[0].embedding


# Search top-k
def search(query: str, k: int = 5):
    query_vec = np.array([get_query_embedding(query)]).astype("float32")
    D, I = index.search(query_vec, k)
    return df.iloc[I[0]]


def load_prompt_template(file_path="prompts/prompt_v1.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


PROMPT_TEMPLATE = load_prompt_template()


# Build LLM prompt
def build_prompt(chunks, query):
    context = "\n".join(chunks)
    return PROMPT_TEMPLATE.format(context=context, query=query)


# Generate answer using Azure OpenAI chat model
def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=DEPLOYMENT_COMPLETION,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# Full query pipeline
def rag_search(query: str, k: int = 5):
    results = search(query, k)
    chunks = results["TextChunk"].tolist()
    prompt = build_prompt(chunks, query)
    answer = generate_answer(prompt)
    return answer, chunks


# Main interactive loop
if __name__ == "__main__":
    while True:
        query = input("\n🔍 Enter your query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break

        answer, top_chunks = rag_search(query, k=5)

        print("\n🤖 LLM Answer:")
        print(answer)

        print("\n📚 Top Context Chunks:")
        for i, chunk in enumerate(top_chunks):
            print(f"{i+1}. {chunk}")
