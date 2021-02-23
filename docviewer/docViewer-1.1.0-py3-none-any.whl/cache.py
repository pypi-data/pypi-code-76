import hashlib
import os
from pathlib import Path

from .config import CONFIG


def get_cache_file(content):
    if hasattr(content, 'encode'):
        content = content.encode()
    content_md5 = hashlib.new('md5', content).hexdigest()
    cache_dir = CONFIG['CACHE_ROOT']
    cache_file = Path(cache_dir, content_md5)
    return cache_file


def load_cache(content):
    cache_file = get_cache_file(content)
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return f.read()
    return None


def write_cache(content, cache_content):
    cache_file = get_cache_file(content)
    if not cache_file.parent.exists():
        os.makedirs(cache_file.parent)
    with open(cache_file, 'wb') as f:
        f.write(cache_content)


def load_or_write_cache(func, content):
    cache = load_cache(content)
    if cache:
        return cache
    cache_content = func(content)
    write_cache(content, cache_content)
    return cache_content
