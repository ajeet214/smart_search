import numpy as np
from utils.azure_openai_client import client
from utils.config import DEPLOYMENT_EMBEDDING


def get_query_embedding(query: str):
    response = client.embeddings.create(
        input=[query],
        model=DEPLOYMENT_EMBEDDING
    )
    return np.array([response.data[0].embedding]).astype("float32")
