import pprint
from typing import List

import requests
from dataclasses import dataclass
import re
from urllib.parse import unquote
import html


@dataclass
class Recipe:
    """ A dataclass to represent a recipe returned by the API
    Fields:
        title: title of the recipe
        href: link to a web page containing the entire recipe
        ingredients: the list of ingredients used in the recipe
        thumbnail_href: link to a thumbnail photo with the result of the recipe
    """
    title: str
    href: str
    ingredients: List[str]
    thumbnail_href: str

    def __init__(self, title: str, href: str, ingredients: List[str], thumbnail_href: str):
        self.title = title
        self.href = href
        self.ingredients = ingredients
        self.thumbnail_href = thumbnail_href


class RecipePuppy(object):
    def __init__(self):
        self.base_url = 'http://www.recipepuppy.com/api/'
        self.max_pages = 100

    def _decode_href(self, href: str) -> str:
        decoded_href = unquote(href)
        decoded_href = re.sub('\\\/', '/', decoded_href)
        return decoded_href

    def _parse_ingredients(self, raw_ingredients: str) -> List[str]:
        ingredients = raw_ingredients.split(',')
        return list(map(lambda x: html.unescape(x.strip()), ingredients))

    def _process_response(self, resp: requests.Response) -> List[Recipe]:
        resp_json = resp.json()
        raw_recipes = resp_json.get('results', None)
        if not raw_recipes:
            return []
        processed_recipes = []
        for raw_recipe in raw_recipes:
            recipe = Recipe(
                title=html.unescape(raw_recipe['title'].strip()),
                href=self._decode_href(raw_recipe['href']),
                ingredients=self._parse_ingredients(raw_recipe['ingredients']),
                thumbnail_href=self._decode_href(raw_recipe['thumbnail'])
            )
            processed_recipes.append(recipe)
        return processed_recipes

    def get_recipes(self, ingredients='', search_query='') -> List[Recipe]:
        """ queries the API to return the recipes containing a given list of ingredients and/or a given search term
        Args:
            ingredients: comma delimited ingredients
            search_query: normal search query
        Returns:
            The list of recipes returned by the API
        """
        params = {}
        if ingredients:
            params['i'] = ingredients
        if search_query:
            params['q'] = search_query
        if 'i' not in params and 'q' not in params:
            return []

        all_recipes = []
        for page in range(1, self.max_pages):
            params['p'] = page
            try:
                resp = requests.get(self.base_url, params=params)
            except Exception as e:
                print(f'The following exception occurred during the request: {str(e)}')
                return all_recipes
            if not resp or resp.status_code != 200:
                return all_recipes
            recipes_current_page = self._process_response(resp)
            if not recipes_current_page:
                return all_recipes
            all_recipes += recipes_current_page
        return all_recipes
