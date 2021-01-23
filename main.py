from nltk.stem import PorterStemmer
import pandas as pd
import spacy
import json
from chart import chart
from sentiment import sentiment


def find_aspects(nouns):
    ps = PorterStemmer()

    aspects = list()
    new_nouns = dict()
    with open("aspects.json", "r") as f:
        aspects = json.load(f)
        f.close()

    stem_aspects = [ps.stem(aspect) for aspect in aspects]

    for noun in nouns:
        if ps.stem(noun) in stem_aspects:
            index = stem_aspects.index(ps.stem(noun))
            new_nouns[aspects[index]] = nouns[noun]

    return new_nouns


def main():
    df = pd.read_csv("C:/Users/amirh/Desktop/archive/phone_user_review_file_1.csv")
    nlp = spacy.load("en_core_web_sm")
    negative_review = dict()
    positive_review = dict()
    total_rate = 0

    for i in range(1000):
        doc = nlp(df['extract'][i])
        # doc = nlp("they like phone but i dont")
        # print(doc)
        nouns = sentiment(doc)
        print(nouns)
        aspects = find_aspects(nouns)
        for aspect in aspects:
            total_rate += abs(aspects[aspect])
            if aspects[aspect] < 0:
                if aspect in negative_review.keys():
                    negative_review[aspect] = negative_review[aspect] + aspects[aspect]
                else:
                    negative_review[aspect] = aspects[aspect]

            else:
                if aspect in positive_review.keys():
                    positive_review[aspect] = positive_review[aspect] + aspects[aspect]
                else:
                    positive_review[aspect] = aspects[aspect]

    print(total_rate)
    for aspect in positive_review:
        print(aspect, ": {0:.2f}%".format(positive_review[aspect] * 100 / total_rate))
    print("************************************************************")
    for aspect in negative_review:
        print(aspect, ": {0:.2f}%".format(abs(negative_review[aspect]) * 100 / total_rate))

    chart(positive_review, "positive aspects")
    chart(positive_review, "negative aspects")


main()
