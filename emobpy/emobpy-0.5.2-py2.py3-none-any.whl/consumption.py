from zenodo_get import zenodo_get
from datetime import datetime
import pandas as pd
import numpy as np
import numba
import time
import logging
import wget
import yaml
import pytz
import sys
import os
import uuid
import gzip
import pickle

from .constants import (
    TIME_FREQ,
    CWD,
    DEFAULT_DATA_DIR,
    USER_PATH,
    DATA_DIR,
    MODULE_DATA_PATH,
    WEATHER_FILES,
    WEATHER_OPTIONS,
    EVSPECS_FILE,
    MG_EFFICIENCY_FILE,
    DC_FILE,
    UNITS,
    LAYER_NAMES,
    ZONE_NAMES,
    ZONE_LAYERS,
    ZONE_SURFACE,
    LAYER_CONDUCTIVITY,
    LAYER_THICKNESS,
    TARGET_TEMP,
    GRAVITY,
    VEHICLE_NEEDED_PARAMETERS,
)

from .functions import (
    rolling_resistance_coeff,
    vehicle_mass,
    Prollingresistance,
    Pairdrag,
    Pgravity,
    Pinertia,
    Pwheel,
    Pmotorout,
    EFFICIENCYregenerative_breaking,
    Pgeneratorin,
    Pmotorin,
    Pgeneratorout,
    Qhvac,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(message)s")
log_filename = "emobpy.log"

file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] kilobyte" % (
        current / total * 100,
        current / 1024,
        total / 1024,
    )
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def consumption_progress(current, total, width=80):
    progress_message = "Progress: %d%% [%d / %d] trips" % (
        current / total * 100,
        current,
        total,
    )
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


@numba.jit(nopython=True)
def inertial_mass(curb_weight, gear_ratio):
    return curb_weight * (0.04 + 0.0025 * gear_ratio ** 2)


def include_weather(pf, refdate, temp_arr, pres_arr, dp_arr, H, r_ha):
    year = pd.to_datetime(refdate).year
    start_date = pd.to_datetime(year, format="%Y")
    drange = pd.date_range(start_date, periods=len(r_ha) * 2, freq="H")
    df = pd.DataFrame(
        data={
            "temp_degC": np.concatenate([temp_arr, temp_arr]),
            "pressure_mbar": np.concatenate([pres_arr, pres_arr]),
            "dewpoint_degC": np.concatenate([dp_arr, dp_arr]),
            "humidity": np.concatenate([H, H]),
            "air_density_kg/m3": np.concatenate([r_ha, r_ha]),
        },
        index=drange,
    )
    df = df.rename_axis("datetime")
    df = df.sort_index().reset_index()
    df["weather_time"] = df["datetime"]
    return pd.merge_asof(
        pf, df, on="datetime", tolerance=pd.Timedelta("3600s"), direction="nearest"
    ).set_index("hr", drop=False)


class Weather:
    def __init__(self):
        pass

    def temp(self, country_code, year):
        return (
            self.load_data(country_code, year, option="temp Kelvin", location=None)
            - 273.15
        )

    def pressure(self, country_code, year):
        return (
            self.load_data(country_code, year, option="pressure Pascal", location=None)
            / 100
        )

    def dewpoint(self, country_code, year):
        return (
            self.load_data(country_code, year, option="dew_point Kelvin", location=None)
            - 273.15
        )

    @staticmethod
    def download_weather_data(location=None):
        user_dir = location or USER_PATH or DEFAULT_DATA_DIR
        os.makedirs(user_dir, exist_ok=True)
        os.chdir(user_dir)
        zenodo_get(["10.5281/zenodo.1489915", "-wurls.txt"])
        os.chdir(CWD)
        time.sleep(2)
        fh = open(os.path.join(user_dir, "urls.txt"))
        text_list = []
        for line in fh:
            text_list.append(line)
        fh.close()
        dest_list = []
        for url in text_list:
            for file in WEATHER_FILES.keys():
                if file in url:
                    filename = os.path.join(user_dir, WEATHER_FILES[file])
                    if os.path.exists(filename):
                        os.remove(filename)
                    print(f"Downloading file... {url.strip()}")
                    dest = wget.download(url.strip(), filename, bar=bar_progress)
                    print("")
                    dest_list.append(dest)
        for dfp in dest_list:
            print(dfp)
        return dest_list

    @staticmethod
    def load_data(country_code="DE", year=2016, option="temp Kelvin", location=None):
        """
        location: root dir of weather files
        option: 'dew_point Kelvin', 'pressure Pascal', 'temp Kelvin'
        """

        user_dir = location or USER_PATH or DEFAULT_DATA_DIR
        filename = os.path.join(user_dir, WEATHER_OPTIONS[option])
        if country_code == "UK":
            code = "GB"
        else:
            code = country_code

        dateparse = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S %Z")
        df = pd.read_csv(
            filename,
            parse_dates=["date"],
            date_parser=dateparse,
            usecols=["date", country_code],
        )
        timezones = pytz.country_timezones[code]
        logger.info(
            " ".join([option, country_code, str(year), "Timezone:", timezones[0]])
        )
        df.date = pd.DatetimeIndex(df.date).tz_localize("GMT").tz_convert(timezones[0])
        data = df[df.date.dt.year.isin([year])]
        return (
            data.set_index("date").reset_index(drop=True)[country_code][0:8760].values
        )

    @staticmethod
    def calcVaporPressureWF(t, h):
        T = t  # degC
        H = h  # pct
        E = (H / 100) * 6.112 * np.exp((17.67 * T) / (243.5 + T))
        return E

    @staticmethod
    def calcVaporPressure(t):
        """
        t: temp degC
        """
        T = t  # dew point or air temp degC
        E = 6.11 * np.power(
            10, ((7.5 * T) / (237.3 + T))
        )  # saturated  vapor pressure (mb) if t is dewpoint
        return E

    def calcRelHumidity(self, Dp, T):
        """
        Dp,T: temp degC
        """
        H = (
            100 * self.calcVaporPressure(Dp) / self.calcVaporPressure(T)
        )  # Relative humidity (percentage)
        return H

    @staticmethod
    def calcDewPoint(t, h):
        """
        t: temp degC
        h: %
        """
        T = t
        H = h
        Td = (
            243.04
            * (np.log(H / 100) + ((17.625 * T) / (243.04 + T)))
            / (17.625 - np.log(H / 100) - ((17.625 * T) / (243.04 + T)))
        )
        return Td

    @staticmethod
    def calcDryAirPartialPressure(P, pv):
        pair = P - pv
        return pair

    @staticmethod
    def airDensityFromIdealGasLaw(t, p):
        T = t + 273.15  # convert degC => degK
        P = 100 * p  # convert mb   => Pascals
        N = 287.05  # specific gas constant , J/(kg*degK) = 287.05 for dry air
        return P / (N * T)

    def humidairDensity(self, t, p, dp=None, h=None):
        """
        t,dp: temp degC
        h: %
        p: mbar
        """
        if dp is None and h is None:
            raise Exception("One value is required, either dp or h")
        if dp is not None:
            pv = self.calcVaporPressure(dp)  # mbar
        if h is not None:
            pv = self.calcVaporPressure(self.calcDewPoint(t, h))  # mbar

        pd = self.calcDryAirPartialPressure(p, pv)  # mbar

        Pv = 100 * pv  # convert mb   => Pascals
        Pd = 100 * pd  # convert mb   => Pascals

        Rd = 287.05  # specific gas constant for dry air [J/(kgK)]
        Rv = 461.495  # specific gas constant for water vapour [J/(kgK)]
        T = t + 273.15  # convert degC => degK

        AD = Pd / (Rd * T) + Pv / (Rv * T)  # density [kg/m3]
        return AD


class BEVspecs:
    def __init__(self, filename=None):
        self.filename = filename
        self.data = []
        self.parameters = [
            "Acceleration from 0 to 100 km/h s (seconds)",
            "Axle ratio",
            "Battery capacity kWh (kilowatt hours)",
            "Brand",
            "Curb weight kg (kilograms)",
            "Drag coefficient Cd (drag coefficient)",
            "Electric motor type",
            "Height m (meters)",
            "Length m (meters)",
            "Market",
            "EV Model",
            "Model year",
            "Number of cells",
            "Number of modules",
            "Power kW (kilowatts)",
            "Regenerative braking",
            "Top speed km/h (kilometers per hour)",
            "Torque Nm (newton meters)",
            "Trunk volume m3 (cubic meters)",
            "Type of rechargeable battery",
            "Voltage V (volts)",
            "Weight kg (kilograms)",
            "Width m (meters)",
        ]
        self.load_specs(filename=self.filename)

    def load_specs(self, filename=None):
        """
        filename: file .yml with ev data
        """

        if filename is None:
            user_dir = USER_PATH or DEFAULT_DATA_DIR
            self.filename = os.path.join(user_dir, EVSPECS_FILE)
        else:
            self.filename = filename
        with open(self.filename) as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

    def search(self, *args):
        dc = {}
        if not args:
            args = ["Power kW (kilowatts)"]
        for arg in args:
            if arg in self.parameters:
                for ev in self.data:
                    model = ev["EV Model"]
                    brand = ev["Brand"]
                    year = str(int(ev["Model year"]))
                    ids = tuple([brand, model, year])
                    if ids in dc:
                        pass
                    else:
                        dc[ids] = {}
                    if arg in dc[ids]:
                        pass
                    else:
                        dc[ids][arg] = {}
                    dc[ids][arg] = ev[arg]
            else:
                print(f"{arg} not in titles")
        return dc

    def get(self, brand, model, year, parameter):
        if parameter in self.parameters:
            flag = False
            for ev in self.data:
                modeldb = ev["EV Model"]
                branddb = ev["Brand"]
                yeardb = str(int(ev["Model year"]))
                if tuple([brand, model, str(int(year))]) == tuple(
                    [branddb, modeldb, yeardb]
                ):
                    value = ev[parameter]
                    flag = True
                    break
            if flag:
                return value
            else:
                print("No value found! verify there is no typo")
        else:
            print("No value found!")
        return None

    def dropna_model(self, parameter):
        index = []
        for i, ev in enumerate(self.data):
            if ev[parameter].__class__.__name__ in ["float"]:
                if np.isnan(ev[parameter]):
                    index.append(i)
        for j in index[::-1]:
            print(
                f"Delete {self.data[j]['Brand']} {self.data[j]['EV Model']} {int(self.data[j]['Model year'])}"
            )
            self.data.pop(j)

    def replacena_model(self, parameter, default):
        index = []
        for i, ev in enumerate(self.data):
            if ev[parameter].__class__.__name__ in ["float"]:
                if np.isnan(ev[parameter]):
                    index.append(i)
        for j in index[::-1]:
            print(
                f"Added {default} to {self.data[j]['Brand']} {self.data[j]['EV Model']} {int(self.data[j]['Model year'])}"
            )
            self.data[j][parameter] = default

    def maximum(self, parameter):
        value = []
        for i, ev in enumerate(self.data):
            if ev[parameter].__class__.__name__ in ["float", "int"]:
                if not np.isnan(ev[parameter]):
                    value.append(ev[parameter])
        return max(value)

    def average(self, parameter):
        value = []
        for i, ev in enumerate(self.data):
            if ev[parameter].__class__.__name__ in ["float", "int"]:
                if not np.isnan(ev[parameter]):
                    value.append(ev[parameter])
        return round(sum(value) / len(value), 3)

    def model(self, model, msg=True):
        M = ModelSpecs(model, self)
        M.add_parameters()
        M.add_calculated_param()
        self.ev_par_test(M, msg=msg)
        return M

    def ev_par_test(self, Model, msg=True):
        param_names = VEHICLE_NEEDED_PARAMETERS
        param_missing = []
        for wanted in param_names:
            flag = False
            for parameter in Model.parameters:
                if wanted == parameter:
                    if not isinstance(Model.parameters[parameter], (int, float)):
                        flag = False
                        break
                    flag = True
                    break
            if not flag:
                param_missing.append(wanted)
        if len(param_missing) == 0:
            pass
        else:
            if msg:
                print("Missing relevant parameters:")
                for name in param_missing:
                    print("   ", name)
                print(
                    'Please, add these parameters to the model instance < model_instance.add({"parameter":value}) >'
                )

    def save(self):
        """
        filename: file .yml with ev data
        """
        with open(self.filename, "w") as file:
            yaml.dump(self.data, file)
        print(f"File saved: {self.filename}")
        logger.info(f"File saved: {self.filename}")


class ModelSpecs:
    def __init__(self, model, BEVspecs_instance):
        self.name = model
        self.parameters = {}
        self.db = BEVspecs_instance
        for parameter in self.db.parameters:
            if parameter == "Brand":
                self.parameters[parameter] = model[0]
            elif parameter == "EV Model":
                self.parameters[parameter] = model[1]
            elif parameter == "Model year":
                self.parameters[parameter] = model[2]
            else:
                self.parameters[parameter] = None

    def add_parameters(self):
        for parameter in self.db.parameters:
            value = self.db.get(*self.name, parameter)
            self.parameters[parameter] = value

    def add_calculated_param(self):
        if (
            "Power kW (kilowatts)" in self.parameters
            and "Curb weight kg (kilograms)" in self.parameters
        ):
            self.parameters["PMR W/kg"] = self.PMR(
                self.parameters["Power kW (kilowatts)"],
                self.parameters["Curb weight kg (kilograms)"],
            )
        else:
            self.parameters["PMR W/kg"] = None
        if (
            "Curb weight kg (kilograms)" in self.parameters
            and "Axle ratio" in self.parameters
        ):
            self.parameters["Inertial mass kg"] = inertial_mass(
                self.parameters["Curb weight kg (kilograms)"],
                self.parameters["Axle ratio"],
            )
        else:
            self.parameters["Inertial mass kg"] = None
        if (
            "Width m (meters)" in self.parameters
            and "Height m (meters)" in self.parameters
        ):
            self.parameters["Frontal area m2"] = self.frontal_area(
                self.parameters["Height m (meters)"],
                self.parameters["Width m (meters)"],
            )
        else:
            self.parameters["Frontal area m2"] = None

    def PMR(self, power, curb_weight):
        return power * 1000 / curb_weight  #  W/kg

    def frontal_area(self, height, width):
        return height * width

    def addtodb(self):
        nones = []
        flag = False
        for param in self.parameters:
            if self.parameters[param] is None:
                flag = True
                nones.append(param)
        if flag:
            print(
                "The model can not be added to the database. It has parameters with None as value"
            )
            return nones
        self.add_calculated_param()
        self.db.data.append(self.parameters)
        print("Model added to the BEVspecs instance")
        return None

    def add(self, parameters_dict, msg=True):
        for k, v in parameters_dict.items():
            self.parameters[k] = v
            if k in VEHICLE_NEEDED_PARAMETERS:
                if msg:
                    print(f"{k} has been added to the model object. Required OK")


class MGefficiency:
    def __init__(self, filename=None):
        self.data = None
        self.filename = filename
        self.load_file(filename=self.filename)
        self.get_codes()

    def load_file(self, filename=None):
        """
        filename: file .csv with bev efficiency
        """
        if filename is None:
            user_dir = USER_PATH or DEFAULT_DATA_DIR
            self.filename = os.path.join(user_dir, MG_EFFICIENCY_FILE)
        else:
            self.filename = filename
        with open(self.filename) as file:
            self.data = pd.read_csv(file)

    def get_codes(self):
        self.load_fraction = self.data.load_fraction.values
        self.motor = self.data.motor.values
        self.generator = self.data.generator.values

    def get_efficiency(self, load_fraction, g_m_code):
        """
        g_m_code: 1 -> motor, -1 -> generator
        """
        if not g_m_code in [1, -1]:
            raise Exception(f"g_m_code is {g_m_code}. It should be 1 or -1")
        if g_m_code == 1:
            return self._get_efficiency(load_fraction, self.load_fraction, self.motor)
        elif g_m_code == -1:
            return self._get_efficiency(
                np.abs(load_fraction), self.load_fraction, self.generator
            )

    @staticmethod
    @numba.jit(nopython=True)
    def _get_efficiency(load_fraction, load_fraction_values, column_values):
        return np.interp(load_fraction, load_fraction_values, column_values)


@numba.jit(nopython=True)
def acceleration(V0, V2):  # V0, V2 km/h
    acc = (V2 - V0) / 2 / 3.6  # acc m/s**2
    return acc


@numba.jit(nopython=True)
def acceleration_array(speed_array):
    acc = np.zeros((speed_array.shape[0],))
    acc[0] = acceleration(0, speed_array[1])
    i = 0
    for a, b in zip(speed_array[0:-2], speed_array[2:]):
        i += 1
        acc[i] = acceleration(a, b)
    return acc


class DrivingCycle:
    def __init__(self):
        self.data = []
        self.index_speed = None
        user_dir = USER_PATH or DEFAULT_DATA_DIR
        self.datafile = os.path.join(user_dir, DC_FILE)
        # self.load_data()

    def get_csv(self, csv_path=os.path.join(MODULE_DATA_PATH, "driving_cycles.csv")):
        self.csv_path = csv_path
        self.dc_df = pd.read_csv(self.csv_path, index_col="Seconds")

    def create_data(self):
        self.data = []
        for i, dc_name in enumerate(self.dc_df.columns):
            dc = {}
            dc["name"] = dc_name
            dc["type"] = dc_name.split("_")[0]
            dc["id"] = i
            dc["speed"] = {}
            dc["speed"]["value"] = self.dc_df[dc_name].dropna().values
            dc["speed"]["unit"] = "km/h"
            dc["mean_speed"] = {}
            dc["mean_speed"]["value"] = round(float(np.mean(dc["speed"]["value"])), 1)
            dc["mean_speed"]["unit"] = "km/h"
            dc["time"] = {}
            dc["time"]["value"] = len(dc["speed"]["value"])
            dc["time"]["unit"] = "s"
            dc["distance"] = {}
            dc["distance"]["value"] = round(float(sum(dc["speed"]["value"] / 3600)), 1)
            dc["distance"]["unit"] = "km"
            dc["normalized"] = {}
            dc["normalized"]["value"] = np.round(
                dc["speed"]["value"] / dc["mean_speed"]["value"], 4
            )
            dc["normalized"]["unit"] = ""
            dc["acceleration"] = {}
            dc["acceleration"]["value"] = np.round(
                acceleration_array(dc["speed"]["value"]), 4
            )
            dc["acceleration"]["unit"] = "m/s**2"
            dc["max_acceleration"] = {}
            dc["max_acceleration"]["value"] = float(max(dc["acceleration"]["value"]))
            dc["max_acceleration"]["unit"] = "m/s**2"
            self.data.append(dc)
        self.get_index_speed()

    def save_data(self):
        self.tmpdata = []
        i = -1
        for dc in self.data:
            i += 1
            self.tmpdata.append(dc)
            for key in dc.keys():
                if isinstance(self.tmpdata[i][key], dict):
                    if isinstance(self.tmpdata[i][key]["value"], np.ndarray):
                        self.tmpdata[i][key]["value"] = self.tmpdata[i][key][
                            "value"
                        ].tolist()

        with open(self.datafile, "w") as file:
            yaml.dump(self.tmpdata, file)
        print(f"File saved: {self.datafile}")

    def load_data(self):
        if os.path.isfile(self.datafile):
            with open(self.datafile) as file:
                self.tmpdata = yaml.load(file, Loader=yaml.FullLoader)
            i = -1
            for dc in self.tmpdata:
                i += 1
                self.data.append(dc)
                for key in dc.keys():
                    if isinstance(self.data[i][key], dict):
                        if isinstance(self.data[i][key]["value"], list):
                            self.data[i][key]["value"] = np.array(
                                self.data[i][key]["value"]
                            )
            self.get_index_speed()
        else:
            print(
                f'File "{self.datafile}" does not exist!. You can create it from .csv file'
            )

    def get_index_speed(self):
        self.index_speed = {}
        classes = ["WLTC_3b", "WLTC_2"]
        dc_types = list(set([t["type"] for t in self.data]))

        dc_class = []
        dc_full = []
        for t in self.data:
            flag = False
            for entry in classes:
                if entry in t["name"]:
                    flag = True
                    dc_class.append(entry)
                    if "full" in t["name"]:
                        dc_full.append(True)
                    else:
                        dc_full.append(False)
                    break
            if not flag:
                dc_class.append("none")
                if "full" in t["name"]:
                    dc_full.append(True)
                else:
                    dc_full.append(False)

        for type_ in dc_types:
            self.index_speed[type_] = {}
            if "WLTC" == type_:
                for cl in classes:
                    self.index_speed[type_][cl] = {"partial": {}, "full": {}}
            else:
                self.index_speed[type_]["none"] = {"partial": {}, "full": {}}

        for s in self.data:
            if dc_full[s["id"]]:
                key = "full"
            else:
                key = "partial"
            self.index_speed[s["type"]][dc_class[s["id"]]][key][s["id"]] = {
                "value": s["mean_speed"]["value"],
                "unit": s["mean_speed"]["unit"],
            }

    def select_driving_cycle_index(
        self, driving_cycle_type, speed, PMR, full_driving_cycle
    ):

        WLTC_class = "none"
        if driving_cycle_type == "WLTC":
            if PMR is not None:
                if PMR > 34:
                    WLTC_class = "WLTC_3b"
                elif PMR > 22 and PMR <= 34:
                    WLTC_class = "WLTC_2"

        idx = []
        spd = []
        if not full_driving_cycle:
            for k, v in self.index_speed[driving_cycle_type][WLTC_class][
                "partial"
            ].items():
                idx.append(k)
                driving_cycle_type_average_speed = v["value"] * UNITS[v["unit"]]["m/s"]
                trip_average_speed = speed["value"] * UNITS[speed["unit"]]["m/s"]
                spd.append(-abs(driving_cycle_type_average_speed - trip_average_speed))
            return idx[np.argmax(spd)]
        else:
            return list(
                self.index_speed[driving_cycle_type][WLTC_class]["full"].keys()
            )[0]

    def driving_cycle(self, trip, model, full_driving_cycle=False):

        trip.index = self.select_driving_cycle_index(
            trip.driving_cycle_type,
            trip._mean_speed,
            model.parameters["PMR W/kg"],
            full_driving_cycle,
        )

        if full_driving_cycle:
            trip.duration["value"] = (
                self.data[trip.index]["time"]["value"]
                * UNITS[self.data[trip.index]["time"]["unit"]]["s"]
            )
            trip.duration["unit"] = "s"
            trip.distance["value"] = (
                self.data[trip.index]["distance"]["value"]
                * UNITS[self.data[trip.index]["distance"]["unit"]]["m"]
            )
            trip.distance["unit"] = "m"
            trip.get_mean_speed()

        trip.time["value"] = np.ceil(
            trip._duration["value"] * UNITS[trip._duration["unit"]]["s"]
        )
        trip.time["unit"] = "s"
        scale = (
            trip.time["value"]
            // self.data[trip.index]["time"]["value"]
            * UNITS[self.data[trip.index]["time"]["unit"]]["s"]
        )
        slide = (
            trip.time["value"]
            % self.data[trip.index]["time"]["value"]
            * UNITS[self.data[trip.index]["time"]["unit"]]["s"]
        )
        normalized = self.data[trip.index]["normalized"]["value"]
        normalized_array = np.array(
            list(normalized) * int(scale) + list(normalized)[0 : int(slide)]
        )
        speed_array = (
            normalized_array
            * trip._mean_speed["value"]
            * UNITS[trip._mean_speed["unit"]]["m/s"]
        )
        i = 0
        for last_secs in range(-20, 0):
            i += 1
            calc = (
                speed_array[last_secs - 1] - speed_array[last_secs - 1] * (i / 100) * 2
            )
            speed_array[last_secs] = max(0, calc)

        trip.speed["value"] = speed_array
        trip.speed["unit"] = "m/s"
        trip.acceleration["value"] = acceleration_array(speed_array)
        trip.acceleration["unit"] = "m/s**2"

        trip.driving_cycle_name = self.data[trip.index]["name"]


class Trips:
    def __init__(self):
        self.quantity = 0
        self.trips = []

    def get_code(self):
        code = self.quantity
        self.quantity += 1
        return code

    def add_trip(self, trip):
        self.trips.append(trip)

    def get_trip(self, code):
        return self.trips[code]


class Trip:
    def __init__(self, trips):
        self.code = trips.get_code()
        self.origin = None
        self.destination = None
        self.distance = {"value": None, "unit": None}
        self._distance = {"value": None, "unit": None}
        self.duration = {"value": None, "unit": None}
        self._duration = {"value": None, "unit": None}
        self.start_trip_time = {"value": None, "unit": None}
        self.end_trip_time = {"value": None, "unit": None}
        self.mean_speed = {"value": None, "unit": None}
        self._mean_speed = {"value": None, "unit": None}
        self.driving_cycle_type = None
        self.driving_cycle_name = None
        self.acceleration = {"value": None, "unit": None}
        self.speed = {"value": None, "unit": None}
        self.time = {"value": None, "unit": None}
        self.index = None
        self.balance = None
        self.results = {}
        self.rate = {"value": None, "unit": None}
        self.consumption = {"value": None, "unit": None}
        trips.add_trip(self)

    def add_distance_duration(self, distance, duration):
        self.distance["value"] = distance["value"]
        self.distance["unit"] = distance["unit"]
        self.duration["value"] = duration["value"]
        self.duration["unit"] = duration["unit"]
        self.get_mean_speed()

    def get_mean_speed(self):

        self._distance["value"] = (
            self.distance["value"] * UNITS[self.distance["unit"]]["m"]
        )
        self._distance["unit"] = "m"
        self._duration["value"] = (
            self.duration["value"] * UNITS[self.duration["unit"]]["s"]
        )
        self._duration["unit"] = "s"

        self.mean_speed = {
            "value": self.distance["value"] / self.duration["value"],
            "unit": self.distance["unit"] + "/" + self.duration["unit"],
        }
        self._mean_speed = {
            "value": self._distance["value"] / self._duration["value"],
            "unit": self._distance["unit"] + "/" + self._duration["unit"],
        }


class HeatInsulation:
    def __init__(self, default=False):
        self.flag = True
        self.zone_layers = {}
        self.zone_surface = {}
        self.layer_conductivity = {}
        self.layer_thickness = {}
        self.layer_names = None
        self.zone_names = None
        if default:
            self.layers_name(LAYER_NAMES)
            self.zones_name(ZONE_NAMES)
            self.zone_layers = ZONE_LAYERS
            self.zone_surface = ZONE_SURFACE
            self.layer_conductivity = LAYER_CONDUCTIVITY
            self.layer_thickness = LAYER_THICKNESS
            self.flag = False
            self.makearrays()

    def layers_name(self, name_list):
        self.layer_names = name_list
        for nm in name_list:
            self.layer_conductivity[nm] = None
            self.layer_thickness[nm] = None

    def zones_name(self, name_list):
        self.zone_names = name_list
        for nm in name_list:
            self.zone_layers[nm] = None
            self.zone_surface[nm] = None

    def compile(self):
        for zone in self.zone_names:
            layer = {}
            for lyr in self.layer_names:
                layer[lyr] = None
            self.zone_layers[zone] = layer
        self.check()

    def show(self):
        print("zone_layers:")
        print(self.zone_layers)
        print("zone_surface:")
        print(self.zone_surface)
        print("layer_conductivity:")
        print(self.layer_conductivity)
        print("layer_thickness:")
        print(self.layer_thickness)
        self.check()

    def check(self):
        flag = False
        for zone in self.zone_names:
            for lyr in self.layer_names:
                if self.zone_layers[zone][lyr] is None:
                    print(
                        f"{self.__class__.__name__}.zone_layers['{zone}']['{lyr}'] = None"
                    )
                    flag = True

        for zone in self.zone_names:
            if self.zone_surface[zone] is None:
                print(f"{self.__class__.__name__}.zone_surface['{zone}'] = None")
                flag = True

        for lyr in self.layer_names:
            if self.layer_conductivity[lyr] is None:
                print(f"{self.__class__.__name__}.layer_conductivity['{lyr}'] = None")
                flag = True

        for lyr in self.layer_names:
            if self.layer_thickness[lyr] is None:
                print(f"{self.__class__.__name__}.layer_thickness['{lyr}'] = None")
                flag = True
        if flag:
            self.flag = True
            print('There are still "None" fields. All fields must contain values.')
        else:
            self.flag = False

    def makearrays(self):
        if not self.flag:
            z_l = []
            for zone in self.zone_layers.keys():
                z_l.append(list(self.zone_layers[zone].values()))
            self.zone_layers_ = np.array(z_l)
            self.zone_surface_ = np.array(list(self.zone_surface.values()))
            self.layer_conductivity_ = np.array(list(self.layer_conductivity.values()))
            self.layer_thickness_ = np.array(list(self.layer_thickness.values()))


class Consumption:
    def __init__(self, input, ev_model):
        self.profile = None
        self.kind = "consumption"
        self.input = input
        self.vehicle = ev_model
        self.ev_par_test()
        self.brand = "_".join(self.vehicle.parameters["Brand"].split(" "))
        self.model = "_".join(self.vehicle.parameters["EV Model"].split(" "))
        self.year = str(int(self.vehicle.parameters["Model year"]))
        self.name = (
            self.input
            + "_"
            + self.brand
            + "_"
            + self.model
            + "_"
            + self.year
            + "_"
            + uuid.uuid4().hex[0:5]
        )
        self.COP = {
            "heating": self.vehicle.parameters["HVAC_COP_heating"],
            "cooling": self.vehicle.parameters["HVAC_COP_cooling"],
        }
        self.TARGET_TEMP = TARGET_TEMP

    def ev_par_test(self):
        param_names = VEHICLE_NEEDED_PARAMETERS
        param_missing = []
        for wanted in param_names:
            flag = False
            for parameter in self.vehicle.parameters:
                if wanted == parameter:
                    if not isinstance(self.vehicle.parameters[parameter], (int, float)):
                        flag = False
                        break
                    flag = True
                    break
            if not flag:
                param_missing.append(wanted)
        if len(param_missing) == 0:
            pass
        else:
            print("Missing parameters in vehicle object:")
            for name in param_missing:
                print(name)
            raise Exception(
                'Parameters missing, add these parameters to the ev_model object < ev_model.add({"parameter_name":value}) >'
            )

    def cop_and_target_temp(self, T_out):
        if T_out < self.TARGET_TEMP["heating"]:
            T_targ = self.TARGET_TEMP["heating"]
            cop = self.COP["heating"]
            flag = 1
        elif T_out > self.TARGET_TEMP["cooling"]:
            T_targ = self.TARGET_TEMP["cooling"]
            cop = self.COP["cooling"]
            flag = -1
        else:
            T_targ = None
            cop = 1
            flag = 0
        return T_targ, cop, flag

    def loadSettingMobility(self, DataBase):
        """
        DataBase: object DataBase(). see example,
        eg. manager = DataBase(dir)
            "manager" is a class instance that contains the profiles

        Then, the following attributes can be called
            self.df
            self.t
            self.totalrows
            self.hours
            self.freq
            self.refdate
            self.energy_consumption
            self.states
        """
        if DataBase.db[self.input]:
            if DataBase.db[self.input]["kind"] == "driving":
                self.profile = DataBase.db[self.input]["profile"].copy()
                self.t = DataBase.db[self.input]["t"]
                self.totalrows = DataBase.db[self.input]["totalrows"]
                self.hours = DataBase.db[self.input]["hours"]
                self.freq = TIME_FREQ[self.t]["f"]
                self.refdate = DataBase.db[self.input]["refdate"]
                self.states = DataBase.db[self.input]["states"]
            else:
                raise ValueError(
                    "The driving profile {} can not be found in the database".format(
                        self.input
                    )
                )
        else:
            raise ValueError(
                "The driving profile {} can not be found in the database".format(
                    self.input
                )
            )

    def run(
        self,
        heat_insulation,  # object
        weather_country="DE",
        weather_year=2016,
        passenger_mass=75,  # kg
        passenger_sensible_heat=70,  # W
        passenger_nr=1.5,
        air_cabin_heat_transfer_coef=10,  # W/(m2K)
        air_flow=0.01,  # m3/s   0.02 high ventilation - 0.001 minimum vent
        driving_cycle_type="WLTC",
        road_type=0,  # see function rolling_resistance_coeff(method='M1') if an integer then all trips have the same value, if list must fit the lenght of the profile
        wind_speed=0,  # m/s if an integer then all trips have the same value, if list must fit the lenght of the profile
        road_slope=0,  # radians if an integer then all trips have the same value, if list must fit the lenght of the profile
    ):

        self.heat_insulation = heat_insulation
        self.weather_country = weather_country
        self.weather_year = weather_year
        self.passenger_mass = passenger_mass
        self.passenger_sensible_heat = passenger_sensible_heat
        self.passenger_nr = passenger_nr
        self.air_flow = air_flow
        self.driving_cycle_type = driving_cycle_type
        self.road_type = road_type
        self.wind_speed = wind_speed
        self.road_slope = road_slope
        self.transmission_eff = self.vehicle.parameters["Transmission_efficiency"]
        self.battery_discharge_eff = self.vehicle.parameters[
            "Battery_discharging_efficiency"
        ]
        self.battery_charge_eff = self.vehicle.parameters["Battery_charging_efficiency"]
        self.air_cabin_heat_transfer_coef = air_cabin_heat_transfer_coef
        self.auxiliary_power = self.vehicle.parameters["Auxiliary_power_W"]
        self.cabin_volume = self.vehicle.parameters["Cabin_volume_m3"]

        if heat_insulation.flag:
            raise Exception(
                "heat_insulation object is not complete. Test the object with the method check() before including it as argument"
            )

        print("New profile running: " + self.name)
        logger.info("###################################################")
        logger.info("===================================================")
        logger.info("New profile running: " + self.name)
        logger.info("===================================================")
        logger.info("###################################################")

        self.profile = self.profile[["hr", "state", "distance", "trip_duration"]].copy()
        self.profile.loc[:, "datetime"] = pd.to_datetime(self.refdate) + (
            self.profile.hr * 60
        ).astype("timedelta64[m]")
        self.profile = self.profile.set_index("datetime")
        self.profile = self.profile.sort_index().reset_index()
        self.profile.loc[:, "speed km/h"] = (
            self.profile["distance"] / self.profile["trip_duration"] * 60
        )
        self.profile.loc[:, "wind_m/s"] = wind_speed
        self.profile.loc[:, "slope_rad"] = road_slope
        self.profile.loc[:, "road_type"] = road_type

        wt = Weather()
        D = wt.humidairDensity
        temp_arr = wt.temp(weather_country, weather_year)
        pres_arr = wt.pressure(weather_country, weather_year)
        dp_arr = wt.dewpoint(weather_country, weather_year)
        hum_arr = wt.calcRelHumidity(dp_arr, temp_arr)
        r_ha = wt.humidairDensity(temp_arr, pres_arr, h=hum_arr)

        self.profile = include_weather(
            self.profile, self.refdate, temp_arr, pres_arr, dp_arr, hum_arr, r_ha
        )
        self.η = MGefficiency()
        self.Trips = Trips()
        dc = DrivingCycle()
        dc.load_data()
        total = len(self.profile[self.profile["state"] == "driving"])
        current = 1

        for i, row in self.profile.iterrows():
            if row["state"] == "driving":
                consumption_progress(current, total)
                current += 1
                trip = Trip(self.Trips)
                trip.driving_cycle_type = driving_cycle_type
                trip.add_distance_duration(
                    distance={"value": row["distance"], "unit": "km"},
                    duration={"value": row["trip_duration"], "unit": "min"},
                )
                dc.driving_cycle(trip, self.vehicle, full_driving_cycle=False)
                v = trip.speed["value"]  # m/s
                acc = trip.acceleration["value"]  # m/s2
                targ_temp, cop, ret = self.cop_and_target_temp(row["temp_degC"])
                frontal_area = self.vehicle.parameters["Frontal area m2"]
                P_max = (
                    self.vehicle.parameters["Power kW (kilowatts)"] * 1000
                )  # kW to W
                f_d = self.vehicle.parameters["Drag coefficient Cd (drag coefficient)"]
                f_r = rolling_resistance_coeff(
                    method="M1",
                    temp=row["temp_degC"],
                    v=v * 3.6,
                    road_type=row["road_type"],
                )
                # f_r = rolling_resistance_coeff(method='M2', v=v*3.6, tire_type=0, road_type=4)
                m_i = self.vehicle.parameters["Inertial mass kg"]
                m_c = self.vehicle.parameters["Curb weight kg (kilograms)"]
                m_v = vehicle_mass(m_c, passenger_mass * passenger_nr)
                P_rol = Prollingresistance(f_r, m_v, GRAVITY, v)
                P_air = Pairdrag(
                    row["air_density_kg/m3"], frontal_area, f_d, v, row["wind_m/s"]
                )  # last arg is wind speed
                P_g = Pgravity(
                    m_v, GRAVITY, v, row["slope_rad"]
                )  # last arg is road slope
                P_ine = Pinertia(m_i, m_v, acc, v)
                P_wheel = Pwheel(P_rol, P_air, P_g, P_ine)
                P_m_o = Pmotorout(P_wheel, self.transmission_eff)
                n_rb = EFFICIENCYregenerative_breaking(acc)
                P_gen_in = Pgeneratorin(P_wheel, self.transmission_eff, n_rb)
                Load_p_m = P_m_o / P_max
                Load_p_g = P_gen_in / P_max
                n_mot = self.η.get_efficiency(Load_p_m, 1)
                n_gen = self.η.get_efficiency(Load_p_g, -1)
                P_m_in = Pmotorin(P_m_o, n_mot)
                P_g_out = Pgeneratorout(P_gen_in, n_gen)
                P_aux = np.array([self.auxiliary_power] * len(v))
                Q_hvac, Tcabin = Qhvac(
                    D,
                    row["temp_degC"],
                    targ_temp,
                    self.cabin_volume,
                    air_flow,
                    heat_insulation.zone_layers_,
                    heat_insulation.zone_surface_,
                    heat_insulation.layer_conductivity_,
                    heat_insulation.layer_thickness_,
                    v,
                    Q_sensible=passenger_sensible_heat,
                    Persons=passenger_nr,
                    air_cabin_heat_transfer_coef=air_cabin_heat_transfer_coef,
                )
                P_hvac = np.abs(Q_hvac[:, 0]) / cop
                P_gen_bat_charg = P_g_out * self.battery_charge_eff * -1
                P_bat = (P_m_in + P_aux + P_hvac) / self.battery_discharge_eff
                # section to calculate consumption
                P_all = P_m_in + P_aux + P_hvac + P_g_out
                P_all_negative = P_all.copy()
                P_all_negative[P_all_negative > 0.0] = 0.0
                P_all_positive = P_all.copy()
                P_all_positive[P_all_positive < 0.0] = 0.0
                P_bat_chg = P_all_negative * self.battery_charge_eff
                P_bat_dischg = P_all_positive / self.battery_discharge_eff
                P_bat_actual = np.add(P_bat_dischg, P_bat_chg)  # W
                consumption = P_bat_actual.sum() / 1000 / 3600  # kWh
                rate = consumption / v.sum() * 100000  # kWh/100 km

                # Add variables to trip object: International units (power in W)
                trip.results["targ_temp"] = targ_temp
                trip.results["cop"] = cop
                trip.results["ret"] = ret
                trip.results["frontal_area"] = frontal_area
                trip.results["P_max"] = P_max
                trip.results["Drag_coeff"] = f_d
                trip.results["roll_res_coeff"] = f_r
                trip.results["m_i"] = m_i
                trip.results["m_c"] = m_c
                trip.results["m_v"] = m_v
                trip.results["P_rol"] = P_rol
                trip.results["P_air"] = P_air
                trip.results["P_g"] = P_g
                trip.results["P_ine"] = P_ine
                trip.results["P_wheel"] = P_wheel
                trip.results["P_gen_in"] = P_gen_in
                trip.results["Load_p_m"] = Load_p_m
                trip.results["Load_p_g"] = Load_p_g
                trip.results["n_mot"] = n_mot
                trip.results["n_gen"] = n_gen
                trip.results["P_m_in"] = P_m_in
                trip.results["P_g_out"] = P_g_out
                trip.results["P_aux"] = P_aux
                trip.results["Q_hvac"] = Q_hvac
                trip.results["Tcabin"] = Tcabin
                trip.results["Tout"] = row["temp_degC"]
                trip.results["P_hvac"] = P_hvac

                trip.results["P_gen_bat_charg"] = P_gen_bat_charg
                trip.results["P_bat"] = P_bat  # only all positive loads
                trip.results[
                    "P_bat_actual"
                ] = P_bat_actual  # positive load after generation substraction and negarive load (generation) after positive loads substraction

                # Variable for the balance

                P_wheel_pos = P_wheel[P_wheel > 0].sum()  # Ws
                P_wheel_neg = P_wheel[P_wheel < 0].sum() * -1  # Ws
                P_m_o_t = P_m_o.sum()  # Ws
                P_gen_in_t = P_gen_in.sum() * -1  # Ws
                P_m_in_t = P_m_in.sum()  # Ws
                P_g_out_t = P_g_out.sum() * -1  # Ws
                P_aux_t = P_aux.sum()  # Ws
                P_hvac_t = P_hvac.sum()  # Ws
                Heat_source = np.abs(Q_hvac[:, 0]).sum() - P_hvac_t  # Ws
                P_gen_bat_charg_t = P_gen_bat_charg.sum()  # Ws
                P_gen_bat_dischg_t = (
                    P_gen_bat_charg_t * self.battery_discharge_eff
                )  # Ws
                P_bat_t = P_bat.sum()  # Ws

                trip.consumption[
                    "value"
                ] = consumption  # the only option this value be to small or negative is the ev goes downhill most of the trip
                trip.consumption["unit"] = "kWh"
                trip.rate["value"] = rate
                trip.rate["unit"] = "kWh/100 km"

                Loss_gen = P_gen_in_t - P_g_out_t
                Loss_trans_m = P_m_o_t - P_wheel_pos
                Loss_trans_g = P_wheel_neg - P_gen_in_t
                Loss_motor = P_m_in_t - P_m_o_t
                Loss_gen_bat_charg = P_gen_bat_charg_t * (1 - self.battery_charge_eff)
                Loss_gen_bat_dischg = P_gen_bat_charg_t * (
                    1 - self.battery_discharge_eff
                )
                Loss_bat = P_bat_t * (1 - self.battery_discharge_eff)

                if ret == 1:
                    cooling = 0
                    heating = P_hvac_t + Heat_source
                elif ret == -1:
                    cooling = P_hvac_t + Heat_source
                    heating = 0
                elif ret == 0:
                    cooling = 0
                    heating = 0

                # data for sankey diagram
                j = np.zeros((v.shape[0], 7))
                j[:, 0] = P_rol
                j[:, 1] = P_air
                j[:, 2] = P_g
                j[:, 3] = P_ine
                j[:, 4] = np.sum(j[:, 0:4], axis=1)
                j[:, 5] = j[:, 4]
                j[np.where(j[:, 5] > 0.0), 5] = 0
                j[:, 6] = j[:, 4]
                j[np.where(j[:, 6] < 0.0), 6] = 0

                ig = np.zeros((v.shape[0], 4))
                ig[np.where(j[:, 5] < 0.0), 0:4] = j[np.where(j[:, 5] < 0.0), 0:4]
                ig[np.where(ig[:, 0] > 0.0), 0] = 0
                ig[np.where(ig[:, 1] > 0.0), 1] = 0
                ig[np.where(ig[:, 2] > 0.0), 2] = 0
                ig[np.where(ig[:, 3] > 0.0), 3] = 0
                xg = np.true_divide(
                    ig,
                    ig.sum(axis=1, keepdims=True),
                    out=np.zeros_like(ig),
                    where=ig.sum(axis=1, keepdims=True) != 0,
                )
                yg = (xg.T * j[:, 5]).T * -1
                zg = yg.sum(axis=0)

                ip = np.zeros((v.shape[0], 4))
                ip[np.where(j[:, 6] > 0.0), 0:4] = j[np.where(j[:, 6] > 0.0), 0:4]
                ip[np.where(ip[:, 0] < 0.0), 0] = 0
                ip[np.where(ip[:, 1] < 0.0), 1] = 0
                ip[np.where(ip[:, 2] < 0.0), 2] = 0
                ip[np.where(ip[:, 3] < 0.0), 3] = 0
                xp = np.true_divide(
                    ip,
                    ip.sum(axis=1, keepdims=True),
                    out=np.zeros_like(ip),
                    where=ip.sum(axis=1, keepdims=True) != 0,
                )
                yp = (xp.T * j[:, 6]).T
                zp = yp.sum(axis=0)
                gra_neg = zg[2]
                acc_neg = zg[3]

                rol_pos = zp[0]
                air_pos = zp[1]
                gra_pos = zp[2]
                acc_pos = zp[3]

                self.profile.loc[i, "consumption kWh/100 km"] = rate
                self.profile.loc[i, "consumption kWh"] = consumption
                self.profile.loc[i, "battery discharge kWh"] = P_bat_t / 3600 / 1000
                self.profile.loc[i, "regeneration kWh"] = (
                    P_gen_bat_dischg_t / 3600 / 1000
                )
                self.profile.loc[i, "auxiliary kWh"] = P_aux_t / 3600 / 1000
                self.profile.loc[i, "hvac kWh"] = P_hvac_t / 3600 / 1000
                self.profile.loc[i, "motor in kWh"] = P_m_in_t / 3600 / 1000
                self.profile.loc[i, "transmission in kWh"] = P_m_o_t / 3600 / 1000
                self.profile.loc[i, "wheel kWh"] = P_wheel_pos / 3600 / 1000
                self.profile.loc[i, "rolling res kWh"] = rol_pos / 3600 / 1000
                self.profile.loc[i, "air res kWh"] = air_pos / 3600 / 1000
                self.profile.loc[i, "gravity kWh"] = gra_pos / 3600 / 1000
                self.profile.loc[i, "acceleration kWh"] = acc_pos / 3600 / 1000
                self.profile.loc[i, "trip code"] = trip.code

                stv = [
                    ["Heat source", "HVAC", Heat_source / 3600 / 1000],
                    ["Potential energy", "Gravity force", gra_neg / 3600 / 1000],
                    [
                        "Battery",
                        "Discharge",
                        (P_bat_t - P_gen_bat_charg_t) / 3600 / 1000,
                    ],
                    [
                        "Discharge",
                        "Losses",
                        (Loss_bat + Loss_gen_bat_dischg) / 3600 / 1000,
                    ],
                    ["Discharge", "HVAC", P_hvac_t / 3600 / 1000],
                    ["Discharge", "Auxiliary", P_aux_t / 3600 / 1000],
                    ["Discharge", "Motor", P_m_in_t / 3600 / 1000],
                    [
                        "Regenerative breaking",
                        "Discharge",
                        P_gen_bat_dischg_t / 3600 / 1000,
                    ],
                    [
                        "Regenerative breaking",
                        "Losses",
                        Loss_gen_bat_charg / 3600 / 1000,
                    ],
                    ["HVAC", "Cooling", cooling / 3600 / 1000],
                    ["HVAC", "Heating", heating / 3600 / 1000],
                    ["Motor", "Transmission of traction", P_m_o_t / 3600 / 1000],
                    ["Motor", "Losses", Loss_motor / 3600 / 1000],
                    ["Transmission of traction", "Wheel", P_wheel_pos / 3600 / 1000],
                    ["Transmission of traction", "Losses", Loss_trans_m / 3600 / 1000],
                    ["Wheel", "Rolling resistance", rol_pos / 3600 / 1000],
                    ["Wheel", "Air resistance", air_pos / 3600 / 1000],
                    ["Wheel", "Gravity force", gra_pos / 3600 / 1000],
                    ["Wheel", "Acceleration force", acc_pos / 3600 / 1000],
                    ["Rolling resistance", "Losses", rol_pos / 3600 / 1000],
                    ["Air resistance", "Losses", air_pos / 3600 / 1000],
                    ["Gravity force", "Kinetic energy", gra_neg / 3600 / 1000],
                    ["Gravity force", "Losses", (gra_pos - gra_neg) / 3600 / 1000],
                    ["Acceleration force", "Kinetic energy", acc_neg / 3600 / 1000],
                    ["Acceleration force", "Losses", (acc_pos - acc_neg) / 3600 / 1000],
                    [
                        "Kinetic energy",
                        "Transmission of regenerative",
                        (acc_neg + gra_neg) / 3600 / 1000,
                    ],
                    [
                        "Transmission of regenerative",
                        "Generator",
                        P_gen_in_t / 3600 / 1000,
                    ],
                    [
                        "Transmission of regenerative",
                        "Losses",
                        Loss_trans_g / 3600 / 1000,
                    ],
                    ["Generator", "Regenerative breaking", P_g_out_t / 3600 / 1000],
                    ["Generator", "Losses", Loss_gen / 3600 / 1000],
                    ["Cooling", "Losses", cooling / 3600 / 1000],
                    ["Heating", "Losses", heating / 3600 / 1000],
                    ["Auxiliary", "Losses", P_aux_t / 3600 / 1000],
                ]

                link_label = []
                for lk in stv:
                    llk = [lk[0], lk[1], str(round(lk[2], 1))]
                    link_label.append("->".join(llk))

                sort = np.array(stv, dtype=object)
                s = sort.T[0].tolist()
                t = sort.T[1].tolist()
                v = sort.T[2]

                balance = {}
                balance["label"] = [
                    "Heat source",
                    "Potential energy",
                    "Battery",
                    "Discharge",
                    "Regenerative breaking",
                    "HVAC",
                    "Motor",
                    "Generator",
                    "Transmission of traction",
                    "Wheel",
                    "Kinetic energy",
                    "Cooling",
                    "Heating",
                    "Auxiliary",
                    "Gravity force",
                    "Acceleration force",
                    "Rolling resistance",
                    "Air resistance",
                    "Losses",
                    "Transmission of regenerative",
                ]
                balance["source"] = [balance["label"].index(i) for i in s]
                balance["target"] = [balance["label"].index(i) for i in t]
                balance["value"] = v
                balance["link_label"] = link_label
                balance["data"] = stv
                trip.balance = balance
        print("")

    def save_profile(self, folder, description=" "):
        """
        folder: string, where the files will be stored. Folder is created in case it does not exist.
        description: string
        """
        self.description = description
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, self.name + ".pickle")
        with gzip.open(filepath, "wb") as datei:
            pickle.dump(self.__dict__, datei)
        print("=== profile saved === : " + filepath)
        logger.info("=== profile saved === : " + filepath)

