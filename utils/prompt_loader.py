# utils/prompt_loader.py

"""
Module: prompt_loader
---------------------
Responsible for loading the LLM prompt template used to generate responses.
"""

from utils.config import PROMPT_FILE_PATH


def load_prompt_template():
    """
    Loads the prompt template from a text file.

    Returns:
        str: The prompt template string with placeholders.
    """
    with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()
