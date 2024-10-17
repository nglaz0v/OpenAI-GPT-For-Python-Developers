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

prompt = "beautiful landscape"
n = 1
size = "256x256"

kwargs = {
    "prompt": prompt,
    "n": n,
    "size": size,
}

im = openai.Image.create(**kwargs)

for i in range(n):
    print(im.data[i].url)
