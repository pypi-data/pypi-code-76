import pandas as pd
from flask import Flask, jsonify,render_template, request
import warnings
warnings.filterwarnings('ignore')
from gensim.summarization import keywords
from gensim.summarization.keywords import get_graph
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests


def results():
    # get data
    URLS = ['https://www.binance.com/en', 'http://www.supermap.com']
    ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords']
    collected_data = []
    res = []
    data = request.form['command']
    # ..............................................
    URLS = [data]
    for url in URLS:
        entry = {'url': url}
        try:
            r = requests.get(url)
        except Exception as e:
            res = 'Could not load page {}. Reason: {}'.format(url, str(e))
            print('Could not load page {}. Reason: {}'.format(url, str(e)))
            return render_template('results.html',predictions=res)
            continue
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            meta_list = soup.find_all("meta")
            for meta in meta_list:
                if 'name' in meta.attrs.keys() and meta.attrs['name'].strip().lower() in ['description', 'keywords']:
                    name = meta.attrs['name']
                    entry[name.lower()] = meta.attrs['content']
            # if len(entry) == 3:
            collected_data.append(entry)
            # else:
            #     print('Could not find all required attributes for URL {}'.format(url))
            #     res = 'Could not find all required attributes for URL {}'.format(url)
            #     return render_template('results.html',predictions=res)
        else:
            print('Could not load page {}.Reason: {}'.format(url, r.status_code))
            res = 'Could not load page {}.Reason: {}'.format(url, r.status_code)
            return render_template('results.html',predictions=res)
    print('Collected meta attributes (TODO - push to DB):')
    for entry in collected_data:
        print(entry)
        print("Summary ")

        # Textrank method
        print(keywords(str(entry)).split('\n'))
        print('\n')
        # KeyBERT method
        from keybert import KeyBERT
        model = KeyBERT('distilbert-base-nli-mean-tokens')
        print(model.extract_keywords(str(entry), keyphrase_ngram_range=(1, 2), stop_words=None))
        print('\n')
        res = model.extract_keywords(str(entry), keyphrase_ngram_range=(1, 2), stop_words=None)

    return res
