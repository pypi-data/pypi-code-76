from os.path import abspath, join, dirname


def absolute_path(filename):
    return abspath(join(dirname(__file__), filename))


FILES = {
    'words': absolute_path('dist.words'),
    'products': absolute_path('dist.products'),
}


def get_collection(dist):
    """ Load up the list of words """
    _ = []
    with open(dist, 'r') as reader:
        for line in reader:
            line = line.strip()
            try:
                name, category = line.split(',')
            except ValueError:
                name, category = line, None
            _.append({'name': name, 'category': category})
    return _


collection_words = get_collection(FILES['words'])
collection_products = get_collection(FILES['products'])
