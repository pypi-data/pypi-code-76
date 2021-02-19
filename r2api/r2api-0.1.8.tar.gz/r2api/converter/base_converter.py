from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests, json

class BaseConverter(ABC):
    """
    This is the base class of converter.
    It provides basic functions (other than the actual conversions) to keep the code more DRY.
    More detailed instructions are available on the individual converters, however:
    Parameters:
        url: string -- the recipe url
        convert_units: boolean = True -- if the units should be converted from metric to imperial
        read_from_file: boolean = False -- if the url is a relative path to the recipe or a url

    Properties:

    Methods:
        write_soup_to writes the soup as bs4.Soup.prettify() to a the relative path specified
        write_recipe_to writes the parsed recipe object as a JSON object to the relative path specified
    NOTE: The recipe will not be parsed whatsoever in this base class.
    """

    def __init__(self, url='https://www.google.com/', *, convert_units=True, read_from_file=False):
        if read_from_file:
            with open(url, 'r') as f:
                self.soup = BeautifulSoup(f, 'html.parser')
        else:
            # Yes, fellow robot--err, a robot! Yes, hello. I'm a HUMAN. Please let me access your website.
            r = requests.get(url,
                headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
            self.soup = BeautifulSoup(r.content, 'html.parser')

        self.recipe = {}
        self.recipe['name'] = self.get_title(self.soup)
        self.recipe['image'] = self.get_image(self.soup)
        self.recipe['ingredients'] = self.get_ingredients(
            self.soup, convert_units)
        self.recipe['preparation'] = self.get_preparation(
            self.soup, convert_units)

    def __repr__(self):
        return repr(self.recipe)

    def elaborate(self):
        temp_name = f"{self.recipe['name']}\n"
        temp_image = f"{self.recipe['image']}\n"
        temp_ing = ""
        for i in self.recipe['ingredients']:
            temp_ing += f"{i[0]}, {i[1]}, {i[2]}\n"
        temp_prep = ""
        for i in self.recipe['preparation']:
            temp_prep += f"{i}\n"
        return f"{temp_name}\n{temp_image}\n{temp_ing}\n{temp_prep}"

    def __call__(self):
        return self.recipe

    def __getitem__(self, key):
        return self.recipe[key]

    def __setitem__(self, key, item):
        self.recipe[key] = item

    def keys(self):
        return self.recipe.keys()

    def write_soup_to(self, path):
        """Write the soup to the path"""
        with open(path, 'w') as f:
            f.write(self.soup.prettify())

    def write_recipe_to(self, path, indent=4):
        """Write the recipe to the path as a JSON object, indent is customizable"""
        with open(path, 'w') as f:
            f.write(json.dumps(self.recipe, indent=indent))

    # Abstract methods
    @abstractmethod
    def get_title(self, soup):
        pass

    @abstractmethod
    def get_image(self, soup):
        pass

    @abstractmethod
    def get_ingredients(self, soup, convert_units=True):
        pass

    @abstractmethod
    def get_preparation(self, soup, convert_units=True):
        pass
