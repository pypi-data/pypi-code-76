import os 
import requests
from zipfile import ZipFile
import shutil
from IPython.display import display, Markdown
import pandas as pd
import yaml

class Citable:

    def __init__(self, DOI):
        
        self.doi = DOI.split('/')[-1].split('.')[1]
        self.url = 'https://zenodo.org/api/records/' + self.doi
        
        if not os.path.isdir('./data'):
            os.mkdir('./data')
    
    def download(self,display=True):
        r = requests.get(self.url)
        links = [i['links']['self'] for i in r.json()['files']]
        linksfiles = [i['links']['self'] for i in r.json()['files'] if not (os.path.isfile('./data/' + i['key']) or os.path.isfile('./data/' + '.'.join(i['key'].split('.')[:-1])))]
        if not linksfiles:
            print('All files you want to download are already in the local data folder.')
        else:
            # going through all links, download and extract all files:
            for URL in linksfiles:
                try:
                    dl = requests.get(URL)

                    # write file into the 'data'-folder and name it test.zip:
                    if URL.split('.')[-1] == 'zip':
                        with open('./data/test.zip', 'wb') as f:  
                            f.write(dl.content)

                        # extract zip-file into data-folder
                        zf = ZipFile('./data/test.zip', 'r')
                        zf.extractall('./data')
                        zf.close()

                        # removing original zip-file and '__MACOSX'-folder, if it exists:
                        os.remove('./data/test.zip') 
                        if os.path.isdir('./data/__MACOSX'):
                            shutil.rmtree('./data/__MACOSX')
                    else:
                        with open('./data/' + URL.split('/')[-1], 'wb') as f:  
                            f.write(dl.content)
                    print('Successfully downloaded and extracted data under ' + URL)
                except:
                    print('Something went wrong while downloading and extracting data under ' + URL) 
        ds = []
        files = ['./data/' + URL.split('/')[-1].replace('.zip', '') for URL in links]
        fil = [URL.split('/')[-1].replace('.zip', '') for URL in links]
        for file in files:         
            # open the downloaded data as a pandas object:
            # making path
            path = file
            ending = path.split('.')[-1]

            # process file according to ending:
            if ending == 'json':
                try:
                    d = pd.read_json(path, orient = 'table')
                except:
                    d = pd.read_json(path)
            if ending == 'csv':
                try:
                    d = pd.read_csv(path, delimiter = ',')
                except:
                    d = pd.read_csv(path, delimiter = '\t')
            if ending == 'md':
                if display==True:
                    with open(path, encoding="utf8") as file:
                        d = file.read()
                    display(Markdown(d))
            ds.append(d)
                        
#               unsure if necessary!: 
#               if ending == 'yaml' or ending == 'cite':
#                    with open(path) as yml:
#                        d = yaml.load(yml, Loader=yaml.FullLoader)
        print('The download returns a list of either strings or DataFrames.')    
        print('List elements are in the order: ' + ', '.join(fil))        
        return ds