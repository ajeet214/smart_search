# utils/answer_generator.py

"""
Module: answer_generator
------------------------
Responsible for constructing prompts and generating LLM-based answers
based on the provided context and user query.
"""

from utils.azure_openai_client import client
from utils.config import DEPLOYMENT_COMPLETION
from utils.prompt_loader import load_prompt_template

# Load prompt template from file (once at import)
prompt_template = load_prompt_template()


def build_prompt(chunks: list[str], query: str) -> str:
    """
    Build a prompt using the retrieved context chunks and the user query.

    Args:
        chunks (list[str]): Top-k relevant text chunks.
        query (str): User's input query.

    Returns:
        str: Formatted prompt to be passed to the LLM.
    """
    context = "\n".join(chunks)
    return prompt_template.format(context=context, query=query)


def generate_answer(prompt: str) -> str:
    """
    Generate an answer using the OpenAI completion endpoint.

    Args:
        prompt (str): Fully formatted prompt string.

    Returns:
        str: Model-generated answer.
    """
    response = client.chat.completions.create(
        model=DEPLOYMENT_COMPLETION,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
