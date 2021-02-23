import base64
import string
from urllib.parse import urljoin
import zlib

import requests

from .cache import load_or_write_cache
from .config import CONFIG

base64_alphabet = (string.ascii_uppercase + string.ascii_lowercase +
                   string.digits + '+/')
plantuml_alphabet = (string.digits + string.ascii_uppercase +
                     string.ascii_lowercase + '-_')
b64_to_plantuml = bytes.maketrans(
    base64_alphabet.encode('utf-8'),
    plantuml_alphabet.encode('utf-8'),
)


def compress_uml(uml_content):
    compressed_content = zlib.compress(uml_content.encode())
    encoded_content = base64.b64encode(compressed_content).translate(
        b64_to_plantuml).decode()
    return encoded_content


def get_resource_url(uml_content, server=None, image_format=None):
    compressed_content = compress_uml(uml_content)
    server = server or CONFIG['PLANTUML.SERVER']
    image_format = image_format or CONFIG['PLANTUML.IMAGE_FORMAT']
    url = urljoin(server, f'{image_format}/~1{compressed_content}')
    return url, f'.{image_format}'


def get_resource(url):
    resp = requests.get(url)
    # resp.raise_for_status()
    return resp.content


def render(uml_content):
    url, ext = get_resource_url(uml_content)
    content = load_or_write_cache(get_resource, url)
    return content, ext
