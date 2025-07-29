from utils.config import PROMPT_FILE_PATH


def load_prompt_template():
    with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()
