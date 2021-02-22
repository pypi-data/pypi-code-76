import re
from bs4 import BeautifulSoup

from .base_converter import BaseConverter
from ..utilities.unit_conversion import (
    convert_units_prep,
    convert_units_name,
    convert_units_ing,
    float_dot_zero
)

class FCConverter(BaseConverter):
    """
    This class will take a URL of a Fatto in Casa da Benedetta recipe and produce a dictionary accessible at .recipe with the following qualities:
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list of the following format
        [string(name), float(quantity), string(unit)]
    recipe['preparation']: list of the steps to make the recipe

    The methods write_soup_to and write_recipe_to writes the soup and recipe respectively to the path passed in their arguments, the former as the BS4 object prettified, the latter as a JSON object

    Optional parameters: convert_units: bool = True
    If True, units and their quantities in both ingredients and preparation will be converted into American imperial units. If False, they will not be converted
    """
    def get_title(self, soup):
        return soup.find('title').text.strip().replace("\n", "")

    def get_image(self, soup):
        return soup.find('img', {'id': 'top-img'}).attrs['src']

    def get_ingredients(self, soup, convert_units = True):
        """
        Pass a BeauitfulSoup of a Fatto in Casa recipe and get in return a list of the following format:
        [
            [ingredient name, ingredient quantity, ingredient unit],
            [ingredient name, ingredient quantity, ingredient unit],
            etc.
        ]
        The units and quantities will have been converted from metric to imperial units if convert_units is True.
        """
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("expected argument soup to be of type bs4.BeautifulSoup")
        
        # This will identify the LIs, each of which contains the quantity, unit and name of the ingredient
        ing_elements = soup.find_all('li', {'class': 'wpurp-recipe-ingredient'})
        ingredients = []
        for element in ing_elements:
            quantity = element.find('span', {'class': 'wpurp-recipe-ingredient-quantity'}).text
            unit = element.find('span', {'class': 'wpurp-recipe-ingredient-unit'}).text
            # Unlike quantity and unit, the name may include a span
            # with a note or a particular qualifier; if we add the .text method then
            # the span element will get flattened into it
            name = element.find('span', {'class': 'wpurp-recipe-ingredient-name'})
            children = name.findChildren()
            # If there are any children, they will either be:
            # A note or a quantity (5 o 6) 
            # The note will be handled later.
            # The quantity will have a digit in it, hence the RegEx
            if len(children) > 0 and re.search(r'\d+', children[0].text):
                # The first child's text will be the quantity
                # i.e. (5 o 6) in this particular case
                try:
                    float(quantity)
                except:
                    quantity = children[0].text
                # If there are parentheses, then this will get rid of them
                quantity = quantity.replace("(", "").replace(")", "")

                name = name.text
                # We remove the quantity from the name and any extra ()
                name = name.replace(quantity, '').replace('(', '').replace(')', '')

            # If it doesn't have that quality, it is the default case
            # And we don't need to do anything special
            else: name = name.text

            # Testing if there is a special word
            # Unlike GZConverter, the q.b./a piacere will show up in the name
            special_words = {'q.b.':'to taste', 'a piacere':'to taste'}
            for word in special_words:
                if word in name:
                    name = name.replace(word, '')
                    quantity = special_words[word]
            # If nothing came up for units, it will be n/a because
            # a unit is necessary
            if not unit or len(unit) == 0:
                unit = 'n/a'
            # Idem with quantity
            if len(quantity) == 0:
                quantity = 'n/a'
            name = name.strip()

            # 'di' in Italian means 'of, as in 'two tablespoons OF vanilla extract'
            # Occasionally it shows up in the name because of
            # how we've parsed the sentence; it can be removed without changing the meaning
            if name[:3] == "di ":
                name = name[3:].capitalize()

            # If convert_units is set to False, this is skipped
            if convert_units:
                quantity, unit = convert_units_ing(quantity, unit)
                name = convert_units_name(name)

            # If we have a quantity like 1.0 (which should not happen with this recipe)
            # then we convert it to 1
            if float_dot_zero(quantity):
                quantity = int(quantity)

            ingredients.append([name, quantity, unit])
        return ingredients

    def get_preparation(self, soup, convert_units = True):
        """
        This function takes a soup of a Fatto in Casa recipe and returns the steps made into a list.
        Ingredients and units are converted from metric to imperial if convert_units is True
        """
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("expected argument soup to be of type bs4.BeautifulSoup")

        elements = soup.find_all("li", {"class": "wpurp-recipe-instruction"})
        prep = []
        for step in elements:
            temp = step.text.strip().replace("\n", " ")
            if convert_units:
                # If convert_units is set to False, this is skipped
                temp = convert_units_prep(temp)
            if len(temp) > 0:
                # Occasioaly these will be empty and can be safely discarded
                prep.append(temp)
        return prep

