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
    model="text-davinci-003",
    prompt="Once upon a time",
    max_tokens=100,
    frequency_penalty=2.0,
    presence_penalty=2.0
)

print("=== Frequency and presence penalty 2.0 ===")
print(next["choices"][0]["text"])

next = openai.Completion.create(
    model="text-davinci-003",
    prompt="Once upon a time",
    max_tokens=100,
    frequency_penalty=-2.0,
    presence_penalty=-2.0
)

print("=== Frequency and presence penalty -2.0 ===")
print(next["choices"][0]["text"])
