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

image = open("../resources/without_mask.png", "rb")
mask = open("../resources/mask.png", "rb")
prompt = "A group of people hiking in green forest between trees"
n = 1
size = "1024x1024"

kwargs = {
    "image": image,
    "mask": mask,
    "prompt": prompt,
    "n": n,
    "size": size,
}

response = openai.Image.create_edit(**kwargs)
image_url = response['data'][0]['url']

print(image_url)
