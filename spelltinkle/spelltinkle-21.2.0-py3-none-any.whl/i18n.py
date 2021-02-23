__all__ = ['_']

da = {
    'year': 'år',
    'years': 'år',
    'week': 'uge',
    'mo': 'ma',
    'tu': 'ti',
    'we': 'on',
    'th': 'to',
    'fr': 'fr',
    'sa': 'lø',
    'su': 'sø',
    'may': 'maj',
    'oct': 'okt',
    'modified': 'ændret',
    'me': 'mig'}

de = {
    'year': 'Yahr',
    'years': 'Yahre',
    'mon': 'Mon',
    'tue': 'Die',
    'wed': 'Mit',
    'thu': 'Don',
    'fri': 'Fre',
    'sat': 'Sam',
    'sun': 'Son',
    'me': 'mich'}


words = {
    'da': {'hej', 'en', 'et', 'jeg', 'du', 'ikke', 'og', 'er', 'så'}}

dictionary = {}


def set_language(lang=None):
    global dictionary
    dictionary = da


def _(word):
    return dictionary.get(word, word)
