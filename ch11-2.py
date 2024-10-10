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

# Указываем идентификатор модели. Вставьте здесь ID своей модели
model = "ada:ft-learninggpt:drug-malady-data-2023-02-21-20-36-07"

# Используем по одному лекарству из каждого класса
drugs = [
   "What is 'A CN Gel(Topical) 20gmA CN Soap 75gm' used for?", # Класс 0
   "What is 'Addnok Tablet 20'S' used for?", # Класс 1
   "What is 'ABICET M Tablet 10's' used for?", # Класс 2
]

class_map = {
   0: "Acne",
   1: "Adhd",
   2: "Allergies",
   # ...
}

# Возвращаем класс для каждого лекарства
for drug_name in drugs:
   prompt = "Drug: {}\nMalady:".format(drug_name)

   response = openai.Completion.create(
       model=model,
       prompt= prompt,
       temperature=1,
       max_tokens=1,
   )

   response = response.choices[0].text
   try:
       print(drug_name + " применяется при " + class_map[int(response)])
   except:           
       print("Я не знаю, когда применяется " + drug_name)
   print()