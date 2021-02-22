import re
from bs4 import BeautifulSoup

from .base_converter import BaseConverter
from ..utilities.unit_conversion import (
    convert_units_prep,
    convert_units_name,
    convert_units_ing,
    float_dot_zero
)


class AGConverter(BaseConverter):
    """
    This class will take a URL of a recipe on a Giallo Zafferano blog (developed for Molliche di Zucchero) and produce a dictionary accessible at .recipe with the following qualities
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list of the following format
        [string(name), float(quantity), string(unit)]
    recipe['preparation']: list of the steps to make the recipe
    """

    def get_title(self, soup):
        return soup.find("title").text

    def get_image(self, soup):
        imgs = soup.find_all("img")
        title = soup.find("title").text.lower()
        # We'll have a fallback so the converter doesn't crash
        final_image = ""
        # One of the images will have the following classes,
        # and we want that one's src attribute
        for img in imgs:
            if 'alt' in img.attrs and img.attrs['alt'].lower() in title and img.attrs['alt'] != "":
                final_image = img.attrs['src']
        return final_image

    def get_ingredients(self, soup, convert_units = True):
        """
        Pass a BeauitfulSoup comprehension of an appropriate recipe and get in return a list of the following format:
        [
            [ingredient name, ingredient quantity, ingredient unit],
            [ingredient name, ingredient quantity, ingredient unit],
            etc.
        ]
        The units and quantities will have been converted from metric to imperial units if convert_units is True
        """
        # The soup will contain a ul element that contains divs, each of which contains
        # three spans which contains the three span elements of the ingredients
        ingredients_ul = soup.find("div", {"class": "recipe-ingredients-content"})
        ingredients_item = ingredients_ul.find_all("div", {"class": "recipe-ingredient-item"})
        
        # From this point on, I discovered that recipes on the blog are
        # of two, moderately different styles
        # Presumably, they were written at different times or in different formats
        # I either had two choices: create two converters or find a way for one converter
        # to get them both work

        # It turns out, after studying it, that a lot of things were shared.
        # The main differences were in the ingredient parsing
        # It also made me implement a correct method of finding the image

        # For website style #1:
        # e.g. https://blog.giallozafferano.it/allacciateilgrembiule/torta-salata-con-prosciutto/
            # This loop will get the spans' content for processing down below
            # They will be one of the following three configurations:
            # Possibility 1: ['1 rotolo', 'Pasta Sfoglia', '(o brisee o pasta matta)']
            # Possibility 2: ['200 g', 'Prosciutto cotto', '']
            # Possibility 3: ['', 'Latte', '']

        # For website style #2:
        # e.g. https://blog.giallozafferano.it/allacciateilgrembiule/uova-alla-garibaldina/
            # This loop will get the spans' content for processing down below
            # They will be one of the following three configurations:
            # Possibility 1: ['4', 'uova']
            # Possibility 2: ['500', 'ml', 'pomodori pelati']
            # Possibility 3: ['', 'Prezzemelo']

        ing_total = []
        for item in ingredients_item:
            ing_spans = []
            for span in item.find_all("span"):
                # The need to look for spans in spans was because of recipes in group #2
                # Because such a recipe has needlessly nested spans
                if not span.find("span"):
                    ing_spans.append(span.text.strip())
            ing_total.append(ing_spans)

        # For style #1:
            # There will be either three items in each ingredient
            # based on the above-mentioned possibilities
            # ing[0]: (quantity unit) OR empty string
            # ing[1]: ingredient name
            # ing[2]: ingredient note OR empty string

            # ing[0] will only be an empty string if ing[2]
            # is also an empty string
            # ing[2] can be an empty string regardless of anything else
        
        # For style #2:
            # 
        ingredients = []
        for ing in ing_total:
            # This if condition splits off possibility 1/2 and possibility 3
            # of either style - if = possibility 1/2, else = possibility 3
            if ing[0] != "":
                # If we do have it, we need to separate the elements
                # Note: \w includes digits too, so I needed to change it
                ing_u_q = re.search(r"(\d*)\s?([a-zA-Z]+)", ing[0])
                # The following condition will only be true for style #1
                if ing_u_q and ing_u_q.groups()[0]:
                    quantity = ing_u_q.groups()[0]
                    unit = ing_u_q.groups()[1]
                else:
                    # We have a style #2, which is pretty simple to break down
                    # We're just handed everything
                    if len(ing) > 2:
                        # This is possibility #2
                        quantity = ing[1]
                        unit = ing[0]
                        name = ing[2]
                    else:
                        # This is possibility #1
                        quantity = ing[0]
                        unit = "n/a"
                        name = ing[1]
                    # We end the current iteration here
                    # because there are no notes, and the way it's set up
                    # will disrupt how style #2 breaks down the recipe
                    ingredients.append([name, unit, quantity])
                    continue
            else:
                # We have possibility 3 of either style
                unit = "n/a"
                quantity = "n/a"
            # There will always be a name
            name = ing[1]
            # Sometimes there will be a note (possibility 1)
            if len(ing) > 2 and ing[2]:
                # We just append it to the name
                name += f" {ing[2]}"
            ingredients.append([name, quantity, unit])
        
        if convert_units:
            # I outsourced this method to make things easier
            ingredients = [self._translate_ingredient(name, quantity, unit)
                for name, quantity, unit in ingredients]
            
        return ingredients

    def _translate_ingredient(self, name, quantity, unit):
        """
        Converts a name, quantity and unit from metric to imperial units
        """
        # There are two parts of the conversion
        # 1. the name conversion
        # 2. the quantity and unit conversion
        #   these last two are married because it requires both to know
        #   how the conversion must be done
        _name = convert_units_name(name)
        _quantity, _unit = convert_units_ing(quantity, unit)
        if float_dot_zero(_quantity):
            # This is the best and only spot to knock off the .0
            # since it will be created by the conversion util functions
            _quantity = int(_quantity)
        return [_name, _quantity, _unit] 

    def get_preparation(self, soup, convert_units=True):
        """
        This function takes a soup of an appropriate recipe and returns the steps made into a list.
        Ingredients and units are converted from metric to imperial if convert_units is True
        """
        steps = soup.find("div", {"class": "recipe-steps"})

        # Thankfully the prep is extraordinarily simple
        prep_p = [step.text for step in steps.find_all("p")]
        if convert_units:
            prep_p = [convert_units_prep(p) for p in prep_p]
        return prep_p
