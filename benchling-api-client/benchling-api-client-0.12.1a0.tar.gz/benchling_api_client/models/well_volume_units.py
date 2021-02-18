from enum import Enum


class WellVolumeUnits(str, Enum):
    PL = "pL"
    NL = "nL"
    UL = "uL"
    ML = "mL"
    L = "L"

    def __str__(self) -> str:
        return str(self.value)
