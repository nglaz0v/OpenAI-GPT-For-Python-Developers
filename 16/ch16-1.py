import torch
import clip
import PIL

# Загрузка модели CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device=device)

# Загрузка изображения
# wget https://upload.wikimedia.org/wikipedia/commons/d/d0/STS086-371-015_-_STS-086_-_Various_views_of_STS-86_and_Mir_24_crewmembers_on_the_Mir_space_station_-_DPLA_-_92233a2e397bd089d70a7fcf922b34a4.jpg -O ASTRONAUTS.jpg
image = PIL.Image.open("ASTRONAUTS.jpg")

# Предварительная обработка изображения
image_input = preprocess(image).unsqueeze(0).to(device)

# Кодирование изображения при помощи модели CLIP
with torch.no_grad():
    image_features = model.encode_image(image_input)

# Определение списка текстовых запросов
prompts = [
    "Большая галактика в центре скопления галактик, расположенного в созвездии Волопаса.",
    "Автобус MTA Long Island только что выехал из автовокзала Хемпстеда по маршруту N6.",
    "Специалисты экспедиции STS-86 Владимир Титов и Жан-Лу Кретьен позируют для фото в главном модуле станции",
    "Вид на Международную космическую станцию (МКС) с космического корабля Союз ТМА-19 при приближении к станции для стыковки. ",
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
