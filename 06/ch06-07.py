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

response_1 = openai.Edit.create(
    model="text-davinci-002",
    instrucation="correct the spelling mistakes:",
    input="The kuick brown fox jumps over the lazy dog and",
    temperature=0,
)

response_2 = openai.Edit.create(
    model="text-davinci-002",
    instrucation="correct the spelling mistakes:",
    input="The kuick brown fox jumps over the lazy dog and",
    temperature=0.9,
)

print("Temperature 0:")
print(response_1['choices'][0]['text'])
print("Temperature 0.9:")
print(response_2['choices'][0]['text'])
