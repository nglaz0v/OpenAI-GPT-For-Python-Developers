import os
import openai

# чтение переменных из файла .env, а именно API_KEY и ORG_ID
with open(".env") as env:
    for line in env:
        key, value = line.strip().split("=")
        os.environ[key] = value

# Инициализация ключа API и идентификатора организации
openai.api_key = os.environ.get("API_KEY")
openai.organization = os.environ.get("ORG_ID")

# Вызов API и получение списка моделей
models = openai.Model.list()
print(models)
