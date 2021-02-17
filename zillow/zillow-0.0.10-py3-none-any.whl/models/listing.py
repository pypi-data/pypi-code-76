# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Pip
from jsoncodable import JSONCodable

# Local
from .address import Address
from .listing_features import ListingFeatures
from .price_history_entry import PriceHistoryEntry
from .listing_image import ListingImage
from .listing_video import ListingVideo
from .listing_area_size import ListingAreaSize

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Listing ------------------------------------------------------------ #

class Listing(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        details = d[list(d.keys())[1]]['property']
        self.zpid = details['zpid']
        address = details['address'] if 'address' in details else None

        self.address = Address(
            address['streetAddress'] if address and 'streetAddress' in address else None,
            address['city'] if address and 'city' in address else None,
            address['state'] if address and 'state' in address else None,
            address['zipcode'] if address and 'zipcode' in address else None,
            address['neighborhood'] if address and 'neighborhood' in address else None,
            address['community'] if address and 'community' in address else None,
            address['subdivision'] if address and 'subdivision' in address else None,
            details['latitude'] if 'latitude' in details else None,
            details['longitude'] if 'longitude' in details else None
        )

        self.bedrooms = details['bedrooms']
        self.bathrooms = details['bathrooms']
        self.price = details['price']
        self.price_estimate = details['zestimate']
        self.rent_estimate = details['rentZestimate']
        self.year_built = details['yearBuilt']
        self.description = details['description']
        self.type = details['homeType']

        self.area = ListingAreaSize(
            details['lotAreaValue'],
            details['lotAreaUnits'],
            details['lotSize'],
            details['livingArea'],
            details['livingAreaUnits'],
            details['livingAreaUnitsShort']
        )

        self.year_built = details['yearBuilt']
        self.schools_in_area = len(details['schools']) if 'schools' in details and details['schools'] else 0
        self.features = ListingFeatures(details['resoFacts'])

        self.price_history = [PriceHistoryEntry(e) for e in details['priceHistory']]
        self.price_history.reverse()
        details['responsivePhotosOriginalRatio']
        self.is_price_history_usable = True

        for e in self.price_history:
            if e.price_change_rate > 0.5 or e.price_change_rate < -0.5:
                self.is_price_history_usable = False

                break

        self.images = [ListingImage(e) for e in details['responsivePhotosOriginalRatio']]
        self.main_image = self.images[0] if len(self.images) > 0 else None

        self.video = ListingVideo(details['primaryPublicVideo']) if details['primaryPublicVideo'] else None


# ---------------------------------------------------------------------------------------------------------------------------------------- #