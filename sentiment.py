import json
from word_polarity import word_polarity


def add_value(doc, key, value):
    if key in doc.keys():
        return doc[key] + value
    else:
        return value


def sentiment(sentence):
    sent_dict = dict()
    adverbs = []
    wordlist = []
    with open("adverbsOfDegree.json", "r") as file:
        adverbs = json.load(file)
        file.close()

    for token in sentence:
        if word_polarity(token.text):
            sentimentMeasure = word_polarity(token.text)  # is word positive or negative?
            if (token.dep_ == "advmod"):
                continue
            elif token.dep_ == "amod":
                sent_dict[token.head.text] = add_value(sent_dict, token.head.text, sentimentMeasure)
            # for opinion words that are adjectives, adverbs
            else:
                for child in token.children:
                    # if there's a adj modifier like 'very' , add more weight to sentiment
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in adverbs):
                        sentimentMeasure *= 1.5
                    # check negative word
                    if child.dep_ == "neg":
                        sentimentMeasure *= -1
                for child in token.children:
                    # if verb, check if there's a direct object
                    if (token.pos_ == "VERB") & (child.dep_ == "dobj"):
                        sent_dict[child.text] = add_value(sent_dict, child.text, sentimentMeasure)
                        # check for 'AND' , then add both words
                        subchildren = []
                        conj = 0
                        for subchild in child.children:
                            if subchild.text == "and":
                                conj = 1
                            if (conj == 1) and (subchild.text != "and"):
                                subchildren.append(subchild.text)
                                conj = 0
                        for subchild in subchildren:
                            sent_dict[subchild] = add_value(sent_dict, subchild, sentimentMeasure)

                # check negative words
                for child in token.head.children:
                    if ((child.dep_ == "amod") or (child.dep_ == "advmod")) and (child.text in adverbs):
                        sentimentMeasure *= 1.5
                    # check negative words
                    if (child.dep_ == "neg"):
                        sentimentMeasure *= -1
                # check nouns
                for child in token.head.children:
                    noun = ""
                    if (child.pos_ == "NOUN" or child.pos_ == "PROPN") and (child.text not in sent_dict):
                        noun = child.text
                        for subchild in child.children:
                            if subchild.dep_ == "compound":
                                noun = subchild.text + " " + noun
                        sent_dict[noun] = add_value(sent_dict, noun, sentimentMeasure)
        #print("\n")
    return sent_dict
