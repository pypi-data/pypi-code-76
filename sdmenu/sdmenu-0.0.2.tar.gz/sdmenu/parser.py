from requests.models import Response
from sdmenu.classes import menu_item
from typing import List


class page_object:
    def __init__(self, name: str, time_of_day: str, hours: List[List[int]], menu_items: List[menu_item]):
        self.name = name
        self.time_of_day = time_of_day
        self.hours = hours
        self.menu_items = menu_items

    @classmethod
    def from_web_call(cls, dining_hall: str, time_of_day: str, page: Response):
        '''Create a page object directly from HTML'''
        # TODO: Parse page
        hours = list()
        menu_items = list()
        return cls(dining_hall, time_of_day, hours, menu_items)
