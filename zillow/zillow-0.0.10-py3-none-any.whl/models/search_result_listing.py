# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Pip
from jsoncodable import JSONCodable

# Local
from .address import Address

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: SearchResultListing ------------------------------------------------------ #

class SearchResultListing(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        self.id = int(d['id'])
        self.zpid = int(d['zpid'])
        self.status_type = d['statusType']
        self.price = d['unformattedPrice']
        self.beds = d['beds']
        self.baths = d['baths']
        self.has_video = d['hasVideo']
        self.is_zillow_owned = d['isZillowOwned']
        self.url = 'https://www.zillow.com/homedetails/{}_zpid'.format(self.zpid)

        try:
            self.address = Address(
                d['addressStreet'],
                d['addressCity'],
                d['addressState'],
                d['addressZipcode'],
                None, None, None,
                d['latLong']['latitude'], d['latLong']['longitude']
            )
        except:
            self.address = None


# ---------------------------------------------------------------------------------------------------------------------------------------- #