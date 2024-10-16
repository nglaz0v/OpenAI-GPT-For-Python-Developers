import openai
import os
import spacy
import numpy as np

# Загружаем предварительно обученную модель spaCy
# python3 -m spacy download en_core_web_md
nlp = spacy.load('en_core_web_md')


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


def cos_sim(a: str, b: str) -> float:
    """
    Вычисление косинусного подобия двух строк.
    Применяется для сравнения сходства строки пользовательского ввода и сегментов истории.
    """
    a = nlp(a)
    a_without_stopwords = nlp(' '.join([t.text for t in a if not t.is_stop]))
    b = nlp(b)
    b_without_stopwords = nlp(' '.join([t.text for t in b if not t.is_stop]))
    return a_without_stopwords.similarity(b_without_stopwords)


def sort_history(history: str, user_input: str) -> None:
    """
    Сортировка истории запросов на основе косинусного подобия между пользовательским вводом и сегментами истории.
    История представляет собой текстовую строку с разделителями.
    """
    segments = history.split(separator)
    similarities = []

    for segment in segments:
        # получаем косинусное подобие между вводом пользователя и сегментом
        similarity = cos_sim(user_input, segment)
        similarities.append(similarity)
    sorted_similarities = np.argsort(similarities)
    sorted_history = ""
    for i in range(1, len(segments)):
        sorted_history += segments[sorted_similarities[i]] + separator
    save_history_to_file(sorted_history)


def get_latest_n_from_history(history: str, n: int) -> str:
    """
    Получаем n последних сегментов из истории.
    История представляет собой текстовую строку с разделителями.
    """
    segments = history.split(separator)
    return separator.join(segments[-n:])


initial_prompt_1 = """
Вы: Привет!
ИИ: Привет!
#####
Вы: Как дела?
ИИ: В порядке, спасибо.
#####
Вы: Ты знаешь об автомобилях?
ИИ: Да, я кое-что знаю об автомобилях.
#####
Вы: Тебе доводилось есть пиццу?
ИИ: Я не ел пиццу. Я ИИ, поэтому не могу есть.
#####
Вы: Ты когда-нибудь был на луне?
ИИ: Я никогда не был на луне. А Вы?
#####
Вы: Как тебя зовут?
ИИ: Меня зовут Pixel. А вас как зовут?
#####
Вы: Какой у тебя любимый фильм?
ИИ: Мой любимый фильм The Matrix. Следуй за белым кроликом :)
#####
"""

initial_prompt_2 = """
Вы: {}
ИИ:
"""
initial_prompt = initial_prompt_1 + initial_prompt_2
separator = "#####"

init_api()
save_history_to_file(initial_prompt_1)

while True:
    prompt = input("Вы: ")
    sort_history(load_history_from_file(), prompt)
    history = load_history_from_file()
    best_history = get_latest_n_from_history(history, 5)
    full_user_prompt = initial_prompt_2.format(prompt)
    full_prompt = best_history + "\n" + full_user_prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        temperature=1,
        max_tokens=100,
        stop=[" Вы:", " ИИ:"],
    )
    response_text = response.choices[0].text.strip()
    history += "\n" + full_user_prompt + response_text + "\n" + separator + "\n"
    save_history_to_file(history)
