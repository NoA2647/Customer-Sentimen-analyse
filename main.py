from nltk.stem import PorterStemmer
import pandas as pd
import spacy
import json
from sentiment import sentiment_review
from chart import chart
from radar import beautiful_spider
import time


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


def update_review(doc, key, value):
    if key in doc.keys():
        doc[key] = doc[key] + value
    else:
        doc[key] = value
    return doc


def main():
    start = time.time()
    data = pd.read_csv('DataSet/phone_user_review_file_1.csv', sep=",", encoding='Latin-1')
    en_data = data[data['lang'] == 'en'].dropna()  # remove other language
    df = en_data[en_data["phone_url"].str.contains('s5', case=False)].reset_index(drop=True)  # get model data
    nlp = spacy.load("en_core_web_sm")

    negative_review = dict()
    positive_review = dict()
    total_rate = 0
    print("size of model:", len(df['extract']))

    for i in range(len(df['extract'])):
        print(f"review[{i+1}] completed")
        doc = nlp(df['extract'][i])
        nouns = sentiment_review(doc)
        aspects = find_aspects(nouns)
        for aspect in aspects:
            total_rate += abs(aspects[aspect])
            if aspects[aspect] < 0:
                negative_review = update_review(negative_review, aspect, aspects[aspect])
            else:
                positive_review = update_review(positive_review, aspect, aspects[aspect])

    print("total_rate:", total_rate)
    end = time.time()
    elapsed = end - start
    print("time:", elapsed)
    '''
    for aspect in positive_review:
        print(aspect, ": {0:.2f}%".format(positive_review[aspect] * 100 / total_rate))
    print("************************************************************")
    for aspect in negative_review:
        print(aspect, ": {0:.2f}%".format(abs(negative_review[aspect]) * 100 / total_rate))
    '''
    chart(positive_review, negative_review)
    beautiful_spider(positive_review, negative_review)


main()
