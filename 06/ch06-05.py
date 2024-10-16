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

response = openai.Edit.create(
    model="text-davinci-002",
    instruction="Complete the story",
    input="Once upon a time."
)

print(response['choices'][0]['text'])
