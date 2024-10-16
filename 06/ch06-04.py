import os
import openai


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


init_api()

next = openai.Completion.create(
    model="text-davinci-002",
    prompt="""
    Translate the follwing sentence from English to French, Arabic, and Spanish.
    English: The cat sat on the mat.
    French:
    Arabic:
    Spanish:
    """,
    max_tokens=60,
    temperature=0
)

print(next)
