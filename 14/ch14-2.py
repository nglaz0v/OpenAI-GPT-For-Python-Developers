import openai
import os


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


init_api()

initial_prompt = """
Вы: Всем привет!
ИИ: Как дела?
Вы: {}
ИИ: """

history = ""

while True:
    prompt = input("Вы: ")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=initial_prompt.format(prompt),
        temperature=1,
        max_tokens=100,
        stop=[" Вы:", " ИИ:"]
    )

    response_text = response.choices[0].text
    history += "Вы: " + prompt + "\n" + "ИИ: " + response_text + "\n"

    print("ИИ: " + response_text)
