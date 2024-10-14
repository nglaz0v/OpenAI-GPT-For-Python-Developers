import os
import pandas as pd
import numpy as np
import nltk
import openai
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity

def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

def download_nltk_data():
    try:
       nltk.data.find('tokenizers/punkt')
    except LookupError:
       nltk.download('punkt')
    try:
       nltk.data.find('corpora/stopwords')
    except LookupError:
       nltk.download('stopwords')

def preprocess_review(review):
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    stopwords = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(review.lower())
    tokens = [token for token in tokens if token not in stopwords]
    tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

init_api()
download_nltk_data()

# получаем поисковый запрос от пользователя
input_coffee_name = input("Enter a coffee name: ")

# читаем csv-файл в DataFrame (только первые 50 строк для 
# ускорения работы примера и снижения расходов на оплату API)

df = pd.read_csv('simplified_coffee.csv', nrows=50)

# предварительная обработка обзоров: нижний регистр, токенизация,
# удаление стоп-слов и стемминг
df['preprocessed_review'] = df['review'].apply(preprocess_review)

# получаем встраивание для каждого обзора
review_embeddings = []
for review in df['preprocessed_review']:
    review_embeddings.append(get_embedding(review, engine='text-embedding-ada-002'))

# получаем индекс названия кофе, введенного пользователем
try:
    input_coffee_index = df[df['name'] == input_coffee_name].index[0]
except:
    print("Извините, такого названия кофе нет в нашей базе данных. Попробуйте еще раз.")
    exit()

# Вычисляем косинусное сходство между обзором кофе, который выбрал
# пользователь, и всеми остальными обзорами
similarities = []
input_review_embedding = review_embeddings[input_coffee_index]
for review_embedding in review_embeddings:
    similarity = cosine_similarity(input_review_embedding, review_embedding)
    similarities.append(similarity)

# получаем индексы наиболее похожих отзывов (исключая обзор исходного кофе)
most_similar_indices = np.argsort(similarities)[-6:-1]

# получаем названия наиболее похожих сортов кофе
similar_coffee_names = df.iloc[most_similar_indices]['name'].tolist()

# вывод результатов на печать
print("Сорта кофе, наиболее похожие на {}:".format(input_coffee_name))
for coffee_name in similar_coffee_names:
    print(coffee_name)
