#coding:utf-8
import requests

def get_url(url):
    return requests.get(url=url)


def file_downloads(url, path):
    r = requests.get(url, stream=True)
    f = open(path, 'wb')
    for a in r.iter_content(chunk_size=100):  # iter是iter
        f.write(a)