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
    instrucation="Exerices is good for your health.",
    input="Edit the text to make it longer.",
    top_p=0.2,
    n=2,
)

print(response['choices'][0]['text'])
print(response['choices'][1]['text'])
