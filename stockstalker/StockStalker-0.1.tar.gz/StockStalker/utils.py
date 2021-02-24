import requests
import bs4
import datetime


def marketOpen():

    primaryCheck = False

    weekday = datetime.datetime.today().weekday()
    currentTime = datetime.datetime.utcnow()
    hour = currentTime.hour

    if weekday < 5 and hour in range(15, 21):
        primaryCheck = True



    if primaryCheck:
        page = requests.get("https://www.tradinghours.com/open?")
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        hit = soup.find(class_='text-open font-weight-bold')
        if hit == None:
            hit = soup.find(class_='text-close font-weight-bold')

        if hit.text == "Yes":
            return True

        else:
            return False

    return False