from bs4 import BeautifulSoup
import urllib.parse
import csv
import re
from lxml import html
import requests
import PySimpleGUI as sg
import codecs
import os.path
from csv import writer
import threading

def append_list_as_row(file_name, list_of_elem):
    with open(file_name,'a+',newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerows([i] for i in list_of_elem)

def file_get_contents(url):
    encoding = 'utf-8'
    try:
        page = requests.get(url)
        return page.content.decode(encoding)
    except:
        return("")

def findAll(url):
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        return soup.find_all('a')
    except:
        return False

def crawlUrl(url,prof):
    window['-STATE-']('URL search parameter: depth=0')
    urls=[]
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    urls.append([url])
    parsed_url=urllib.parse.urlparse(url)
    host=parsed_url.scheme+"://"+parsed_url.netloc
    total=0
    for i in range(prof):
        for y in urls[i]:
            avancement="Link search depth="+str(prof)+" - actual depth="+str(i+1)+"\nURL found: "+str(total)
            window['-STATE-'](avancement)
            window.refresh()
            temp=[]
            if findAll(y)!=False:
                for link in findAll(y):
                    try:
                        if re.match(regex, link.get('href')) is not None:
                            if host in link.get('href'):
                                if link.get('href') not in temp:
                                    total+=1
                                    temp.append(link.get('href'))
                        else:
                            crawl=host+link.get('href')
                            if crawl not in temp:
                                total+=1
                                temp.append(crawl)
                    except:
                        pass
                urls.append(temp)
    return urls

def findMail(url):
    rot13 = lambda s : codecs.getencoder("rot-13")(s)[0]
    mails=[]
    total=0
    for i in url:
        tot=0
        for y in i:
            state="Mail research: "+str(total+1)+"/"+str(len(url))+" : "+str(tot+1)+"/"+str(len(i))
            window['-STATE-'](state)
            window.refresh()
            text=file_get_contents(y)
            rx = r'[\w.+-]+@[^\W_]+[.-][A-Za-z0-9.-]+'
            for z in re.findall(rx, text):
                if (z not in mails) and (rot13(z) not in mails):
                    if (".png" not in z) and (".jpg" not in z) and ("@." not in z):
                        if (".pbz" in z) or (".se" in z): #ROT13 encrypted
                            mails.append(rot13(z))
                        else:
                            mails.append(z)
            tot+=1
        total+=1
    return mails

def start(depth,filename):
    global urls
    window.Element('-LINK-').Update(visible=False)
    window.Element('-LINKLIST-').Update(visible=False)
    window.Element('-DEPTH-').Update(visible=False)
    window.Element('-LINKTEXT-').Update(visible=False)
    window.Element('-DEPTHTEXT-').Update(visible=False)
    window.Element('-START-').Update(visible=False)
    window.Element('-ADD-').Update(visible=False)
    window.Element('-SAVE-').Update(visible=False)
    window.Element('-FILENAME-').Update(visible=False)
    window.Element('-LEAVE-').Update(visible=False)
    for i in urls:
        url_list=crawlUrl(i,depth)
        mails=findMail(url_list)
        append_list_as_row(filename,mails)
    state="File created ! "+str(len(mails))+" mails have been found"
    window['-STATE-'](state)

def add(value):
    global urls
    if ("https://" not in value) and ("http://" not in value) or value in urls:
        sg.Popup('Link is wrong or already added', keep_on_top=True)
    else:
        if(len(urls)==1):
            window['-LINKLIST-'].update(str(len(urls)+1)+" link")
        else:
            window['-LINKLIST-'].update(str(len(urls)+1)+" links")
        urls.append(value)
    window.Element('-ADD-').Update(visible=False)
    window['-LINK-']('')

def inputLink(value):
    if len(value)>0:
        window.Element('-ADD-').Update(visible=True)

layout = [[sg.Text('Add a link:',k="-LINKTEXT-"), sg.Input(k='-LINK-',enable_events=True), sg.Button('Add',k="-ADD-",visible=False)],
          [sg.Text('No link added',k='-LINKLIST-')],
          [sg.Text('Search depth (Enter a number)',k="-DEPTHTEXT-"),sg.Input(k='-DEPTH-',default_text='2')],
          [sg.FileSaveAs(k='-SAVE-',  initial_folder='/tmp',file_types=(("CSV Files", "*.csv"),),target="-FILENAME-"),sg.Input(visible=True, enable_events=True, k='-FILENAME-')],
          [sg.Button('Start',k="-START-"), sg.Button('Leave',k="-LEAVE-")],
          [sg.Text(size=(100,2),k='-STATE-')]]
window = sg.Window('Email Extractor', layout)

urls=[]

def main():
    while True:
        event, values = window.read()
        if event == '-LEAVE-' or event == sg.WIN_CLOSED:
            break

        if event == '-LINK-':
            threading.Thread(target=inputLink(str(values['-LINK-']))).start()
            
        if event == '-ADD-':
            threading.Thread(target=add(str(values['-LINK-']))).start()

        if event == '-START-':
            threading.Thread(target=start(int(values['-DEPTH-']),str(values['-FILENAME-']))).start()
    window.close()

if __name__ == '__main__':
    main()
