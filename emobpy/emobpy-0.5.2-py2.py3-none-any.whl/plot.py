import pandas as pd
import numpy as np
from .functions import balance

try:
    import plotly.graph_objects as go
    from plotly.offline import iplot
    import cufflinks as cf

    cf.go_offline()
except ImportError:
    raise Exception("This plotly code only works within a jupyter notebook")

from IPython.display import display, HTML


class NBplot:
    """
    Work in Jupyter notebooks only.
    Set of plots for a single time series and groups.
    self.__init__(db)
        db is an instance of a DataBase class that contains the time series.
    Three kind of plots:
        self.sgplot_dp(tscode) for driving profiles
        self.sgplot_ga(tscode) for grid availability profiles
        self.sgplot_ged(tscode) for grid electricity demand profiles
            tscode: time series code (string of profile name)
    """

    def __init__(self, db):
        self.db = db

    def sgplot_dp(self, tscode, rng=None, to_html=False, path=None):
        """
        plot of a single driving profile
        tscode is time series code. Eg. 'ev_user_W3_85e59'
        """
        if rng is None:
            df = self.db.db[tscode]["timeseries"].copy()
        else:
            df = self.db.db[tscode]["timeseries"].iloc[rng[0] : rng[1]].copy()
        if self.db.db[tscode]["kind"] != "driving":
            raise Exception(
                "code '{}' does not correspond to a driving profile".format(tscode)
            )

        cnt = df.groupby([df.index, "state"])["state"].count()
        cn = (
            pd.DataFrame(cnt)
            .rename(columns={"state": "count"})
            .unstack(level=-1)
            .fillna(0)
        )
        cn.columns = cn.columns.droplevel()
        rr = (cn.T / cn.T.sum(axis=0)).T
        figa = rr.iplot(kind="area", fill=True, asFigure=True)
        figb = df["distance"].iplot(asFigure=True)
        fig = cf.subplots([figa, figb], shape=(2, 1), shared_xaxes=True)
        fig["layout"]["yaxis"].update(
            {"title": "Location", "rangemode": "tozero", "domain": [0.7, 1.0]}
        )
        fig["layout"]["yaxis2"].update(
            {"title": "Distance (km)", "rangemode": "tozero", "domain": [0.0, 0.65]}
        )
        iplot(fig, show_link=False)
        FIG = go.Figure(data=fig["data"], layout=fig["layout"])
        if to_html:
            if path is None:
                raise Exception(
                    """when to_html is True then path must be given with .html extension"""
                )
            else:
                FIG.write_html(file=path)
        return FIG

    def sgplot_ga(self, tscode, rng=None, to_html=False, path=None):
        """
        plot of a single grid availability profile
        tscode is time series code. Eg. 'ev_user_W3_85e59_avai_65t2p'
        """
        if rng is None:
            df = self.db.db[tscode]["timeseries"].copy()
        else:
            df = self.db.db[tscode]["timeseries"].iloc[rng[0] : rng[1]].copy()
        if self.db.db[tscode]["kind"] != "availability":
            raise Exception(
                "code '{}' does not correspond to a grid availability profile".format(
                    tscode
                )
            )

        dt = df[["state", "consumption", "charging_point", "charging_cap", "soc"]]
        cnt = dt.groupby([dt.index, "state"])["state"].count()
        cn = (
            pd.DataFrame(cnt)
            .rename(columns={"state": "count"})
            .unstack(level=-1)
            .fillna(0)
        )
        cn.columns = cn.columns.droplevel()
        rr = (cn.T / cn.T.sum(axis=0)).T
        figa = rr.iplot(kind="area", fill=True, asFigure=True)
        dk = dt[["consumption", "charging_cap"]]
        figb = dk.iplot(asFigure=True)
        dd = dt["soc"]
        figc = dd.iplot(asFigure=True)
        fig = cf.subplots([figa, figb, figc], shape=(3, 1), shared_xaxes=True)
        fig["layout"]["xaxis"].update(
            {"tickfont": {"family": "Arial, sans-serif", "size": 13, "color": "black"}}
        )
        fig["layout"]["yaxis"].update(
            {
                "title": "Location",
                "titlefont": {"size": 12},
                "showgrid": False,
                "showline": True,
                "rangemode": "tozero",
                "zeroline": True,
                "domain": [0.75, 1.0],
                "tickformat": "%",
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 12,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"]["yaxis2"].update(
            {
                "title": "Grid Availability (kW)",
                "titlefont": {"size": 12},
                "showgrid": True,
                "showline": True,
                "rangemode": "tozero",
                "domain": [0.4, 0.7],
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 12,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"]["yaxis3"].update(
            {
                "title": "SOC",
                "titlefont": {"size": 12},
                "showgrid": True,
                "showline": True,
                "rangemode": "tozero",
                "domain": [0.0, 0.35],
                "tickformat": "%",
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 12,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"].update(
            {
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "margin": dict(l=10, r=10, t=20, b=10, pad=0),
            }
        )  # ,'width': 800,'height': 450,'showlegend': True
        iplot(fig, show_link=False)
        FIG = go.Figure(data=fig["data"], layout=fig["layout"])
        if to_html:
            if path is None:
                raise Exception(
                    """when to_html is True then path must be given with .html extension"""
                )
            else:
                FIG.write_html(file=path)
        return FIG

    def sgplot_ged(self, tscode, rng=None, to_html=False, path=None):
        """
        plot of grid electricity demand profiles associated with the same grid availability profile
        tscode is time series code. Eg. 'ev_user_W3_85e59_avai_65t2p'
        """
        if self.db.db[tscode]["kind"] != "charging":
            raise Exception(
                "code '{}' does not correspond to a grid electricity demand profile".format(
                    tscode
                )
            )
        df = pd.DataFrame()
        availcode = self.db.db[tscode]["input"]
        for k in self.db.db.keys():
            if self.db.db[k]["kind"] == "charging":
                if self.db.db[k]["input"] == availcode:
                    tmp = self.db.db[k]["timeseries"].copy()
                    tmp.loc[:, "option"] = self.db.db[k]["option"]
                    df = df.append(tmp, sort=False)

        if rng is None:
            pass
        else:
            df = df.iloc[rng[0] : rng[1]].copy()

        dt = df[["state", "actual_soc", "charge_grid", "option"]]
        cnt = dt.groupby([dt.index, "state"])["state"].count()
        cn = (
            pd.DataFrame(cnt)
            .rename(columns={"state": "count"})
            .unstack(level=-1)
            .fillna(0)
        )
        cn.columns = cn.columns.droplevel()
        rr = (cn.T / cn.T.sum(axis=0)).T
        figc = rr.iplot(kind="area", fill=True, asFigure=True)
        dff = dt.pivot_table(
            index=dt.index, columns="option", values="actual_soc", aggfunc="sum"
        )
        figa = dff.iplot(asFigure=True)
        dg = dt.pivot_table(
            index=dt.index, columns="option", values="charge_grid", aggfunc="sum"
        )
        figb = dg.iplot(asFigure=True)
        fig = cf.subplots([figa, figb, figc], shape=(3, 1), shared_xaxes=True)
        fig["layout"]["xaxis"].update(
            {"tickfont": {"family": "Arial, sans-serif", "size": 14, "color": "black"}}
        )
        fig["layout"]["yaxis"].update(
            {
                "title": "SOC",
                "titlefont": {"size": 14},
                "showgrid": False,
                "showline": True,
                "rangemode": "tozero",
                "zeroline": True,
                "domain": [0.7, 1.0],
                "tickformat": "%",
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 14,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"]["yaxis2"].update(
            {
                "title": "Actual charge (kW)",
                "titlefont": {"size": 14},
                "showgrid": True,
                "showline": True,
                "rangemode": "tozero",
                "domain": [0.25, 0.65],
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 12,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"]["yaxis3"].update(
            {
                "title": "Location",
                "titlefont": {"size": 14},
                "showgrid": True,
                "showline": True,
                "rangemode": "tozero",
                "domain": [0.0, 0.2],
                "tickformat": "%",
                "tickfont": {
                    "family": "Arial, sans-serif",
                    "size": 12,
                    "color": "black",
                },
                "linewidth": 2,
            }
        )
        fig["layout"].update(
            {
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "margin": dict(l=10, r=10, t=20, b=10, pad=0),
                "showlegend": True,
            }
        )  # 'width': 800,'height': 450
        iplot(fig, show_link=False)
        FIG = go.Figure(data=fig["data"], layout=fig["layout"])
        if to_html:
            if path is None:
                raise Exception(
                    """when to_html is True then path must be given with .html extension"""
                )
            else:
                FIG.write_html(file=path)
        return FIG

    def sankey(self, tscode, include=None, to_html=False, path=None):
        distance, consumption, rate, label, source, target, value = balance(
            self.db, tscode, include=include
        )

        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=50, thickness=10)
        data = go.Sankey(link=link, node=node)
        fig = go.Figure(data)
        if to_html:
            if path is None:
                raise Exception(
                    """when to_html is True then path must be given with .html extension"""
                )
            else:
                fig.write_html(file=path)
        print(f"Consumption [kWh]: {consumption}")
        print(f"Distance [km]: {distance}")
        print(f"Specific consumption [kWh/100 km]: {rate}")
        return fig
