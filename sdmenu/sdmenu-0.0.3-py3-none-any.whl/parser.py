from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
from requests.models import Response
from sdmenu.classes import menu_item
from sdmenu.classes.nutrition import find_nutrition_by_url
from typing import List

DAY_INDICIES = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
BASE_URL = 'https://hdh-web.ucsd.edu'
DEFAULT_PARSER = 'html.parser'
HOURS_ID = 'hoursContainer'
MENU_ID = 'menuContainer'


def parse_one_item(tag: Tag) -> menu_item:
    '''Parse a <li> listing to a menu item'''
    name = str()
    price = 0
    nutrition = list()
    link = str()
    for item in tag.contents:
        if item.name == 'a':
            text = item.contents[0].strip() # Bacon Bobcat Sandwich $4.25
            if 'href' in item.attrs:
                link = BASE_URL + item['href']
            price_str = text.split(' ')[-1] # $4.25
            name = text[:len(name) - len(price_str) - 1] # Bacon Bobcat Sandwich
            try:
                price = float(price_str[1:]) # 4.25
            except:
                pass
        elif item.name == 'img':
            if 'href' in item.attrs:
                icon_item = find_nutrition_by_url(item['href'])
                if icon_item:
                    nutrition.append(icon_item)
    return menu_item(name, price, nutrition, link)


def parse_item_list(tag: Tag) -> List[menu_item]:
    '''Parse a <ul> subsection of the menu'''
    if 'id' in tag.attrs and 'nutrition' in tag['id']:
        return list()
    items = list()
    for item in tag.contents:
        if type(item) is Tag and item.name == 'li':
            items.append(parse_one_item(item))
    return items


def parse_web_items(tag: Tag) -> List[menu_item]:
    '''Parse the <div> menu'''
    items = list()
    for container in tag.contents:
        if type(container) is Tag:
            items.extend(parse_item_list(container))
    return items


def parse_hours(tag: Tag) -> List[List[int]]:
    '''Parse <div> hours'''
    hours = [[-1, -1]] * 7
    try:
        # Hardcoded traversal, since hours are not critical
        for option in tag.div.ul.li.contents:
            if type(option) is tag:
                date_string = option.contents[0].strip()
                weekday_string = date_string.split(' ')[0]
                if weekday_string in DAY_INDICIES:
                    weekday = DAY_INDICIES[weekday_string]
                else:
                    continue
                date_string = date_string[weekday_string + 1:]
                # TODO: update the hours
    except:
        return hours


class page_object:
    def __init__(self, name: str, time_of_day: str, hours: List[List[int]], menu_items: List[menu_item]) -> 'page_object':
        self.name = name
        self.time_of_day = time_of_day
        self.hours = hours
        self.menu_items = menu_items

    @classmethod
    def from_web_call(cls, dining_hall: str, time_of_day: str, page: Response) -> 'page_object':
        '''Create a page object directly from HTML'''
        soup = Soup(page.text, DEFAULT_PARSER)
        hours_soup = soup.find(id=HOURS_ID)
        menu = soup.find(id=MENU_ID)
        menu = [child for child in menu if type(child) is Tag]
        menu_items = list()
        for child in menu:
            menu_items.extend(parse_web_items(child))
        hours = parse_hours(hours_soup)
        return cls(dining_hall, time_of_day, hours, menu_items)
