from sdmenu.classes import menu_item
from sdmenu.webworker import menu_cache
from typing import List


class menu:
    def __init__(self) -> 'menu':
        self.cache = menu_cache()

    def get(self, dining_hall: str, time_of_day='Auto') -> List[menu_item]:
        '''Get a restaurant menu'''
        data = self.cache.get(dining_hall, time_of_day)
        return data.menu_items

    def has(self, dining_hall: str, item: str, time_of_day='Auto') -> bool:
        '''Whether or not the restaurant has the item at the moment'''
        data = self.cache.get(dining_hall, time_of_day)
        for dish in data.menu_items:
            if dish.name == item:
                return True
        return False
