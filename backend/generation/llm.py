import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set."
        )

    return Groq(api_key=api_key)


def generate_answer(system_prompt, user_prompt):
    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()