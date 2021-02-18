from datetime import datetime, timedelta
from requests import get
from sdmenu.parser import page_object
from typing import Tuple

BASE_URL = 'https://hdh-web.ucsd.edu/dining/apps/diningservices/Restaurants/MenuItem'

DINING_HALLS = {
    '64 Degrees': '64',
    'Cafe Ventanas': '18',
    'Canyon Vista': '24',
    'Club Med': '15',
    'Foodworx': '11',
    'OceanView': '05',
    'Pines': '01',
    'Sixth College': '37',
    'The Bistro': '27'
}

ALLOWED_TIMES = {
    'Auto',
    'Breakfast',
    'Lunch',
    'Dinner'
}


def get_current_time() -> Tuple[int, int, int, int, int]:
    '''The current date and time of day'''
    now = datetime.utcnow() + timedelta(hours=-8)
    return now.year, now.month, now.day, now.weekday(), now.hour


def get_current_time_of_day():
    year, month, day, weekday, hour = get_current_time()
    if weekday > 0 or weekday < 6:
        if hour < 11:
            return 'Breakfast'
    else:
        if hour < 13:
            return 'Breakfast'
    if hour < 16:
        return 'Lunch'
    else:
        return 'Dinner'


class menu_cache:
    def __init__(self):
        self.year, self.month, self.day, weekday, hour = get_current_time()
        self.cache = dict()

    def needs_update(self) -> bool:
        '''Check if the combination needs an update'''
        year, month, day, weekday, hour = get_current_time()
        return self.year != year or self.month != month or self.day != day

    def get(self, dining_hall: str, time_of_day='Auto') -> page_object:
        '''Get a menu page, considering cache time'''
        if dining_hall not in DINING_HALLS:
            raise KeyError(f'{dining_hall} is not a known dining hall!')
        if time_of_day not in ALLOWED_TIMES:
            raise KeyError(
                f'{time_of_day} invalid, must be one of: Auto, Breakfast, Lunch, Dinner')
        if time_of_day == 'Auto':
            time_of_day = get_current_time_of_day()
        if dining_hall in self.cache:
            if time_of_day in self.cache[dining_hall]:
                return self.cache[dining_hall][time_of_day]
        return self.get_menu_page(dining_hall, time_of_day)

    def store_menu_page(self, dining_hall: str, time_of_day: str, page: page_object) -> None:
        '''Store menu page in cache'''
        if dining_hall not in self.cache:
            self.cache[dining_hall] = dict()
        self.cache[dining_hall][time_of_day] = page

    def get_menu_page(self, dining_hall: str, time_of_day='Auto') -> page_object:
        '''Returns a menu page for a given dining hall and time of day'''
        if dining_hall not in DINING_HALLS:
            raise KeyError(f'{dining_hall} is not a known dining hall!')
        if time_of_day not in ALLOWED_TIMES:
            raise KeyError(
                f'{time_of_day} invalid, must be one of: Auto, Breakfast, Lunch, Dinner')
        if time_of_day == 'Auto':
            time_of_day = get_current_time_of_day()
        if time_of_day in {'Breakfast', 'Dinner'}:
            # TODO: make POST request to change context and flush cache
            pass
        menu_page = get(f'{BASE_URL}/{DINING_HALLS[dining_hall]}')
        page = page_object.from_web_call(dining_hall, time_of_day, menu_page)
        self.store_menu_page(dining_hall, time_of_day, page)
        return page
