# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: ListingFeatures -------------------------------------------------------- #

class ListingFeatures(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        f: dict
    ):
        self.basement = f['basement']
        self.flooring = f['flooring'] if 'flooring' in f and f['flooring'] else []
        self.heating = f['heating'] if 'heating' in f and f['heating'] else []
        self.cooling = f['cooling'] if 'cooling' in f and f['cooling'] else []
        self.appliances = f['appliances'] if 'appliances' in f and f['appliances'] else []
        self.laundry_features = f['laundryFeatures'] if 'laundryFeatures' in f and f['laundryFeatures'] else []
        self.fireplace_features = f['fireplaceFeatures'] if 'fireplaceFeatures' in f  and f['fireplaceFeatures']else []
        self.furnished = f['furnished']
        self.parking_spots = f['parking']
        self.parking_features = f['parkingFeatures'] if 'parkingFeatures' in f  and f['parkingFeatures']else []
        self.has_garage = f['hasGarage']
        self.levels = f['stories']
        self.has_private_pool = f['hasPrivatePool']
        self.has_spa = f['hasSpa']

        self.has_view = f['hasView']
        self.has_waterfront_view = f['hasWaterfrontView']
        self.wooded_area = f['woodedArea']
        self.vegetation = f['vegetation']
        self.can_raise_horses = f['canRaiseHorses']
        self.other = {d['name']:d['value'] for d in f['otherFacts']}


# ---------------------------------------------------------------------------------------------------------------------------------------- #