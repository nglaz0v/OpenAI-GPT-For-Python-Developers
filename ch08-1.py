import openai
import os
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity

def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

init_api()

# words.csv это csv-файл со столбцом 'text', который содержит слова
df = pd.read_csv('words.csv')

# получаем встраивания для каждого слова в кадре данных
df['embedding'] = df['text'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))

# сохраняем встраивания в другой csv-файл
df.to_csv('embeddings.csv')

# читаем новый csv-файл
df = pd.read_csv('embeddings.csv')

# преобразовываем ось встраиваний в массив numpy
df['embedding'] = df['embedding'].apply(eval).apply(np.array)

# получаем поисковый запрос от пользователя
user_search = input('Enter a search term: ')

# получаем встраивание для поискового запроса
search_term_embedding = get_embedding(user_search, engine='text-embedding-ada-002')

# вычисляем косинусное подобие между поисковым запросом и каждым словом кадра данных
df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_embedding))

print(df)

