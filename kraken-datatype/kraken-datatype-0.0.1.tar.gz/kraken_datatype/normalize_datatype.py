
import email_normalize
import pycountry
from url_normalize import url_normalize
import dateparser
import datetime
from cleanco import prepare_terms, basename


class Normalize_datatype:
    
    def __init__s(self, value = None):

        self.value = value



    def date(self, value = None):
        if value:
            self.value = value

        if not isinstance(self.value, datetime.datetime):

            self.value = dateparser.parse(self.value, settings={'RETURN_AS_TIMEZONE_AWARE': True})
        
        return self.value



    def url(self, value):

        if value:
            self.value = value

        return url_normalize(self.value)



    def email(self, value):

        if value:
            self.value = value

        return email_normalize.normalize(value).normalized_address


    def country(self, value = None):

        if value:
            self.value = value


        return pycountry.countries.search_fuzzy(self.value)[0].alpha_2


    def organization(self, value = None):

        terms = prepare_terms()
        return basename(value, terms, prefix=False, middle=False, suffix=True)

