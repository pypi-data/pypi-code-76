from jibberjabber.generators import jibberjabber_generator
from jibberjabber.dictonaries import collection_words, collection_products

generator = jibberjabber_generator(collection_words, collection_products)


def jibber(category=False):
    _ = next(generator)
    if not category:
        return _[0]
    return _

