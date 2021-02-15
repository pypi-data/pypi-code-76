import random


def jibberjabber_generator(words, products):
    """
    Simple Gibberish non-existent products generator

    :param words:list
    :param products:list
    :return:str
    """
    while True:
        for word in words:
            product = random.choice(products)
            _ = f'{product["name"].title()} {word["name"].title()}'
            yield _, product["category"]
