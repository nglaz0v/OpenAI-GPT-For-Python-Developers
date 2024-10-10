import os
import openai
import pandas as pd
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

categories = [
    "POLITICS",
    "WELLNESS",
    "ENTERTAINMENT",
    "TRAVEL",
    "STYLE & BEAUTY",
    "PARENTING",
    "HEALTHY LIVING",
    "QUEER VOICES",
    "FOOD & DRINK",
    "BUSINESS",
    "COMEDY",
    "SPORTS",
    "BLACK VOICES",
    "HOME & LIVING",
    "PARENTS",
    ]

# определение функции для классификации предложений
def classify_sentence(sentence):
    # получение встраивания предложения
    sentence_embedding = get_embedding(sentence, engine="text-embedding-ada-002")
    # вычисление сходства между предложением и каждой категорией
    similarity_scores = {}
    for category in categories:
       category_embeddings = get_embedding(category, engine="text-embedding-ada-002")
       similarity_scores[category] = cosine_similarity(sentence_embedding, category_embeddings)
    # возвращаем категорию с наивысшей оценкой сходства
    return max(similarity_scores, key=similarity_scores.get)

# классификация предложений
sentences = [
   "1 dead and 3 injured in El Paso, Texas, mall shooting",
   "Director Owen Kline Calls Funny Pages His ‘Self-Critical’ Debut",
   "15 spring break ideas for families that want to get away",
   "The US is preparing to send more troops to the Middle East",
   "Bruce Willis' 'condition has progressed' to frontotemporal dementia, his family says",
   "Get an inside look at Universal’s new Super Nintendo World",
   "Barcelona 2-2 Manchester United: Marcus Rashford shines but Raphinha salvages draw for hosts",
   "Chicago bulls win the NBA championship",
   "The new iPhone 12 is now available",
   "Scientists discover a new dinosaur species",
   "The new coronavirus vaccine is now available",
   "The new Star Wars movie is now available",
   "Amazon stock hits a new record high",
]

for sentence in sentences:
    print("{:50} category is {}".format(sentence, classify_sentence(sentence)))
    print()
