import json as jn

class lords_json():
    def __init__(self):
        self.help = 'lords_json ist ein addon was json file arbeit noch mal einfacher machen sollte nutse get(filename) um einen file zu öffnen oder nutse whrite(file, data) um ein datei zu schreiben.'

    def get(self, file):
        json = open(f'{file}.json', 'r')
        json = jn.load(json)
        return json

    def whrite(self, file, data):
        with open(f'{file}.json', 'w') as outfile:
            jn.dump(data, outfile)

"""
data sollte etwas wie

import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

sein
"""