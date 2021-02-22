import pandas as pd
import numpy as np
import uuid
import os
import pickle
import gzip
from numba import jit
from .constants import TIME_FREQ


def add_column_datetime(df, totalrows, reference_date, t):
    fr = {1: "H", 0.5: "30min", 0.25: "15min", 0.125: "450s"}
    freq = fr[t]
    start_date = pd.to_datetime(reference_date)
    drange = pd.date_range(start_date, periods=totalrows, freq=freq)
    df = pd.DataFrame(df.values, columns=df.columns, index=drange)
    df = df.rename_axis("date").copy()
    return df


####################################################################
# These functions are for grid availability profile creation ###
####################################################################


class Availability:
    """
    self.__init__(input)
        input: string. File name of the input profile (not the path).
        The input should be in this case a driving profile name.

    Methods in the following order:
        self.setScenario(charging_data)
        self.setVehicleFeature(battery_capacity, charging_eff)
        self.setBatteryRules(soc_init, soc_min, altern=[])
        self.loadSettingDriving(DataBase)
        self.run()
        self.save_profile(folder, description=' ')
    """

    def __init__(self, input, DB):
        self.kind = "availability"
        self.input = input
        self.loadSettingDriving(DB)
        self.discharging_eff = self.vehicle.parameters["Battery_discharging_efficiency"]
        self.setVehicleFeature(
            self.vehicle.parameters["Battery capacity kWh (kilowatt hours)"],
            self.vehicle.parameters["Battery_charging_efficiency"],
        )
        self.setBatteryRules()

    def loadSettingDriving(self, DataBase):
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
            self.states
        """
        if DataBase.db[self.input]:
            if DataBase.db[self.input]["kind"] == "consumption":
                self.df = (
                    DataBase.db[self.input]["profile"][
                        [
                            "hr",
                            "state",
                            "distance",
                            "consumption kWh",
                            "consumption kWh/100 km",
                        ]
                    ]
                    .fillna(0)
                    .copy()
                )
                self.t = DataBase.db[self.input]["t"]
                self.totalrows = DataBase.db[self.input]["totalrows"]
                self.hours = DataBase.db[self.input]["hours"]
                self.freq = TIME_FREQ[self.t]["f"]
                self.refdate = DataBase.db[self.input]["refdate"]
                self.states = DataBase.db[self.input]["states"]
                self.vehicle = DataBase.db[self.input]["vehicle"]

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

    def setVehicleFeature(self, battery_capacity, charging_eff):
        """
        battery_capacity: int, kWh
        charging_eff: float
        """
        self.battery_capacity = battery_capacity
        self.charging_eff = charging_eff

    def setBatteryRules(self, soc_init=0.5, soc_min=0.02, altern=[]):
        """
        soc_init: float, [0-1]
        soc_min: float, [0-1]
        altern: list, kWh larger than battery_capacity.
        """
        self.soc_init = soc_init
        self.soc_min = soc_min
        self.storage_altern = altern[:]

    def setScenario(self, charging_data):
        """
        charging_data: dictionary. See example
        eg.

        {'prob_charging_point' :
             {'errands':  {'public':0.3,'none':0.7},
              'escort':   {'public':0.3,'none':0.7},
              'leisure':  {'public':0.3,'none':0.7},
              'shopping': {'public':0.3,'none':0.7},
              'home':     {'public':0.3,'none':0.7},
              'workplace':{'public':0.0,'workplace':0.3,'none':0.7},
              'driving':  {'none':1.0}
              },
        'capacity_charging_point' :
              {'public':11,'home':1.8,'workplace':5.5,'none':0}
        }

        """
        self.chargingdata = charging_data

    def initial_conf(self):
        self.prob_charging_point = self.chargingdata["prob_charging_point"]
        self.capacity_charging_point = self.chargingdata["capacity_charging_point"]
        self.name = self.input + "_avai_" + uuid.uuid4().hex[0:5]

    def ChooseChargingPoint(self, state):
        if state != "driving":
            self.chrg_points = [key for key in self.prob_charging_point[state].keys()]
            self.prob = [val for val in self.prob_charging_point[state].values()]
            self.rnd_name = np.random.choice(self.chrg_points, p=self.prob)
            return self.rnd_name
        else:
            return "none"

    def ChooseChargingPointFast(self, row):
        if row["consumption kWh"] > 0.85 * self.battery_capacity:
            self.chrg_points = [
                key for key in self.prob_charging_point[row["state"]].keys()
            ]
            if "none" in self.chrg_points:
                idx = self.chrg_points.index("none")
                del self.chrg_points[idx]
                if not self.chrg_points:
                    raise Exception(
                        f'This profile has a long distance trip ({row["consumption kWh"]} kWh), higher than battery capacity (0.85 * {self.battery_capacity}). Add fast charging stations'
                    )
                self.prob = [
                    val for val in self.prob_charging_point[row["state"]].values()
                ]
                del self.prob[idx]
                total = sum(self.prob)
                if total == 0:
                    self.rnd_name = self.chrg_points[0]
                    return self.rnd_name
                self.prob = [x / total for x in self.prob]
                self.rnd_name = np.random.choice(self.chrg_points, p=self.prob)
                return self.rnd_name
            else:
                if not self.chrg_points:
                    raise Exception(
                        f'This profile has a long distance trip ({row["consumption kWh"]} kWh), higher than battery capacity (0.85 * {self.battery_capacity}). Add fast charging stations'
                    )
                self.prob = [
                    val for val in self.prob_charging_point[row["state"]].values()
                ]
                self.rnd_name = np.random.choice(self.chrg_points, p=self.prob)
                return self.rnd_name
        else:
            self.chrg_points = [
                key for key in self.prob_charging_point[row["state"]].keys()
            ]
            self.prob = [val for val in self.prob_charging_point[row["state"]].values()]
            self.rnd_name = np.random.choice(self.chrg_points, p=self.prob)
            return self.rnd_name

    def drawing_soc(self):
        self.point = "driving"
        self.statesplusdrv = list(set(self.dt.loc[:, "state"]))
        self.pointcode = self.statesplusdrv.index(self.point)
        self.numpy_array3 = self.dt[["state"]].values.T
        self.arraystringstate = self.numpy_array3[0]
        self.arraycodestate = np.array(
            [self.statesplusdrv.index(s) for s in self.arraystringstate]
        )
        numpy_array = self.dt[["consumption", "charging_cap"]].values.T
        self.dt.loc[:, "soc"] = self.soc(
            self.pointcode,
            self.charging_eff,
            self.battery_capacity,
            self.soc_init,
            self.arraycodestate,
            *numpy_array,
            self.t,
        )

    @staticmethod
    @jit(nopython=True)
    def soc(
        driving_code,
        charging_eff,
        battery_capacity,
        soc_init,
        state,
        consumption,
        charging_cap,
        t,
    ):
        soc = np.empty(consumption.shape)
        rows = soc.shape[0]
        for i in range(rows):
            if i == 0:
                zero = soc_init
                current_soc = (
                    zero
                    - consumption[i] / battery_capacity
                    + charging_cap[i] * t * charging_eff / battery_capacity
                )
                if current_soc > 1:
                    soc[i] = 1
                else:
                    soc[i] = current_soc
            else:
                zero = soc[i - 1]
                if state[i] == driving_code:
                    if zero == 1:
                        current_soc = zero - consumption[i] / battery_capacity
                        soc[i] = current_soc
                    else:
                        current_soc = (
                            zero
                            - consumption[i] / battery_capacity
                            + charging_cap[i] * t * charging_eff / battery_capacity
                        )
                        if current_soc > 1:
                            soc[i] = 1
                        else:
                            soc[i] = current_soc
                else:
                    current_soc = (
                        zero
                        - consumption[i] / battery_capacity
                        + charging_cap[i] * t * charging_eff / battery_capacity
                    )
                    if current_soc > 1:
                        soc[i] = 1
                    else:
                        soc[i] = current_soc
        return soc

    @staticmethod
    @jit(nopython=True)
    def soc_old(charging_eff, battery_capacity, soc_init, consumption, charging_cap, t):
        """
        state of charge of battery
        """
        soc = np.empty(consumption.shape)
        for i in range(soc.shape[0]):
            if i == 0:
                zero = soc_init
                current_soc = (
                    zero
                    - consumption[i] / battery_capacity
                    + charging_cap[i] * t * charging_eff / battery_capacity
                )
                if current_soc > 1:
                    soc[i] = 1
                else:
                    soc[i] = current_soc
            else:
                zero = soc[i - 1]
                current_soc = (
                    zero
                    - consumption[i] / battery_capacity
                    + charging_cap[i] * t * charging_eff / battery_capacity
                )
                if current_soc > 1:
                    soc[i] = 1
                else:
                    soc[i] = current_soc
        return soc

    def testing_soc(self):
        self.failed_chrg = self.dt[self.dt["soc"] < self.soc_min].copy()
        if self.failed_chrg.empty:
            if self.dt["soc"].iloc[-1] >= self.soc_init:
                self.soc_end = round(self.dt["soc"].iloc[-1], 3)
                print(
                    "soc_init:", round(self.soc_init, 3), "--> soc_end:", self.soc_end
                )
                self.success = True
                self.notation = "True"
                self.ready = True
            else:
                self.drivlist = self.dt[self.dt["state"] == "driving"].index.to_list()[
                    ::-1
                ]
                self.len = len(self.dt)
                for ix in self.drivlist:
                    self.dt.loc[ix, "consumption"] = 0.0
                    self.drawing_soc()
                    if self.dt["soc"].iloc[-1] >= self.soc_init:
                        break
                self.new_len = len(self.dt[:ix])
                self.proportion_ts_modified = round(self.new_len / self.len, 3)
                if self.dt["soc"].iloc[-1] >= self.soc_init:
                    self.stored_n += 1
                    self.stored_success_prop.append(self.proportion_ts_modified)
                    self.stored_success.append(self.dt.copy())
                    if self.stored_n == 3:
                        self.dt = self.stored_success[
                            max(
                                enumerate(self.stored_success_prop),
                                key=lambda tup: tup[1],
                            )[0]
                        ].copy()
                        self.proportion_ts_modified = max(
                            enumerate(self.stored_success_prop), key=lambda tup: tup[1]
                        )[1]
                        self.success = True
                        self.notation = str(self.proportion_ts_modified)
                        self.ready = True
                        print(
                            "Consumption set zero for the last trips. Time steps share:",
                            max(
                                enumerate(self.stored_success_prop),
                                key=lambda tup: tup[1],
                            )[1],
                        )
                        self.soc_end = round(self.dt["soc"].iloc[-1], 3)
                        print(
                            "soc_init:",
                            round(self.soc_init, 3),
                            "--> soc_end:",
                            self.soc_end,
                        )

        if not self.ready:
            if self.n % 40 == 0:
                if self.n != 0:
                    print(
                        "still in while loop after ",
                        self.n,
                        " iterations. Battery may be small, or few charging points available...",
                    )
            if self.n % 80 == 0:
                if self.n != 0:
                    if self.battopt:
                        print(
                            "Change battery capacity from {} kWh to {} kWh".format(
                                self.battery_capacity, self.battopt[0]
                            )
                        )
                        self.battery_capacity = self.battopt[0]
                        self.battopt.remove(self.battopt[0])
                    else:
                        self.success = False
                        self.notation = "Faulty"  # save anyway but it must be verified
                        self.name = self.name + "_FAIL"
                        print(
                            " ----- !!! UNSUCCESSFUL profile creation !!! ----- please check this '{}', it may need to increase battery capacity or soc init is too low".format(
                                self.name
                            )
                        )
                        self.ready = True

    def fill_rows(self):
        self.repeats = [
            "hr",
            "state",
            "charging_point",
            "charging_cap",
            "distance",
            "consumption",
        ]
        self.fixed = ["consumption kWh"]
        self.copied = []
        self.calc = ["dayhrs"]
        self.same = []

        self.dt = pd.DataFrame(columns=self.db.columns)
        self.dt.loc[:, "hh"] = np.arange(0, self.hours, self.t)
        self.idx = self.dt[self.dt["hh"].isin(self.db["hr"].tolist())].index.tolist()
        self.mixed = self.repeats + self.fixed + self.copied
        for r in self.mixed:
            self.val = self.db[r].values.tolist()
            self.dt.loc[self.idx, r] = self.val
        self.dt.loc[self.totalrows - 1, "state"] = self.db["state"].iloc[-1]
        self.dt.loc[self.totalrows - 1, "hr"] = self.dt["hh"][self.totalrows - 1]
        self.rp = self.dt[::-1].reset_index(drop=True)
        self.rp.loc[:, self.repeats] = self.rp[self.repeats].fillna(method="ffill")
        self.rp.loc[:, self.fixed] = self.rp[self.fixed].fillna(0)
        self.dt = self.rp[::-1].reset_index(drop=True)
        for sm in self.same:
            self.dt.loc[:, sm] = self.db[sm].values.tolist()[0]
        for cal in self.calc:
            self.dt.loc[:, cal] = self.dt["hh"].apply(lambda x: x % 24)
        self.dt.loc[:, "count"] = self.dt.groupby(["hr", "state"])[
            "consumption"
        ].transform("count")
        self.dt.loc[:, "consumption"] = (
            self.dt.loc[:, "consumption"] / self.dt.loc[:, "count"]
        )
        self.dt.loc[:, "distance"] = (
            self.dt.loc[:, "distance"] / self.dt.loc[:, "count"]
        )
        # convert this section to numba
        flag = False
        for i, row in self.dt.iterrows():
            if flag:
                if row["state"] == "driving":
                    flag = True
                    if self.cumcons != 0 and self.cumchrg == 0:
                        self.cumcons += row["consumption"]
                        if self.cumcons < self.battery_capacity * 0.50:
                            self.dt.loc[i, "charging_cap"] = 0
                            self.dt.loc[i, "charging_point"] = "none"
                            self.cumchrg = 0
                        else:
                            self.cumchrg += row["charging_cap"] * self.t
                            self.cumcons = 0
                    else:
                        self.cumchrg += row["charging_cap"] * self.t
                        if self.cumchrg > self.battery_capacity * 0.5:
                            self.cumchrg = 0
                            self.cumcons += 0.001
                        else:
                            pass
                else:
                    flag = False
            elif row["state"] == "driving":
                flag = True
                self.cumcons = row["consumption"]
                if self.cumcons < self.battery_capacity * 0.65:
                    self.dt.loc[i, "charging_cap"] = 0
                    self.dt.loc[i, "charging_point"] = "none"
                    self.cumchrg = 0
                else:
                    self.cumchrg = row["charging_cap"] * self.t
                    self.cumcons = 0

    def run(self):
        """
        No input required.
        Once it finishes the following attributes can be called.
        Attributes:
            'kind',
            'input',
            'chargingdata',
            'battery_capacity',
            'charging_eff',
            'discharging_eff',
            'soc_init',
            'soc_min',
            'storage_altern',
            'profile',
            'timeseries',
            'success',
            'name',
            'proportion_ts_modified'
        """
        self.initial_conf()
        self.battopt = self.storage_altern[:]
        self.battopt.sort()
        self.ready = False
        self.proportion_ts_modified = 1.0
        self.stored_success = []
        self.stored_success_prop = []
        self.stored_n = 0
        self.n = 0
        self.df.loc[:, "dayhrs"] = self.df["hr"] % 24
        self.df.loc[:, "consumption"] = self.df["consumption kWh"]
        while True:
            self.db = self.df.copy()
            self.db.loc[:, "charging_point"] = self.df["state"].apply(
                lambda state: self.ChooseChargingPoint(state)
            )
            self.db.loc[
                self.df[self.df["state"] == "driving"].index, "charging_point"
            ] = self.df[self.df["state"] == "driving"].apply(
                self.ChooseChargingPointFast, axis=1
            )
            self.db.loc[:, "charging_cap"] = self.db["charging_point"].apply(
                lambda charging_point: self.capacity_charging_point[charging_point]
            )
            self.fill_rows()
            self.drawing_soc()
            self.testing_soc()
            if self.ready:
                break
            else:
                self.n += 1
        self.profile = self.dt[
            [
                "hh",
                "state",
                "distance",
                "consumption",
                "charging_point",
                "charging_cap",
                "soc",
                "consumption kWh",
                "count",
            ]
        ].copy()
        self.timeseries = add_column_datetime(
            self.profile.copy(), self.totalrows, self.refdate, self.t
        )

        to_rem = list(self.__dict__.keys())[:]

        keep_attr = [
            "kind",
            "input",
            "chargingdata",
            "battery_capacity",
            "charging_eff",
            "discharging_eff",
            "soc_init",
            "soc_min",
            "soc_end",
            "storage_altern",
            "profile",
            "timeseries",
            "success",
            "name",
            "proportion_ts_modified",
            "totalrows",
            "refdate",
            "t",
            "notation",
        ]

        for r in keep_attr:
            if r in to_rem:
                to_rem.remove(r)
        for attr in to_rem:
            self.__dict__.pop(attr, None)
        del to_rem
        print("Profile done: " + self.name)

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

