"""GPT request module"""
import openai
from src.app.gpt.token_counter import add_tokens
from src.configs.openai import (
    OPENAI_APITOKEN,
    OPENAI_MODELNAME,
)


openai.api_key = OPENAI_APITOKEN


def make(messages):
    """Make request to openai api"""
    response = openai.chat.completions.create(
        model=OPENAI_MODELNAME,
        messages=messages
    )
    print(f'TOKENS USED PER REQUEST: {response.usage.total_tokens}')
    add_tokens(response.usage.total_tokens)
    return response.choices[0].message.content

