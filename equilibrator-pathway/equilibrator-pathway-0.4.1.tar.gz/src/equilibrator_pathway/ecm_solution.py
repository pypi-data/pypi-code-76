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
from typing import Tuple

import numpy as np
import pandas as pd
from equilibrator_api import Q_
from matplotlib import pyplot as plt
from sbtab import SBtab

from .analysis_solution import PathwayAnalysisSolution
from .cost_function import EnzymeCostFunction
from .util import PlotCorrelation


class PathwayEcmSolution(PathwayAnalysisSolution):
    """Handle MDF results.

    PathwayMDFData is a container class for MDF results, with plotting
    capabilities.
    """

    def __init__(
        self, ecm_model: "EnzymeCostModel", score: float, ln_conc: np.ndarray
    ) -> None:
        """

        Parameters
        ----------
        ecm_model : EnzymeCostModel
        ln_conc : ndarray
            log concentrations at ECM optimum
        """
        super(PathwayEcmSolution, self).__init__(
            ecm_model._thermo_model, score, ln_conc
        )
        self.ecf = ecm_model.ecf

        if ecm_model._val_df_dict is not None:
            self.meas_met_conc = ecm_model._get_measured_metabolite_conc()
            self.meas_enz_conc = ecm_model._get_measured_enzyme_conc()
        else:
            self.meas_met_conc = None
            self.meas_enz_conc = None

        self.enzyme_df = pd.DataFrame(
            data=self.costs.tolist(),
            columns=["capacity", "thermodynamic", "saturation", "allosteric"],
        )

        self.enzyme_df["concentration"] = [
            np.exp(x.value) * Q_("M") for x in self.ecf.ECF(self.ln_conc)
        ]

        self.enzyme_df.insert(
            0, "reaction_id", pd.Series(list(self.reaction_ids))
        )

    @property
    def driving_forces(self) -> np.ndarray:
        """Calculate the driving forces of all reactions."""
        return self.ecf._driving_forces(self.ln_conc)

    @property
    def volumes(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the volume occupied by each enzyme and metabolite.

        Returns
        -------
        enz_vols : array
        met_vols : array
        """
        return self.ecf.get_volumes(self.ln_conc)

    @property
    def costs(self) -> np.ndarray:
        """

        Returns
        -------
        costs : array (2D)
            A matrix containing the enzyme costs separated to the 4 ECF
            factors (as columns).
            The first column is the ECF1 predicted concentrations in [M].
            The other columns are unitless (added cost, always > 1)
        """
        return self.ecf.get_enzyme_cost_partitions(self.ln_conc)

    def _get_volume_data_for_plotting(self):
        enz_vols, met_vols = self.volumes

        enz_data = sorted(zip(enz_vols.flat, self.reaction_ids), reverse=True)
        enz_vols, enz_labels = zip(*enz_data)
        enz_colors = [(0.5, 0.8, 0.3)] * len(enz_vols)

        met_data = zip(met_vols.flat, self.compound_ids)
        # remove H2O from the list and sort by descending volume
        met_data = sorted(filter(lambda x: x[1] != "h2o", met_data))
        met_vols, met_labels = zip(*met_data)
        met_colors = [(0.3, 0.5, 0.8)] * len(met_vols)

        return (
            enz_vols + met_vols,
            enz_labels + met_labels,
            enz_colors + met_colors,
        )

    def plot_volumes(self, ax: plt.axes) -> None:
        width = 0.8
        vols, labels, colors = self._get_volume_data_for_plotting()

        ax.bar(np.arange(len(vols)), vols, width, color=colors)
        ax.set_xticklabels(labels, size="medium", rotation=90)
        ax.set_ylabel("total weight [g/L]")

    def plot_volumes_pie(self, ax: plt.axes) -> None:
        vols, labels, colors = self._get_volume_data_for_plotting()
        ax.pie(vols, labels=labels, colors=colors)
        ax.set_title(f"total weight = {sum(vols):.3g} [g/L]")

    def plot_thermodynamic_profile(self, ax: plt.axes) -> None:
        """
        Plot a cumulative line plot of the dG' values given the solution
        for the metabolite levels. This was originally designed for showing
        MDF results, but is also a useful tool for ECM.
        """
        dgs = [0] + list((-self.driving_forces).flat)
        cumulative_dgs = np.cumsum(dgs)

        xticks = np.arange(0, len(cumulative_dgs)) - 0.5
        xticklabels = [""] + list(self.reaction_ids)
        ax.plot(cumulative_dgs)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha="right")
        ax.set_xlim(0, len(cumulative_dgs) - 1)
        ax.set_xlabel("")
        ax.set_ylabel(r"Cumulative $\Delta_r G'$ (kJ/mol)", family="sans-serif")

    def plot_enzyme_demand_breakdown(
        self, ax: plt.Axes, top_level: int = 3, plot_measured: bool = True
    ) -> None:
        """
        A bar plot in log-scale showing the partitioning of cost between
        the levels of kinetic costs:
        1 - capacity
        2 - thermodynamics
        3 - saturation
        4 - allosteric
        """
        assert top_level in range(1, 5)

        # give all reactions with zero cost a base value, which we will
        # also set as the bottom ylim, which will simulate a "minus infinity"
        # when we plot it in log-scale
        costs = self.costs
        base = min(filter(None, costs[:, 0])) / 2.0
        idx_zero = costs[:, 0] == 0
        costs[idx_zero, 0] = base
        costs[idx_zero, 1:] = 1.0

        bottoms = np.hstack(
            [np.ones((costs.shape[0], 1)) * base, np.cumprod(costs, 1)]
        )
        steps = np.diff(bottoms)

        labels = EnzymeCostFunction.ECF_LEVEL_NAMES[0:top_level]

        ind = range(costs.shape[0])  # the x locations for the groups
        width = 0.8
        ax.set_yscale("log")

        if plot_measured and self.meas_enz_conc is not None:
            ax.plot(
                ind,
                self.meas_enz_conc.m_as("M"),
                label="measured",
                color="gold",
                marker="d",
                markersize=7,
                linewidth=0,
                markeredgewidth=0.3,
                markeredgecolor=(0.3, 0.3, 0.3),
            )
        colors = ["tab:blue", "tab:orange", "tab:brown"]
        for i, label in enumerate(labels):
            ax.bar(
                ind,
                steps[:, i].flat,
                width,
                bottom=bottoms[:, i].flat,
                color=colors[i],
                label=label,
            )

        ax.set_xticks(ind)
        ax.set_xticklabels(self.reaction_ids, size="medium", rotation=90)
        ax.legend(loc="best", framealpha=0.2)
        ax.set_ylabel("enzyme demand [M]")
        ax.set_ylim(bottom=base)

    def validate_metabolite_conc(
        self, ax: plt.Axes, scale: str = "log"
    ) -> None:
        pred_met_conc = self.compound_df.concentration.apply(
            lambda x: x.m_as("M")
        ).values

        # remove NaNs and zeros
        mask = np.nan_to_num(self.meas_met_conc) > 0
        mask &= np.nan_to_num(pred_met_conc) > 0

        # remove compounds with fixed concentrations
        mask &= self.ecf.ln_conc_sigma > self.ecf.MINIMAL_STDEV

        PlotCorrelation(
            ax,
            self.meas_met_conc.m_as("M"),
            pred_met_conc,
            labels=self.compound_ids,
            mask=mask,
            scale=scale,
        )
        ax.set_xlabel("measured [M]")
        ax.set_ylabel("predicted [M]")

    def validate_enzyme_conc(self, ax: plt.Axes, scale: str = "log") -> None:
        pred_enz_conc = self.enzyme_df.concentration.apply(
            lambda x: x.m_as("M")
        ).values

        PlotCorrelation(
            ax,
            self.meas_enz_conc.m_as("M"),
            pred_enz_conc,
            labels=self.enzyme_df.reaction_id,
            scale=scale,
        )

        ax.set_xlabel("measured [M]")
        ax.set_ylabel("predicted [M]")

    def to_sbtab(self) -> SBtab.SBtabDocument:
        sbtabdoc = super(PathwayEcmSolution, self).to_sbtab()

        # add another table containing the optimized enzyme concentrations
        enz_df = self.enzyme_df[["reaction_id", "concentration"]].copy()
        enz_df["concentration"] = enz_df.concentration.apply(
            lambda x: f"{x.m_as('M'):.3e}"
        )
        enz_df.insert(0, "!QuantityType", "concentration of enzyme")
        enz_df = enz_df.rename(
            columns={"reaction_id": "!Reaction", "concentration": "!Value"}
        )

        enz_sbtab = SBtab.SBtabTable.from_data_frame(
            enz_df,
            table_id="Predicted enzyme levels",
            table_type="Quantity",
            unit="M",
        )
        sbtabdoc.add_sbtab(enz_sbtab)
        return sbtabdoc
