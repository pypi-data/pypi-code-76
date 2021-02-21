


from kraken_html.html_table import Html_table
from kraken_html.html_record import Html_record
from kraken_html.html_card import Html_card

from kraken_html.html_section import Html_section
from kraken_html.html_bootstrap import Html_bootstrap
from kraken_html.html_navbar import Html_navbar


#from models.html_form import Html_form


class Kraken_html:

    def __init__(self):


        self.nav = []
        self.title_nav = None

        self.input_record = {}

        self.input_records = []

        self._keys = []


    @property
    def keys(self):
        
        if self._keys:
            return self._keys

        else:
            return self._get_keys(self.value)


    @keys.setter
    def keys(self, value):

        self._keys = value


    def table(self, value = None):

        if value:
            self.value = value

        html_table = Html_table()

        return html_table.table(self.keys, self.value)


    def record(self, value):

        if value:
            self.value = value


        html_record = Html_record()

        return html_record.record(self.keys, self.value)




    def form(self, value):

        if value:
            self.value = value

        return 


    def cards(self, value = None):

        if value:
            self.value = value


        html_card = Html_card()

        return html_card.cards(self.value)



    def section(self, title, content):




        html_section = Html_section()

        return html_section.section(title, content)




    def bootstrap(self, nav, title, content):

        html_bootstrap = Html_bootstrap()

        return html_bootstrap.bootstrap(nav, title, content)




    def navbar(self, title, value):

        html_navbar = Html_navbar()

        return html_navbar.navbar(title, value)



    def page(self, content = ''):

        
        
        html_nav = self.navbar('Test title', self.nav)


        content = self.bootstrap(html_nav, self.title_nav, content)

        return content



    def _get_keys(self, value):

        if not isinstance(value, list):
            value = [value]

        keys = []

        for i in value:
            for key in i:
                if key not in keys:
                    keys.append(key)

        return keys