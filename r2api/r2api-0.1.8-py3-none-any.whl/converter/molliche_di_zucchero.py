from bs4 import BeautifulSoup

from .base_converter import BaseConverter
from ..utilities.unit_conversion import (
    convert_units_prep,
    convert_units_name,
    convert_units_ing,
    float_dot_zero
)


class MZConverter(BaseConverter):
    """
    This class will take a URL of a recipe on a Giallo Zafferano blog (developed for Molliche di Zucchero) and produce a dictionary accessible at .recipe with the following qualities
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list of the following format
        [string(name), float(quantity), string(unit)]
    recipe['preparation']: list of the steps to make the recipe
    """

    def get_title(self, soup):
        return soup.find('title').text.strip()

    def get_image(self, soup):
        return self._find_image(soup.find_all('img'))

    def _find_image(self, imgs):
        for img in imgs:
            try:
                if 'wp' in img['class'][0]:
                    return img['src']
            except:
                pass

    def get_ingredients(self, soup, convert_units=True):
        """
        Pass a BeauitfulSoup comprehension of an appropriate recipe and get in return a list of the following format:
        [
            [ingredient name, ingredient quantity, ingredient unit],
            [ingredient name, ingredient quantity, ingredient unit],
            etc.
        ]
        The units and quantities will have been converted from metric to imperial units if convert_units is True
        """
        # We would not be able to proceed whatsoever
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("expected argument soup to be of type bs4.BeautifulSoup")

        ingredients_div = soup.find('div', {'class': 'recipe-ingredients'})
        all_items = ingredients_div.find_all(
            'div', {'class': 'recipe-ingredient-item'})
        sections = ['name', 'number', 'unit']
        ingredients = [[self._get_ingredient_final(
            section, item) for section in sections] for item in all_items]

        # The above two lines replaced the following 8 lines:
        # Another solution could involve itertools.product, but nested list comprehensions seemed easier
        # ingredients = []
        # sections = ['name', 'number', 'unit']
        # for item in all_items:
        #     ing = []
        #     for section in sections:
        #         ing.append(self._get_ingredient_final(section, item))
        #     ingredients.append(ing)

        special_words = {
            'q.b.': 'to taste',
            'q.s.': 'to taste',
            'a piacere': 'to taste'
        }

        if convert_units:
            converted_units = []
            for ingredient in ingredients:
                # Ingredient[0] - Name
                # Ingredient[1] - Quantity
                # Ingredient[2] - Unit
                converted_name = convert_units_name(ingredient[0])
                # If the quantity is n/a then it cannot be converted
                if ingredient[1] != 'n/a':
                    converted_quantity, converted_unit = convert_units_ing(
                        ingredient[1], ingredient[2])
                else:
                    converted_quantity, converted_unit = ingredient[1], ingredient[2]
                
                # Checking for vulgar fractions and special words
                if converted_unit in special_words:
                    converted_unit = special_words[converted_unit]
                # One last check for a float_dot_zero conversion
                if float_dot_zero(converted_quantity):
                    # Note: this is only happening in the conversion because
                    # the units already nice and round before the conversion
                    converted_quantity = int(converted_quantity)
                converted_units.append(
                    [converted_name, converted_quantity, converted_unit])
            ingredients = converted_units
        # float_dot_zero only comes up if the ingredient quantity has been converted
        return ingredients

    def _get_ingredient_final(self, ing_part, item):
        """
            Sub-method to extract the ingredient text
            It is iterated through on each ingredient and in three sections:
            name, number and ingredient, corresponding with the div class names
            and coincidentally what we want (the website APIs often match ours partly)
        """
        especially_vulgar_fractions = {
            '¼': '1/4',
            '½': '1/2',
            '¾': '3/4',
            '⅓': '1/3',
            '⅔': '2/3'
        }

        # Note: Other converters identified and converted name, ingredient and quantity
        # through the same iteration loop. This converter doesn't do the same
        # And so it cannot put the unit at n/a and the quantity at q.b here.
        ing_text = item.find(
            'span', {'class': f'recipe-ingredient-{ing_part}'})
        if ing_text:
            ing_text = ing_text.text.strip()
            # Without the separation into name/quantity/unit
            # This is probably the best place to do the conversion
            if ing_text in especially_vulgar_fractions:
                ing_text = especially_vulgar_fractions[ing_text]
        else:
            ing_text = 'n/a'
        return ing_text

    def get_preparation(self, soup, convert_units=True):
        """
        This function takes a soup of an appropriate recipe and returns the steps made into a list.
        Ingredients and units are converted from metric to imperial if convert_units is True
        """
        # We would not be able to proceed whatsoever
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("expected argument soup to be of type bs4.BeautifulSoup")

        recipe_instructions = soup.find(
            'div', {'class': 'recipe-instructions-group'})
        instructions_divs = recipe_instructions.find_all(
            'div', {'class': 'instruction-text'})
        instructions_text = [i.find('p').text.strip()
                             for i in instructions_divs]
        instructions_text = instructions_text[:-1]
        if convert_units:
            instructions_text = [convert_units_prep(instruction)
                for instruction in instructions_text]
        return instructions_text
