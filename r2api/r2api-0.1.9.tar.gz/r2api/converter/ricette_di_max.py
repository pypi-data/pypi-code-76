import re
from bs4 import BeautifulSoup

from .base_converter import BaseConverter
from ..utilities.unit_conversion import (
    convert_units_prep,
    convert_units_name,
    convert_units_ing,
    float_dot_zero
)


class RMConverter(BaseConverter):
    """
    This class will take a URL of a recipe on a Giallo Zafferano blog (developed for Molliche di Zucchero) and produce a dictionary accessible at .recipe with the following qualities
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list of the following format
        [string(name), float(quantity), string(unit)]
    recipe['preparation']: list of the steps to make the recipe
    """

    def get_title(self, soup):
        return soup.find('title').text

    def get_image(self, soup):
        imgs = soup.find_all('img')
        final_image = ''
        for img in imgs:
            title_in_src = re.search(r'\/([\w-]+)\.\w+$', img['src'])
            if title_in_src:
                potential_match = title_in_src.groups()[0].replace('-', ' ')
                if potential_match.lower() in soup.find('title').text.lower():
                    final_image = img['src']
        # if not final_image:
        #     # It seems like the image is always the second in the page
        #     # So it can be a fallback
        #     try:
        #         final_image = imgs[1]['src']
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
        # This website is, by far, the least organized and most chaotic of any
        # recipe blog that I have parsed so far. Not only are there two blatant formats
        # by which it's labelled, there are other inconsistencies.
        # I have tried to account for them as best as possible
        ingredients_container = soup.find("div", {"class": "recipe-ingredients-content"})

        ingredients = []

        # Format #1
        if ingredients_container:
            ingredients = self._get_ingredients_style_1(ingredients_container)
        else:
            # Format #2
            uls = soup.find_all("ul")
            # We are looking for the first UL that does not have a class
            candidates = [ul for ul in uls if "class" not in ul.attrs]
            ingredients = self._get_ingredients_style_2(candidates[0])
        
        if convert_units:
            ingredients = [self._translate_ingredient(name, quantity, unit)
                for name, quantity, unit in ingredients]

        return ingredients
    
    def _get_ingredients_style_1(self, ingredients_container):
        """Parses the ingredients according to the first style of the blog"""
        ingredients_divs = ingredients_container.find_all("div", {"class", "recipe-ingredient-item"})
        ing_unprocessed = []

        for ing in ingredients_divs:
            _ing = []
            for span in ing.find_all('span'):
                _ing.append(span.text.strip())
            ing_unprocessed.append(_ing)

        # At this point, we'll have one of the following three varieties:
        # NOTE: the final group doesn't matter, whether it contains anything or not
        # 1. '400 g', 'Tortellini', '(di carne macinata)'
        # 2. '1', 'confezione di Panna di cucina', ''
        # 3. 'q.b.', 'Sale', ''
        # > normal_quantity_unit (the first if statement) checks for 1.
        # and splits 400 g into quantity and unit, everything else is part of the name
        # > the else condition handles 2 and 3
        # and splits the first part into the quantity and then gives n/a for unit
        ing_final = []
        for ing in ing_unprocessed:
            normal_quantity_unit = re.search(r'([0-9]+)\s([a-zA-Z]+)', ing[0])
            if normal_quantity_unit:
                quantity = normal_quantity_unit.groups()[0]
                unit = normal_quantity_unit.groups()[1]
            else:
                quantity = ing[0]
                unit = 'n/a'
            name = ing[1]
            if re.search(",[a-zA-Z]", ing[1]):
                name = name.replace(",", ", ")
            if ing[2]:
                name += f" {ing[2]}"
            ing_final.append([name, quantity, unit])
        return ing_final

    def _get_ingredients_style_2(self, ingredients_container):
        """Parses the ingredients according to the second style of the blog"""
        ingredients_li = ingredients_container.find_all("li")

        # So far I have come across the following possible arrangements of the recipe
        # NOTE: All of these are singular strings and not split into 
        # 1. 300 g di salsa di pomodoro già cotta
        # 2. 4 melanzane medie (circa 1 kg e 200 g)
        # 3. foglie di basilico
        # > normal_unit_quantity checks for the first condition, isolating
        # the quantity and unit
        # > only_quantity identifies the second condition, identifying the
        # quantity and outputting the unit as n/a
        # > else handles situation three, in which case quantity and unit are n/a
        final_ing = []
        for ing in ingredients_li:
            normal_quantity_unit = re.search(r'^(\d+)\s?([dDmMkK]?[gGlL])\s', ing.text)
            if normal_quantity_unit:
                quantity = normal_quantity_unit.groups()[0]
                unit = normal_quantity_unit.groups()[1]
                # We remove the quantity from the string before handing it to the name
                name = ing.text.replace(quantity, "").strip()
                # Instead of replacing the unit everywhere, we just remove it from
                # the beginning
                name = name[len(unit):].strip()
            else:
                only_quantity = re.search(r'(\d+)\s', ing.text)
                if only_quantity:
                    # This is similar to normal_quantity_unit
                    quantity = only_quantity.groups()[0]
                    unit = "n/a"
                    name = ing.text.replace(quantity, "").strip()
                else:
                    # By far the easiest situation
                    quantity = "n/a"
                    unit = "n/a"
                    name = ing.text.strip()
            # For case 1 and 2, we sometimes have "di ", meaning "of " at
            # the beginning of the ingredient. We therefore we remove it
            if "di " in name[:3]:
                name = name[3:]
            final_ing.append([name, quantity, unit])
        return final_ing

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
        # At this point we must identify where the preparation begins
        # Unlike other recipes, the preparation is sometimes NOT nested within a div
        # I have witnessed it inside of an h2, an h3 and a p element
        # In those cases where the preparation is nested, the other
        # solution works just as well
        desired = ""
        h2s = soup.find_all("h2")
        for h2 in h2s:
            if 'Ricetta' in h2.text \
                or 'Preparazione' in h2.text \
                or 'Procedimento' in h2.text:
                desired = h2
        if not desired:
            h3s = soup.find_all("h3")
            for h3 in h3s:
                if 'Ricetta' in h3.text \
                    or 'Preparazione' in h3.text \
                    or 'Procedimento' in h3.text:
                    desired = h3
        if not desired:
            ps = soup.find_all("p")
            for p in ps:
                if 'Ricetta' in p.text \
                    or 'Preparazione' in p.text \
                    or 'Procedimento' in p.text:
                    desired = p
        
        # Because it's not nested, we are looking for all p elements
        # that come afterword
        prep_p = desired.find_all_next("p")
        # From this point on, it's fairly uniform
        # Two google ads (that will have the attribute align="CENTER")
        counter = 0
        final_prep = []
        for p in prep_p:
            if 'align' in p.attrs:
                counter += 1
                continue
            if counter == 2:
                break
            else:
                prep = p.text.replace('\n', '').replace('\r', '')
                if prep != '':
                    final_prep.append(p.text)
        if convert_units:
            final_prep = [convert_units_prep(p) for p in final_prep]
        return final_prep
