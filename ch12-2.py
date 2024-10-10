from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import os
import openai

# configuration
DEBUG = True

# instantiate the app
app = Flask(    name    )
app.config.from_object(    name    )

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

init_api()

def regular_discussion(prompt):
    """
    аргументы: prompt - строка
    Возвращает ответ API с использованием Davinci.
    Если пользователь спрашивает о лекарстве, вызывает get_malady_name().
    """
    prompt = """
    Далее следует диалог с ИИ-ассистентом. Ассистент доброжелателен, креативен, умен, очень дружелюбен и осторожен в вопросах здоровья Человека
    ИИ-ассистент не является врачом и не может диагностировать заболевания или назначать лечение Человеку
    ИИ-ассистент не является фармацевтом и не может рекомендовать Человеку лекарственные препараты
    ИИ-ассистент не дает Человеку советы относительно лечения
    ИИ-ассистент не ставит Человеку медицинские диагнозы
    ИИ-ассистент не назначает Человеку медицинские процедуры
    ИИ-ассистент не выдает Человеку рецепты на лекарства
    Если Человек вводит название лекарства, ИИ-ассистент подставляет ответ вместо "######".

    Человек: Привет
    ИИ: Привет, человек. Как дела? Буду рад тебе помочь. Назови лекарство, и я расскажу, для чего оно применяется.
    Человек: Vitibex
    ИИ: ######
    Человек: У меня все хорошо. Как дела у тебя?
    ИИ: У меня тоже все хорошо. Спасибо, что спросил. Буду рад тебе помочь. Назови лекарство, и я расскажу, для чего оно применяется.
    Человек: Что такое хаос-инжиниринг?
    ИИ: Прости, не могу тебе помочь. Я запрограммирован отвечать только на вопросы о лекарствах. Назови лекарство, и я расскажу, для чего оно применяется.
    Человек: Где находится Карфаген?
    ИИ: Прости, не могу тебе помочь. Я запрограммирован отвечать только на вопросы о лекарствах. Назови лекарство, и я расскажу, для чего оно применяется.
    Человек: Что такое Maxcet 5mg Tablet 10'S?
    ИИ: ######
    Человек: Что такое Axepta?
    ИИ: ######

    Человек: {}
    ИИ:""".format(prompt)

    # получение ответа от API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        stop=["\n", " Человек:", " ИИ:"],
    )
    if response.choices[0].text.strip() == "######":
        return get_malady_name(prompt)
    else:
        final_response = response.choices[0].text.strip() + "\n"
        return("{}".format(final_response))

def get_malady_name(drug_name):
    """
    аргументы: drug_name - строка
    Возвращает название заболевания, соответствующего названию препарата, из настроенной модели.
    Эта функция вызывает get_malady_description(), чтобы получить описание болезни

    """
    # указываем идентификатор модели. Вставьте здесь ID своей модели
    model = "ada:ft-learninggpt:drug-malady-data-2023-02-21-20-36-07"
    class_map = {
        0: "Acne",
        1: "Adhd",
        2: "Allergies",
        # ...
   }

    # возвращаем класс для каждого лекарства
    prompt = "Лекарство: {}\nMalady:".format(drug_name)

    response = openai.Completion.create(
        model=model,
        prompt= prompt,
        temperature=1,
        max_tokens=1,
    )

    response = response.choices[0].text.strip()
    try:
        malady = class_map[int(response)]
        print("==")
        print("Это лекарство применяется для лечения {}.".format(malady) + get_malady_description(malady))
        return "Это лекарство применяется для лечения {}.".format(malady) +  " " + get_malady_description(malady)
    except:
        return "Я не знаю, для чего применяется '" + drug_name + "'"


def get_malady_description(malady):
    """
    аргументы: malady - строка
    Получает описание болезни из API с помощью Davinci.
    """
    prompt = """
    Далее следует диалог с ИИ-ассистентом. Ассистент полезен, креативен, умен и очень дружелюбен.
    Ассистент не выдает медицинские заключения. Он только описывает недомогание, болезнь или состояние.
    Если ассистент не знает ответ, он просит перефразировать вопрос.

    Q: Что такое {}?
    A:""".format(malady)

    # получаем ответ из API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        stop=["\n", " Q:", " A:"],
   )
   return response.choices[0].text.strip() + "\\n"

@app.route('/', methods=['GET'])
def repply():
    m = request.args.get('m')
    chatbot = regular_discussion(m)
    print("chatbot: ", chatbot)
    return jsonify({'m': chatbot})

if __name__ == '__main__':
    app.run()