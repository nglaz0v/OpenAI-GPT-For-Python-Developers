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

kwargs = {
       "prompt": "A beautiful landscape.",
}

im = openai.Image.create(**kwargs)

print(im)
