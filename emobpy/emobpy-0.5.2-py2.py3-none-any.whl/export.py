import pandas as pd
import numpy as np
import os


class Export:
    """
    exp = Export()
    exp.loaddata(db), where db is an instance of DataBase Class.
    exp.to_csv()
    exp.save_files('csv')
    """

    def __init__(self, groupbyhr=True, rows=None, kwto="MW"):
        super(Export, self).__init__()
        conversion = {"kW": 1, "MW": 1000, "GW": 1000_000}
        self.kwto = kwto
        self.groupbyhr = groupbyhr
        self.row = rows
        self.conversion = conversion[self.kwto]

    def loaddata(self, db):
        self.data = db

    def to_csv(self):
        self.code = []
        self.name = []
        self.consum = []
        self.availcap = []
        self.fleet = pd.DataFrame()

        self.listavailkeys = []
        self.k = 0
        for key in self.data.db.keys():
            if self.data.db[key]["kind"] == "availability":
                self.k += 1
                self.listavailkeys.append(key)

        for i, key in enumerate(self.listavailkeys):
            df = self.data.db[key]["profile"][
                ["hh", "consumption", "charging_cap"]
            ].copy()
            if self.groupbyhr:
                df.loc[:, "hh"] = df["hh"].astype(int)
                dfcon = df.groupby("hh")["consumption"].sum().reset_index()
                dfcha = df.groupby("hh")["charging_cap"].mean().reset_index()
                dfcon.loc[:, "charging_cap"] = dfcha["charging_cap"]
                df = dfcon.copy()
            if self.row is None:
                self.rows = len(df)
            else:
                self.rows = self.row
                df = df[0 : self.rows].copy()
            self.code.append(key)
            self.name.append("ev" + str(i + 1))
            self.consum.append(df["consumption"].values / self.conversion)
            self.availcap.append(df["charging_cap"].values / self.conversion)

            self.fleet.loc[i, "EV"] = "ev" + str(i + 1)
            self.fleet.loc[i, "efficiency_charge"] = self.data.db[key]["charging_eff"]
            self.fleet.loc[i, "efficiency_discharge"] = self.data.db[key][
                "discharging_eff"
            ]
            self.fleet.loc[i, "ev_start"] = self.data.db[key]["soc_init"]
            self.fleet.loc[i, "ev_capacity"] = (
                self.data.db[key]["battery_capacity"] / self.conversion
            )
            self.fleet.loc[i, "share_ev"] = 1 / self.k
            # self.fleet.loc[i, 'cons_rate'] = self.data.db[key][
            #     'consumption'] / self.conversion
            self.fleet.loc[i, "Passed"] = self.data.db[key]["success"]
            self.fleet.loc[i, "info"] = [self.data.db[key]["description"]]
            self.fleet.loc[i, "code"] = key
            self.fleet.loc[i, "ev_end"] = self.data.db[key]["soc_end"]

        self.arr_cons = np.array(self.consum)
        self.arr_avai = np.array(self.availcap)

        self.consdf = pd.DataFrame(self.arr_cons.T, columns=self.name)
        self.consdf.columns = pd.MultiIndex.from_product(
            [["Demand_" + self.kwto + "h"], ["ev_ed"], self.consdf.columns]
        )

        self.avaidf = pd.DataFrame(self.arr_avai.T, columns=self.name)
        self.avaidf.columns = pd.MultiIndex.from_product(
            [["Grid_connect_" + self.kwto], ["n_ev_p"], self.avaidf.columns]
        )
        self.final = self.consdf.join(self.avaidf)

        self.subscen = {}
        self.setopt = set()

        for cd in self.code:
            temp = {}
            for key in self.data.db.keys():
                if self.data.db[key]["kind"] != "driving":
                    if self.data.db[key]["input"] == cd:
                        option = self.data.db[key]["option"]
                        temp[option] = key
                        self.setopt.add(option)
            if temp:
                self.subscen[cd] = temp

        if self.subscen:
            self.optdict = dict(zip(self.setopt, range(len(self.setopt))))
            self.arr_options = np.empty((len(self.setopt), len(self.code), self.rows))
            for id1, cd in enumerate(self.code):
                if self.subscen[cd]:
                    for key, value in self.subscen[cd].items():
                        id0 = self.optdict[key]
                        df = self.data.db[value]["profile"][
                            ["hh", "charge_grid"]
                        ].copy()
                        if self.groupbyhr:
                            df.loc[:, "hh"] = df["hh"].astype(int)
                            df = df.groupby("hh").mean().reset_index()
                        df = df[0 : self.rows].copy()
                        self.arr_options[id0, id1, :] = (
                            df["charge_grid"].values / self.conversion
                        )
            # self.arr_options = self.arr_options.round(7)
            self.frame = pd.DataFrame(
                index=range(self.rows), columns=pd.MultiIndex.from_product([[], [], []])
            )
            for opt, idopt in self.optdict.items():
                dfop = pd.DataFrame(self.arr_options[idopt].T, columns=self.name)
                dfop.columns = pd.MultiIndex.from_product(
                    [[opt + "_" + self.kwto + "h"], ["ev_ged_exog"], dfop.columns]
                )
                self.frame = self.frame.join(dfop)
            self.final = self.final.join(self.frame)

        self.final["Hour", "-", "-"] = ["h" + str(j + 1) for j in range(self.rows)]
        self.final.set_index(("Hour", "-", "-"), inplace=True)
        self.final.index.name = "Hour"
        self.final = self.final.round(7)

    def save_files(self, repository=""):
        if repository:
            self.repository = repository
        else:
            self.repository = self.data.folder
        os.makedirs(self.repository, exist_ok=True)
        ts_pth = os.path.join(self.repository, "time_series.csv")
        di_pth = os.path.join(self.repository, "data_input.csv")
        self.fleet.to_csv(di_pth, index=False)
        self.final.to_csv(ts_pth)
        print(f"Summary file: {di_pth}")
        print(f"Time series file: {ts_pth}")
