import os

from . import plantuml, rst


def guess_method(filename):
    ext = os.path.splitext(filename)[-1]
    return ext.lstrip('.')


def render(content, method='rst'):
    mapping = {
        'rst': rst.render,
        'puml': plantuml.render,
    }
    handler = mapping[method]
    return handler(content)


def render_file(filename):
    method = guess_method(filename)
    with open(filename, 'rb') as f:
        content = f.read().decode()
    return render(content, method=method)
