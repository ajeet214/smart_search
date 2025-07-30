# utils/examples.py

"""
Module: examples
----------------
Provides example prompt suggestions for the Smart Search application.
These prompts help users understand how to interact with the system.
"""

from typing import List


def get_example_prompts() -> List[str]:
    """
    Returns a list of sample natural language prompts
    that users can try in the search interface.

    Returns:
        List[str]: A list of sample queries.
    """
    return [
        "Who attended AI-related events in Singapore?",
        "List members of the Data Science team based in Tokyo.",
        "Which people participated in cybersecurity training?",
        "What events did Alice Ly take part in?",
        "Show the Marketing team members from Vietnam."
    ]
