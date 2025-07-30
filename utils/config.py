# utils/config.py

"""
Module: config
--------------
Loads environment variables and defines global constants used across the app.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# -------------------------------
# 🔐 Azure OpenAI Configuration
# -------------------------------
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT_EMBEDDING = os.getenv("AZURE_OPENAI_DEPLOYMENT")
DEPLOYMENT_COMPLETION = os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT")

# -------------------------------
# 📁 File Paths
# -------------------------------
INPUT_FILE_PATH = os.getenv("INPUT_FILE")
OUTPUT_INDEX_PATH = os.getenv("OUTPUT_INDEX")
OUTPUT_METADATA_PATH = os.getenv("OUTPUT_METADATA")
CHUNK_EMBEDDINGS_PATH = os.getenv("CHUNK_EMBEDDINGS_PATH")
PROMPT_FILE_PATH = "prompts/prompt_v1.txt"  # Static relative path

# -------------------------------
# 🚀 Feature Flags
# -------------------------------
# Toggle onboarding modal visibility (true/false in .env)
SHOW_ONBOARDING = os.getenv("SHOW_ONBOARDING", "false").lower() == "true"

required_vars = [
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    DEPLOYMENT_EMBEDDING,
    DEPLOYMENT_COMPLETION
]
if not all(required_vars):
    raise EnvironmentError("One or more required environment variables are missing.")
