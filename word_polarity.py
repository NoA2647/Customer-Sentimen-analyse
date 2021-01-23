import json


def word_polarity(word):
    ops = []
    neg = []
    with open("negative.json", "r") as file:
        neg = json.load(file)
        file.close()
    with open("positive.json", "r") as file:
        ops = json.load(file)
        file.close()

    if word in ops:
        return 1
    elif word in neg:
        return -1
    else:
        return 0
