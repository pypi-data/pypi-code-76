""""nlp"""
import io
import pkgutil

import spacy
from nltk.corpus import stopwords
from spacy.lang.char_classes import ALPHA
from spacy.lang.char_classes import ALPHA_LOWER
from spacy.lang.char_classes import ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES
from spacy.lang.char_classes import LIST_ELLIPSES
from spacy.lang.char_classes import LIST_ICONS
from spacy.util import compile_infix_regex

from src.dijkstra import bestDijkstra
from src.dijkstra import createGraph


def setup():
    """
    Setup nltk

    :return:
    """
    nlp = spacy.load("fr_core_news_md")
    # modify tokenizer
    # before: st-pierre-le-moûtier -> ['st', '-', 'pierre', '-', 'le', 'moutier']
    # after: st-pierre-le-moûtier -> ['st-pierre-le-moûtier']
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER,
                au=ALPHA_UPPER,
                q=CONCAT_QUOTES,
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer

    data_arrival = pkgutil.get_data(
        __name__,
        "data/token_arrival.txt",
    ).decode()
    data_depart = pkgutil.get_data(__name__, "data/token_depart.txt").decode()
    data_etap = pkgutil.get_data(__name__, "data/token_etap.txt").decode()
    # data
    with io.StringIO(data_arrival) as arrival:
        token_arrival = [line.strip() for line in arrival]
    with io.StringIO(data_depart) as depart:
        token_depart = [line.strip() for line in depart]

    with io.StringIO(data_etap) as etap:
        token_etap = [line.strip() for line in etap]

    # converts to list of words
    stop_words = set(stopwords.words("french"))
    stop_words.remove("de")

    return token_depart, token_arrival, token_etap, nlp, stop_words


def findGare(
    sentenceList,
    listAvailableGare,
    token_depart,
    token_arrival,
    token_etap,
    stop_word,
):
    """
    Trouve les gares dans une phrase.

    :param list sentenceList: la phrase decoupé en token.
    :param list listAvailableGare: toute les gares disponible.
    :param list token_etap:
    :param list token_arrival:
    :param list token_depart:
    :param list stop_word:

    :return: listes des Gares pour le départ, l'arrivé et les gare de passage
    :rtype: (list, list, list)
    """
    start = list()
    arrived = list()
    passage = list()
    token = ""
    for token_sentence in sentenceList:
        word = token_sentence.lemma_.lower()
        g = list()
        if len(word) >= 4 and token_sentence.pos_ in ["PROPN", "NOUN"]:
            for gare in listAvailableGare:
                if gare is not None and word.lower() in gare:
                    g.append(gare)
        if len(g) == 0 and word not in stop_word:
            token = word
            continue
        if token != "" and len(g) != 0:
            if token in token_etap:
                passage = g
                token = ""
                continue
            elif token in token_arrival:
                arrived = g
                token = ""
                continue
            elif token in token_depart:
                start = g
                token = ""
                continue
            elif not start:
                start = g
                token = ""
                continue
            elif not arrived:
                arrived = g
                token = ""
                continue
        elif token == "" and len(g) != 0:
            if not start:
                start += g
                continue
            elif not arrived:
                arrived += g
                continue
            else:
                passage += g
    return start, arrived, passage


def trip(user_response, escale=2, verbose=False):
    """
    Trouve le meilleur trajet pour répondre à la question.

    :param int escale: nombre d'escale autorisée
    :param str user_response: la phrase du user
    :param boolean verbose: mode debug
    :return: le meilleur trajet
    :rtype: str
    """
    token_depart, token_arrival, token_etap, nlp, stop_words = setup()
    helper = "Format: je veux aller de (Gare Départ) à (Gare d'arrivée).\nex: je veux aller de bourges à nevers"
    word_tokens = nlp(user_response)
    filtered_sentence = [
        w
        for w in word_tokens
        if w.pos_ in ["NOUN", "VERB", "ADP", "PROPN", "AUX", "DET"]
    ]
    if verbose:
        print(f"Nombre d'escal max: {escale}")
        print(f"Phrase: {user_response}")
        print(f"token: {filtered_sentence}")
        print(f"lemme: {[w.lemma_ for w in filtered_sentence]}")
        print(f"pos: {[w.pos_ for w in filtered_sentence]}")
    grapheGare, sommets = createGraph("data/timetables.csv")
    allGareStart, allGareArrived, allGarePassage = findGare(
        filtered_sentence,
        sommets,
        token_depart,
        token_arrival,
        token_etap,
        stop_words,
    )
    if verbose:
        print(f"Gare de départ: {allGareStart}")
        print(f"Gare d'arrivée: {allGareArrived}")
        print(f"Gare de passage: {allGarePassage}")
    if allGareStart is None and allGareArrived is None:
        return "Format Invalide!!!\n" + helper
    elif allGareStart == [] or allGareArrived == []:
        return "Gare Introuvable!!!\n" + helper

    if allGarePassage:
        lGare, time = bestDijkstra(grapheGare, allGareStart, allGarePassage)
        lGare2, time2 = bestDijkstra(
            grapheGare,
            allGarePassage,
            allGareArrived,
        )
        if lGare == [] or lGare2 == []:
            lGare = list()
        else:
            lGare += lGare2
            lGare = list(dict.fromkeys(lGare))
            time += time2
    else:
        lGare, time = bestDijkstra(grapheGare, allGareStart, allGareArrived)
    if verbose:
        print(f"Gare: {lGare}")
    if not lGare:
        return "Trajet introuvable"
    elif len(lGare[1:-1]) > escale:
        return f"Trajet trouvé mais il comporte {len(lGare) - 2} escales, pour l'afficher ajouter l'option --escale {len(lGare) - 2}."
    elif len(lGare) > 2:
        passage = "Vous devrez passer par "
        for gare in lGare[1:-1]:
            passage += gare.capitalize() + ", "
        return f"Le temps de trajet pour votre voyage pour {lGare[-1].capitalize()} en partant de {lGare[0].capitalize()} sera de {time} minutes.{passage[:-2]}."
    else:
        return f"Le temps de trajet pour votre voyage pour {lGare[-1].capitalize()} en partant de {lGare[0].capitalize()} sera de {time} minutes."
