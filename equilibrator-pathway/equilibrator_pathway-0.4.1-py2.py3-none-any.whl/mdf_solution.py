"""thermo_models contains tools for running MDF and displaying results."""
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
from equilibrator_api import Q_, ureg
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from .analysis_solution import PathwayAnalysisSolution


class PathwayMdfSolution(PathwayAnalysisSolution):
    """Handle MDF results.

    PathwayMDFData is a container class for MDF results, with plotting
    capabilities.
    """

    def __init__(
        self,
        thermo_model: "PathwayThermoModel",
        score: float,
        ln_conc: np.array,
        y: np.array,
        reaction_prices: np.array,
        compound_prices: np.array,
    ) -> None:
        """

        Parameters
        ----------
        thermo_model : ThermodynamicModel
        score : float
            the optimal Max-min Driving Force (in kJ/mol)
        ln_conc : ndarray
            log concentrations at MDF optimum
        y : ndarray
            uncertainty matrix coefficients at MDF optimum
        reaction_prices : ndarray
            shadow prices of reactions
        compound_prices : ndarray
            shadow prices of compound concentrations
        """
        super(PathwayMdfSolution, self).__init__(
            thermo_model, score, ln_conc, y
        )
        self.reaction_df["shadow_price"] = reaction_prices
        self.compound_df["shadow_price"] = compound_prices

    def plot_concentrations(self, ax: Optional[plt.Axes] = None) -> None:
        """Plot compound concentrations.

        :return: matplotlib Figure
        """
        ureg.setup_matplotlib(True)

        if not ax:
            fig, ax = plt.subplots(
                1, 1, figsize=(10, self.compound_df.shape[0] * 0.25)
            )

        data_df = self.compound_df.copy()
        data_df["y"] = np.arange(0, data_df.shape[0])
        data_df["shadow_sign"] = data_df.shadow_price.apply(np.sign)

        for shadow_sign, group_df in data_df.groupby("shadow_sign"):
            if shadow_sign == -1:
                color, marker, label = ("blue", "<", "shadow price < 0")
            elif shadow_sign == 1:
                color, marker, label = ("red", ">", "shadow price > 0")
            else:
                color, marker, label = ("grey", "d", "shadow price = 0")

            group_df.plot.scatter(
                x="concentration",
                y="y",
                s=40,
                c=color,
                marker=marker,
                ax=ax,
                zorder=2,
                colorbar=False,
                label=label,
            )
        ax.set_ylabel("")
        ax.set_yticks(data_df.y)

        for j, row in enumerate(data_df.itertuples(index=True)):
            ax.plot(
                [row.lower_bound.m_as("M"), row.upper_bound.m_as("M")],
                [row.y, row.y],
                color="lightgrey",
                linewidth=3,
                zorder=1,
                label="allowed range" if j == 0 else None,
            )

        ax.set_yticklabels(data_df.compound_id, fontsize=9)
        ax.set_xlabel("Concentration (M)")
        ax.set_xscale("log")
        ax.set_ylim(-0.5, data_df.shape[0] + 0.5)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")

    def plot_driving_forces(self, ax: Optional[plt.Axes] = None) -> None:
        """Plot cumulative delta-G profiles.

        :return: matplotlib Figure
        """
        ureg.setup_matplotlib(True)

        if not ax:
            fig, ax = plt.subplots(
                1, 1, figsize=(3 + self.reaction_df.shape[0] * 0.3, 6)
            )

        data_df = self.reaction_df.copy()
        data_df.reindex()

        data_df[
            "cml_dgm"
        ] = self.reaction_df.physiological_dg_prime.cumsum().apply(
            lambda x: x.m_as("kJ/mol")
        )
        data_df[
            "cml_dg_opt"
        ] = self.reaction_df.optimized_dg_prime.cumsum().apply(
            lambda x: x.m_as("kJ/mol")
        )

        xticks = 0.5 + np.arange(data_df.shape[0])
        xticklabels = data_df.reaction_id.tolist()

        yvalues_phy = [0.0] + data_df.cml_dgm.tolist()
        yvalues_opt = [0.0] + data_df.cml_dg_opt.tolist()

        ax.plot(
            yvalues_phy,
            label="Physiological concentrations (1 mM)",
            color="lightgreen",
            linestyle="--",
            zorder=1,
        )
        ax.plot(
            yvalues_opt,
            label="MDF-optimized concentrations",
            color="grey",
            linewidth=2,
            zorder=2,
        )
        lines = [
            ((i, yvalues_opt[i]), (i + 1, yvalues_opt[i + 1]))
            for i in data_df[data_df.shadow_price != 0].index
        ]
        lines = LineCollection(
            lines,
            label="Bottleneck reactions",
            linewidth=3,
            color="red",
            linestyle="-",
            zorder=3,
            alpha=1,
        )
        ax.add_collection(lines)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha="center")
        ax.set_xlim(0, data_df.shape[0])

        ax.set_xlabel("Reaction Step")
        ax.set_ylabel(r"Cumulative $\Delta_r G^\prime$ (kJ/mol)")
        ax.legend(loc="best")
        ax.set_title(f"MDF = {self.score:.2f} kJ/mol")
