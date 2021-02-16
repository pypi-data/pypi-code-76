multidic={"hundred":100,"thousand":1000,"lakh":100000,"crore":10000000,"million":1000000,"billion":1000000000,"trillion":1000000000000}
from bs4 import BeautifulSoup as bs
import re,os,datetime
def get_ammount(string):
  try:
    string=str(string)
    num=re.search(r"((\d)\.?)+",string).group()
    cs=re.search(r"\₹|\$",string).group()
    pf=re.search("(hundred|thousand|lakh|crore|million|billion|trillion)",string).group()
    return {"ammount":float(num)*multidic[pf],"currency":cs}
  except:
    pass

def clean_tags(soup,tags=[]):
  for tag in soup.find_all(tags):
    tag.decompose()


def clean_tags_span(soup):
  for tag in soup.select("span.bday"):
    tag.parent.decompose()


def minutes_to_int(running_time):
  try:
    r=re.compile("\d+")
    s=r.findall(str(running_time))
    if (s):
      return int(s[0])
    else:
      return running_time
  except:
    pass


def get_content_value(row_data):
  try:
    if row_data.find("li"):
      return [li.get_text(" ", strip=True).replace("\xa0"," ") for li in row_data.find_all("li")]
    elif row_data.find("br"):
      return [i for i in row_data.stripped_strings]
    else:
      return row_data.get_text(" ", strip=True).replace("\xa0"," ")
  except:
    pass



def remove_items(test_list, item): 
      
    # using list comprehension to perform the task 
    res = [i for i in test_list if i != item] 
    
def toDate(s):
  try:
    s=str(s)
    dregx=re.compile(r"(\d{1,2})+|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",re.I)
    matches=dregx.finditer(s)
    l=[match[0] for match in matches]
    D="N/A"
    M="N/A"
    Y="N/A"
    for i,d in enumerate(l):
      if len(d)<3:
        D=d
      if len(d)==3:
        M=d.capitalize()
      if len(d)==4:
        Y=d
      if i==2:
        break
    return datetime.datetime.strptime(D+M+Y, "%d%b%Y")
  except:
    pass


class MovieNotFoundError(Exception):
  def __init__(self):
    super().__init__("'Movie details' were not found:Try diffrent 'movie' name as argument")
class InterNetNotConnectedError(Exception):
  def __init__(self):
    super().__init__("'InterNet Not Connected' :please connect to internet")


    

