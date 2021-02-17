# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Address ------------------------------------------------------------ #

class Address(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        neighborhood: Optional[str],
        community: Optional[str],
        subdivision: Optional[str],
        lat: float,
        lon: float
    ):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = int(zip_code) if zip_code else None
        self.neighborhood = neighborhood
        self.community = community
        self.subdivision = subdivision
        self.coordinates = Coordinate(lat, lon)


# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Coordinate ----------------------------------------------------------- #

class Coordinate(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        lat: float,
        lon: float
    ):
        self.latitude = lat
        self.longitude = lon


# ---------------------------------------------------------------------------------------------------------------------------------------- #