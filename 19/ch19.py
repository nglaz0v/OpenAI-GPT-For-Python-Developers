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

image = open("../resources/original_image.png", "rb")
n = 3
size = "1024x1024"

kwargs = {
    "image": image,
    "n": n,
    "size": size
}

response = openai.Image.create_variation(**kwargs)
url = response
