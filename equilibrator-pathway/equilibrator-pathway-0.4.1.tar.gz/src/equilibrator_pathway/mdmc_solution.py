"""A class for visualizing the MDMC solution."""
# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018-2020 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018-2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from typing import Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class PathwayMdmcSolution(object):
    """Handle MDMC results.

    PathwayMDFData is a container class for MDF results, with plotting
    capabilities.
    """

    def __init__(self, thermo_model, solution_df: pd.DataFrame) -> None:
        """Create PathwayMDFData object.

        :param thermo_model: a PathwayThermoModel object
        :param df: a DataFrame with all the QP results (for all lower bounds)
        """
        self.reaction_ids = list(thermo_model.reaction_ids)
        self.compound_ids = list(thermo_model.compound_ids)

        self.solution_df = solution_df
        self.solution_df["df_lb"] = self.solution_df.df_lb.round(2)

        self.min_lb = self.solution_df.df_lb.min()
        self.max_lb = self.solution_df.df_lb.max()

        # replace the internal QP names with reaction IDs and compound names
        self.solution_df["name"] = ""

        var_index_to_cpd_name = dict(enumerate(self.compound_ids))
        var_idx = self.solution_df.var_type == "var"
        self.solution_df.loc[var_idx, "name"] = self.solution_df.loc[
            var_idx, "index"
        ].apply(var_index_to_cpd_name.get)

        cnstr_index_to_rxn_name = dict(enumerate(self.reaction_ids))
        cnstr_idx = self.solution_df.var_type == "cnstr"
        self.solution_df.loc[cnstr_idx, "name"] = self.solution_df.loc[
            cnstr_idx, "index"
        ].apply(cnstr_index_to_rxn_name.get)

        self.objective_values = (
            self.solution_df[self.solution_df.var_type == "obj"]
            .set_index("df_lb")
            .value
        )
        self.objective_values.name = "Total squared Z-scores"

        grouped_df = self.solution_df.groupby(
            ["value_type", "var_type", "var_name"]
        )

        self.concentration_df = grouped_df.get_group(
            ("primal", "var", "log_conc")
        ).pivot("name", "df_lb", "value")
        self.concentration_df = np.exp(self.concentration_df)

        self.zscore_df = grouped_df.get_group(
            ("zscore", "var", "log_conc")
        ).pivot("name", "df_lb", "value")

        self._reaction_prices_df = grouped_df.get_group(
            ("shadow_price", "cnstr", "driving_force")
        ).pivot("name", "df_lb", "value")

    def reaction_prices_df(self, normalized=False) -> pd.DataFrame:
        """Get the reaction shadow prices."""
        abs_prices = self._reaction_prices_df.apply(np.abs)
        if normalized:
            # normalize the shadow prices in each column to 1
            return abs_prices.multiply(1.0 / abs_prices.sum(0))
        else:
            return abs_prices

    def plot_objectives(self, ax: Optional[plt.Axes] = None) -> None:
        """Plot the Pareto front of the two objectives."""
        if not ax:
            fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        self.objective_values.plot(style="b-", ax=ax, legend=False)
        ax.set_xlabel("lower bound on all Driving Forces [kJ/mol]")
        ax.set_ylabel("Sum of squared Z-scores")

    def plot_reaction_prices(
        self, ax: Optional[plt.Axes] = None, normalized: bool = False
    ) -> None:
        """Plot compound concentrations."""
        if not ax:
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        _df = self.reaction_prices_df(normalized=normalized)

        _df.T.plot(ax=ax, legend=False)
        for label, yvalue in _df.iloc[:, 0].items():
            ax.text(self.min_lb - 0.1, yvalue, label, ha="right", va="center")
        for label, yvalue in _df.iloc[:, -1].items():
            ax.text(self.max_lb + 0.1, yvalue, label, ha="left", va="center")
        if normalized:
            ax.set_ylabel("normalized shadow price")
        else:
            ax.set_ylabel("shadow price")
        ax.set_xlabel("lower bound on all Driving Forces [kJ/mol]")
        ax.set_xlim(self.min_lb - 1, self.max_lb + 1)

    def plot_concentrations(
        self, ax: Optional[plt.Axes] = None, show_zscores: bool = True
    ) -> None:
        """Plot all compound concentrations (and, optionally, Z-scores)."""
        if not ax:
            fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        if show_zscores:
            ax.plot(
                self.concentration_df.columns,
                self.concentration_df.values.T,
                color=(0.6, 0.6, 0.6),
                zorder=1,
            )
        else:
            self.concentration_df.T.plot(ax=ax, legend=False)

        for met, row in self.concentration_df.iterrows():
            if show_zscores:
                zscores = self.zscore_df.loc[met, :]
                sc = ax.scatter(
                    row.index,
                    row.values,
                    c=zscores,
                    s=5,
                    cmap="coolwarm",
                    vmin=-4,
                    vmax=4,
                    zorder=2,
                )
            ax.text(self.min_lb - 0.1, row.iat[0], met, ha="right", va="center")
            ax.text(self.max_lb + 0.1, row.iat[-1], met, ha="left", va="center")
        ax.set_ylabel("concentration [M]")
        ax.set_xlabel("lower bound on all Driving Forces [kJ/mol]")
        ax.set_yscale("log")
        ax.set_xlim(self.min_lb - 2, self.max_lb + 2)
        if show_zscores:
            plt.colorbar(sc, label="Z-score")

    def plot_metabolite(self, met: str) -> plt.Figure:
        """Plot a single compound's concentration."""
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        # ax = fig.gca(projection='3d')

        concentrations = self.concentration_df.loc[met, :]
        zscores = self.zscore_df.loc[met, :]
        sc = ax.scatter(
            concentrations.index,
            concentrations.values,
            c=zscores.values,
            linewidth=0,
            s=5,
        )
        # ax.text(self.min_lb - 0.1, concentrations.iat[0], met, ha="right", va="center")
        # ax.text(self.max_lb + 0.1, concentrations.iat[-1], met, ha="left", va="center")
        ax.set_ylabel("{met} concentration [M]")
        ax.set_xlabel("lower bound on all Driving Forces [kJ/mol]")
        ax.set_yscale("log")
        ax.set_xlim(self.min_lb - 2, self.max_lb + 2)
        return fig
