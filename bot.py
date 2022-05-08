import sqlite3
import requests
import discord
from langdetect import detect_langs
from langdetect import DetectorFactory
from dotenv import load_dotenv
import os
import random

from db import create

create()


load_dotenv()
DetectorFactory.seed = 0

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

GIPHY_KEY = os.getenv('GIPHY')
DISCORD_KEY = os.getenv('DISCORD')


# random int in range [5, 50]
def getRandomInt() -> int:
    return random.randint(5, 50)


global next
next = getRandomInt()


def detect_lang(sentence) -> str:
    langs = detect_langs(sentence)

    probabilities = {}
    for lang in langs:
        if lang.lang == "en":
            probabilities["en"] = lang.prob
        elif lang.lang == "fr":
            probabilities["fr"] = lang.prob

    print(langs)
    print(probabilities)

    # return most probable language
    probabilities = sorted(probabilities.items(), key=lambda x: x[1])
    return probabilities


def getOccurence(words, lang) -> list:
    occurences = []
    # select occurence of each word
    for word in words:
        if lang == "fr":
            cur.execute("SELECT occurence FROM fr WHERE word = ?", (word,))
        else:
            cur.execute("SELECT occurence FROM en WHERE word = ?", (word,))
        occurence = cur.fetchone()
        if occurence:
            occurences.append((word, occurence[0]))
        else:
            occurences.append((word, 99999999999999))

    return occurences


def getBestMatch(occurences) -> list:
    # get word will smalled occurence
    occurences.sort(key=lambda x: x[1])
    best_match = occurences[0][0]

    return best_match


def getGiph(word) -> str:
    # get giph from giphy with key and best_match
    url = "http://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_KEY,
        "q": word
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["data"][0]["url"]


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global next

    if message.author == client.user:
        return

    if message.content == "!giph":
        await message.channel.send(f"next giph in {next} messages")

    if next != 0:
        next -= 1
        return

    next = getRandomInt()

    # split message to words
    lang = detect_lang(message.content)
    words = message.content.split()

    occurences = getOccurence(words, lang)
    best_match = getBestMatch(occurences)
    giph = getGiph(best_match)

    print(best_match)

    await message.channel.send(giph)

client.run(DISCORD_KEY)
