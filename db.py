import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()


def clean(file) -> list:
    with open(file, 'r', encoding="utf-8") as wordstxt:
        words = []
        for line in wordstxt.readlines():
            word, occurence = line.strip().split("	")
            occurence = occurence.replace(" ", "")
            words.append((word, occurence))

        return words


def clean_en(file):
    with open(file, 'r', encoding="utf-8") as wordstxt:
        words = []
        for line in wordstxt.readlines():
            line = line.strip()
            occurence, word = line.split(". ")
            occurence = occurence.replace(" ", "")
            words.append((word, occurence))

        return words


def insert(words):
    for word, occurence in words:
        cur.execute("INSERT INTO en (word, occurence) VALUES (?, ?)",
                    (word, occurence))
    con.commit()


def create():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS en (
            word TEXT,
            occurence INTEGER
        )
    """)
    con.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS fr (
            word TEXT,
            occurence INTEGER
        )
    """)
    con.commit()

    words = clean_en("words.txt")
    insert(words)

    words = clean("mots.txt")
    insert(words)
