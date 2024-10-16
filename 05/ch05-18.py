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

my_song = openai.Completion.create(
    model="text-davinci-002",
    prompt="Write a rap song:\n\n",
    max_tokens=200,
    temperature=0.5
)

print(my_song.choices[0]["text"].strip())
