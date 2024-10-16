from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import whisper
import queue
import os
import threading
import torch
import numpy as np
import re
from gtts import gTTS
import openai
import click


def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")


@click.command()
@click.option("--model", default="base", help="Используемая модель", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Использовать ли английскую модель", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Уровень сигнала для обнаружения голоса", type=int)
@click.option("--pause", default=0.8, help="Длительность паузы перед окончанием", type=float)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Флаг включения динамической энергии", type=bool)
@click.option("--wake_word", default="Привет компьютер", help="Команда пробуждения", type=str)
@click.option("--verbose", default=False, help="Печатать ли подробный вывод", is_flag=True, type=bool)
def main(model, english, energy, pause, dynamic_energy, wake_word, verbose):
    """Чтение аргументов."""
    # не существует английской модели с параметром large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio, args=(audio_queue, energy, pause, dynamic_energy,)).start()
    threading.Thread(target=transcribe_forever, args=(audio_queue, result_queue, audio_model, english, wake_word, verbose,)).start()
    threading.Thread(target=reply, args=(result_queue,)).start()

    while True:
        print(result_queue.get())


def record_audio(audio_queue, energy, pause, dynamic_energy):
    """Запись речи."""
    # загружаем систему распознавания речи и настраиваем пороговые значения речи и паузы
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Слушаю...")
        i = 0
        while True:
            # получаем запись и сохраняем ее в файл wav
            audio = r.listen(source)
            # Whisper ожидает получить tensor из чисел с плавающей запятой
            # https://github.com/openai/whisper/blob/main/whisper/audio.py #L49
            # https://github.com/openai/whisper/blob/main/whisper/audio.py #L112
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1


def transcribe_forever(audio_queue, result_queue, audio_model, english, wake_word, verbose):
    """Расшифровка записи."""
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        predicted_text = result["text"]

        if predicted_text.strip().lower().startswith(wake_word.strip().lower()):
            pattern = re.compile(re.escape(wake_word), re.IGNORECASE)
            predicted_text = pattern.sub("", predicted_text).strip()
            punc = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''
            predicted_text.translate({ord(i): None for i in punc})
            if verbose:
                print("Вы произнесли команду пробуждения... Обработка {}...".format(predicted_text))
            result_queue.put_nowait(predicted_text)
        else:
            if verbose:
                print("Вы не произнесли команду пробуждения... Речь проигнорирована")


def reply(result_queue):
    """Ответ пользователю."""
    while True:
        result = result_queue.get()
        data = openai.Completion.create(
            model="text-davinci-002",
            prompt=result,
            temperature=0,
            max_tokens=150,
        )
        answer = data["choices"][0]["text"]
        mp3_obj = gTTS(text=answer, lang="en", slow=False)
        mp3_obj.save("reply.mp3")
        reply_audio = AudioSegment.from_mp3("reply.mp3")
        play(reply_audio)
        os.remove("reply.mp3")


# Главная точка входа
init_api()
main()
