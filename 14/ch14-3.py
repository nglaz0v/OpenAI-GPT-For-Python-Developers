import openai
import os


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


def save_history_to_file(history: str) -> None:
    """Сохраняем историю взаимодействий в файле."""
    with open("history.txt", "w+") as f:
        f.write(history)


def load_history_from_file() -> str:
    """Читаем историю взаимодействий из файла."""
    with open("history.txt", "r") as f:
        return f.read()


def get_relevant_history(history: str) -> str:
    history_list = history.split(separator)
    if len(history_list) > 2:
        return separator.join(history_list[-2:])
    else:
        return history


init_api()

initial_prompt = """
Вы: Привет!
ИИ: Как дела?
Вы: {}
ИИ: """

history = ""
relevant_history = ""
separator = "#####"

while True:
    prompt = input("Вы: ")
    relevant_history = get_relevant_history(load_history_from_file())

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=initial_prompt.format(relevant_history + prompt),
        temperature=1,
        max_tokens=100,
        stop=[" Вы:", " ИИ:"]
    )

    response_text = response.choices[0].text
    history += "\nВы: " + prompt + "\n" + "ИИ: " + response_text + "\n" + separator
    save_history_to_file(history)

    print("ИИ: " + response_text)
