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

# Будем использовать лекарства из каждого класса
drugs = [
   "A CN Gel(Topical) 20gmA CN Soap 75gm", # Class 0
   "Addnok Tablet 20'S", # Class 1
   "ABICET M Tablet 10's", # Class 2
]

# возвращает класс лекарства для каждого класса
for drug_name in drugs:
   prompt = "Drug: {}\nMalady:".format(drug_name)

   response = openai.Completion.create(
	   model=model,
	   prompt= prompt,
	   temperature=1,
	   max_tokens=1,
   )

   # выводим на печать сгенерированный текст
   drug_class = response.choices[0].text
   # вывод должен содержать 0, 1 и 2
   print(drug_class)
