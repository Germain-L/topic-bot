from dotenv import load_dotenv
import paralleldots
import os
from deep_translator import GoogleTranslator
from langdetect import detect_langs
import requests


load_dotenv()

paralleldots.set_api_key(os.getenv("KOMPREHEND_KEY"))


def detect_lang(sentence) -> str:
    langs = detect_langs(sentence)

    probabilities = {}
    for lang in langs:
        if lang.lang == "en":
            probabilities["en"] = lang.prob
        elif lang.lang == "fr":
            probabilities["fr"] = lang.prob

    # return most probable language
    probabilities = sorted(probabilities.items(), key=lambda x: x[1])

    print(probabilities)
    return probabilities[0][0]


def getEmotion(to_translate) -> str:
    print(to_translate)
    lang = detect_lang(to_translate)
    print(lang)

    translated = GoogleTranslator(
        source=lang, target='en').translate(to_translate)

    emotion = paralleldots.emotion(translated)
    return emotion


def getGif(word) -> str:
    # get giph from giphy with key and best_match
    url = "http://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": os.getenv("GIPHY_KEY"),
        "q": word
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["data"][0]["url"]
