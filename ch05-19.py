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
    prompt="Todo list to create a company in US\n\n1.",
    temperature=0.3,
    max_tokens=64,
    top_p=0.1,
    frequency_penalty=0,
    presence_penalty=0.5,
    stop=["6."],
)

print(next)
