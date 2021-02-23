"""Derive Solar Irradiance from various data sources."""
import numpy as np
from pint import UnitRegistry
from datetime import date
import pandas as pd
import csv
from ..Tools import get_data_file


__author__ = "Niklas Bohn, Andre Hollstein"


class SolarIrradiance:
    def __init__(self, dataset="Thuillier2002", used_date=date.today()):
        """ General object for solar constant computations
        dataset: Irradiance dataset to use, either: Thuillier2002 or Fontenla
        used_date: datetime object, for sun earth distance correction
        """
        self.sol_irr = {}
        self.ureg = UnitRegistry()  # for unit conversion
        self.Q_ = self.ureg.Quantity
        self.wvl = None
        self.irr = None
        self.dataset = dataset
        self.rp = None  # actual sun earth distance
        self.rc = None  # distance of reference
        self.cc = None  # c parameter for solar irradiance model

        assert isinstance(used_date, date), "Used date should be datetime date object."
        self.date = used_date

        if self.dataset == "Thuillier2002":
            path_thuillier = get_data_file("sicor", "Solar_irradiance_Thuillier_2002.xls")
            print(path_thuillier)
            self.irr_unit = 'mW/m**2/nm'
            self.sol_irr["Thuillier2002"] = (lambda x: {"ref_day": date(1982, 5, 5),
                                                        "ref_dist": 1.0,
                                                        "wvl": x[:, 0],
                                                        "irr": self.Q_(x[:, 1], 'mW/m**2/nm')}
                                             )(
                np.array(pd.read_excel(path_thuillier, sheet_name="Thuillier 2002"), dtype=float))
        elif self.dataset == "Fontenla":
            path_fontenla = get_data_file("sicor", "SUNp1fontenla.asc")
            self.irr_unit = 'mW/m**2/nm'
            self.sol_irr["Fontenla"] = (lambda x: {"ref_dist": 1,  # AU as given in the doc
                                                   "wvl": 10e6 / x[::-1, 0],  # given in cm-1, converted to nm
                                                   "irr": self.Q_(x[::-1, 1] * x[::-1, 0] ** 2, 'W/cm**2/cm')}
                                        # given in (W CM-2 / CM-1), conversion by v*2*L
                                        )(np.loadtxt(path_fontenla, skiprows=2))
        else:
            raise ValueError("Dataset not implemented: %s" % dataset)

        path_earth_sun_distance = get_data_file("sicor", "Earth_Sun_distances_per_day_edited.csv")
        with open(path_earth_sun_distance, 'r') as csvfile:
            self.sun_earth_dist = {row[0].replace(" ", ""): float(row[1]) for row in csv.reader(csvfile, delimiter=',')}

        assert type(used_date) == date, "Used date should be datetime date object."
        self.date = used_date

        self.wvl = self.sol_irr[self.dataset]["wvl"]

        if self.sun_earth_dist is not None:
            # simple quadratic model S(r)=c/r^2
            self.rp = self.sun_earth_dist[str(self.date)]
            self.rc = self.sol_irr[self.dataset]["ref_dist"]
            self.cc = self.sol_irr[self.dataset]["irr"].to(self.irr_unit).magnitude * self.rc ** 2
            self.irr = self.cc / self.rp ** 2
        else:  # no correction for distance
            self.irr = self.sol_irr[self.dataset]["irr"].to(self.irr_unit).magnitude

    def __call__(self):
        return self.irr
