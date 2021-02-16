from bs4 import BeautifulSoup as bs
from googlesearch import search 
import requests,re
import urllib.request
from PyMovieI.helper import *




class PyMovieInfo:
  def __init__(self,movie):
    query = movie+" Movie "+"WikiPidea"
    try:
        requests.get("https://google.com")
    except:
        raise InterNetNotConnectedError
    try:  
      for url in search(query , num=10, stop=10):
          if(url.find("wiki")!=-1):
            break	  
      r=requests.get(url)
      soup=bs(r.content,"lxml")
      self.info_box=soup.find(class_="infobox vevent")
      info_rows=self.info_box.find_all("tr")
      clean_tags(soup,["sup","b"])
      clean_tags_span(soup)
    except:
      raise MovieNotFoundError
    self.movie_info={}
    for index ,row in enumerate(info_rows):
          if index==0:
            self.movie_info["Title"]=[row.find("th").get_text()]
          else:
            header=row.find("th")
            if header:
              content_key=row.find("th").get_text(" ", strip=True)
              content_value=get_content_value(row.find("td"))
              if type(content_value)!=list:
                content_value=[content_value]
              self.movie_info[content_key]=content_value
    self.movie_info["Release date"]=[toDate(self.movie_info.get("Release date"))]
    self.movie_info["Budget"]=[get_ammount(self.movie_info.get("Budget"))]
    self.movie_info["Box office"]=[get_ammount(self.movie_info.get("Box office"))]
    self.movie_info["Running time"]=[minutes_to_int(self.movie_info.get("Running time"))]

    self.title=self.movie_info.get("Title")
    self.release_date=self.movie_info.get("Release date")
    self.starring=self.movie_info.get("Starring")
    self.running_time=self.movie_info.get("Running time")
    self.directed_by=self.movie_info.get("Directed by")
	

  def getPoster(self,name=None,path=""):    #Poster Download
    try:
      image_url="https:"+self.info_box.img["src"]
      if name:
        urllib.request.urlretrieve(image_url, os.path.join(path,name+"."+image_url[image_url.rfind(".")+1:]))
      else:
        urllib.request.urlretrieve(image_url, os.path.join(path,image_url[image_url.rfind("/")+1:]))
    except TypeError as e:
      return -1
    except Exception as e:
      print(e)

    def get_info():
      return self.movie_info
      

