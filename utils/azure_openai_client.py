# utils/azure_openai_client.py

"""
Module: azure_openai_client
---------------------------
Initializes and exposes a configured Azure OpenAI client instance.
"""

from openai import AzureOpenAI
from utils.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION
)

# Azure OpenAI client instance used throughout the application
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)
