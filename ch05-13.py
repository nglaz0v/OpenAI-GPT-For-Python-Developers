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
    prompt="Write a JSON containing priary numbers between 0 and 9 \n\n{\n\t\"primes\": [",
)
print(next)
