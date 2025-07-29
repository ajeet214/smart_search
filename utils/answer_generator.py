from utils.azure_openai_client import client
from utils.config import DEPLOYMENT_COMPLETION
from utils.prompt_loader import load_prompt_template

prompt_template = load_prompt_template()


def build_prompt(chunks, query):
    context = "\n".join(chunks)
    return prompt_template.format(context=context, query=query)


def generate_answer(prompt: str):
    response = client.chat.completions.create(
        model=DEPLOYMENT_COMPLETION,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
