"""Utils"""
import re


def searchGareInSentence(sentence):
    """cherche une gare"""
    sentence = sentence.lower()
    gare = re.match("gare de (.*)", sentence)
    if gare and len(gare.groups()) == 1:
        return gare.groups()[0].lower().replace(" ", "")
    else:
        return sentence.lower().replace(" ", "")
