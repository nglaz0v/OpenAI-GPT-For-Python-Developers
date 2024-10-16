import torch
import clip
import PIL

# Загрузка модели CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device=device)

# Загрузка изображения
image = PIL.Image.open("../resources/ASTRONAUTS.jpg")

# Предварительная обработка изображения
image_input = preprocess(image).unsqueeze(0).to(device)

# Кодирование изображения при помощи модели CLIP
with torch.no_grad():
    image_features = model.encode_image(image_input)

# Определение списка текстовых запросов
prompts = [
    "Большая галактика в центре скопления галактик, расположенного в созвездии Волопаса.",
    " Автобус MTA Long Island только что выехал из автовокзала Хемпстеда по маршруту N6.",
    "Специалисты экспедиции STS-86 Владимир Титов и Жан-Лу Кретьен позируют для фото в главном модуле станции",
    " Вид на Международную космическую станцию (МКС) с космического корабля Союз ТМА-19 при приближении к станции для стыковки. ",
    "Цирковой тигр в клетке на фоне дрессировщика тигров.",
    "Автомеханик занимается ремонтом двигателя",
]

# кодируем текстовые запросы с помощью модели CLIP
with torch.no_grad():
    text_features = model.encode_text(clip.tokenize(prompts).to(device))

# вычисляем сходство между изображением и каждым запросом
similarity_scores = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# выводим на печать запрос с наивысшей оценкой сходства
most_similar_prompt_index = similarity_scores.argmax().item()
most_similar_prompt = prompts[most_similar_prompt_index]
print("Изображение больше всего соответствует запросу: {}".format(most_similar_prompt))