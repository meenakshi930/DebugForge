from openai import OpenAI

from .config import (
    NEBIUS_API_KEY,
    NEBIUS_BASE_URL,
    NEBIUS_MODEL
)


client = OpenAI(
    api_key=NEBIUS_API_KEY,
    base_url=NEBIUS_BASE_URL
)


def ask_model(prompt):
    response = client.chat.completions.create(
        model=NEBIUS_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content