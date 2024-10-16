import os
import openai
import pandas as pd
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
from sklearn.metrics import precision_score


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
def classify_sentence(sentence: str) -> float:
    # получение встраивания предложения
    sentence_embedding = get_embedding(sentence, engine="text-embedding-ada-002")
    # вычисление сходства между предложением и каждой категорией
    similarity_scores = {}
    for category in categories:
        category_embeddings = get_embedding(category, engine="text-embedding-ada-002")
        similarity_scores[category] = cosine_similarity(sentence_embedding, category_embeddings)
    # возвращаем категорию с наивысшей оценкой сходства
    return max(similarity_scores, key=similarity_scores.get)


def evaluate_precision(categories: list) -> float:
    # загружаем набор данных
    df = pd.read_json("data/News_Category_Dataset_v3.json", lines=True).head(20)
    y_true = []
    y_pred = []

    # классифицируем каждое предложение
    for _, row in df.iterrows():
        true_category = row['category']
        predicted_category = classify_sentence(row['headline'])

        y_true.append(true_category)
        y_pred.append(predicted_category)

    # вычисляем показатель точности
    return precision_score(y_true, y_pred, average='micro', labels=categories)


precision_evaluated = evaluate_precision(categories)
print("Точность: {:.2f}".format(precision_evaluated))
