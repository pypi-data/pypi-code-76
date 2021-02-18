from enum import Enum


class ProductionLevel(Enum):
    DEV = "dev"
    BETA = "beta"
    PROD = "prod"


class VadeSpotType(Enum):
    CURBSPACE = "curbspace"
    STANDARD = "standard"

    @staticmethod
    def from_str(str_val: str):
        if str_val == VadeSpotType.STANDARD.value:
            return VadeSpotType.STANDARD
        if str_val == VadeSpotType.CURBSPACE.value:
            return VadeSpotType.CURBSPACE
        return None

