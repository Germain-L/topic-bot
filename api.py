from dotenv import load_dotenv
import paralleldots
import os
from deep_translator import GoogleTranslator
from langdetect import detect_langs
from langdetect import DetectorFactory

import requests


load_dotenv()

paralleldots.set_api_key(os.getenv("KOMPREHEND_KEY"))
DetectorFactory.seed = 0


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
    # print(to_translate)
    # lang = detect_lang(to_translate)
    # print(lang)

    translated = GoogleTranslator(
        source="auto", target='en').translate(to_translate)

    emotion = paralleldots.emotion(translated)
    return emotion


def getKeywordFromMessage(message):
    # print(message)
    # lang = detect_lang(message)
    # print(lang)

    translated = GoogleTranslator(
        source="auto", target='en').translate(message)

    keywords = paralleldots.keywords(translated)
    print(keywords["keywords"])

    #[{'keyword': 'shitty bot', 'confidence_score': 0.910172}]}
    # get highest confidence score keyword and return
    try:
        keywords = sorted(keywords["keywords"], key=lambda x: x["confidence_score"])
        return keywords[-1]["keyword"]
    except:
        return None


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
