"""A general class for holding solutions to pathway analyses."""
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
from typing import Iterable, Optional

import numpy as np
import pandas as pd
from equilibrator_api import R, default_T, standard_concentration
from sbtab import SBtab

from .pathway import Pathway


class PathwayAnalysisSolution(object):
    """A general class for pathway analysis results."""

    def __init__(
        self,
        pathway: Pathway,
        score: float,
        ln_conc: np.ndarray,
        y: Optional[np.array] = None,
    ) -> None:
        """

        Parameters
        ----------
        thermo_model : ThermodynamicModel
        ln_conc : array
            log concentrations at MDF optimum
        """
        self.score = score
        self.ln_conc = ln_conc
        self.ln_conc_mu = pathway.ln_conc_mu
        self.ln_conc_sigma = pathway.ln_conc_sigma
        self.confidence_interval = pathway.CONFIDENCE_INTERVAL

        standard_dg_primes = pathway.standard_dg_primes.squeeze()

        physiological_dg_primes = standard_dg_primes.copy()
        for i, rxn in enumerate(pathway.reactions):
            physiological_dg_primes[i] += (
                rxn.physiological_dg_correction() * R * default_T
            )

        optimized_dg_primes = standard_dg_primes.copy()
        _dg_adj = (pathway.S.T @ self.ln_conc).values.squeeze()
        optimized_dg_primes += _dg_adj * R * default_T

        # add the calculated error values (due to the ΔG'0 uncertainty)
        if y is not None and pathway.dg_sigma is not None:
            optimized_dg_primes += pathway.dg_sigma @ y.squeeze()

        # adjust ΔGs to flux directions
        standard_dg_primes = pathway.I_dir @ standard_dg_primes
        physiological_dg_primes = pathway.I_dir @ physiological_dg_primes
        optimized_dg_primes = pathway.I_dir @ optimized_dg_primes

        # all dG values are in units of RT, so we convert them to kJ/mol
        reaction_data = zip(
            pathway.reaction_ids,
            pathway.reaction_formulas,
            pathway.fluxes,
            standard_dg_primes,
            physiological_dg_primes,
            optimized_dg_primes,
        )
        self.reaction_df = pd.DataFrame(
            data=list(reaction_data),
            columns=[
                "reaction_id",
                "reaction_formula",
                "flux",
                "standard_dg_prime",
                "physiological_dg_prime",
                "optimized_dg_prime",
            ],
        )

        lbs, ubs = pathway.bounds
        compound_data = zip(
            pathway.compound_ids,
            np.exp(self.ln_conc).flatten() * standard_concentration,
            lbs,
            ubs,
        )
        self.compound_df = pd.DataFrame(
            data=list(compound_data),
            columns=[
                "compound_id",
                "concentration",
                "lower_bound",
                "upper_bound",
            ],
        )

    @property
    def reaction_ids(self) -> Iterable[str]:
        return self.reaction_df.reaction_id.__iter__()

    @property
    def compound_ids(self) -> Iterable[str]:
        return self.compound_df.compound_id.__iter__()

    def to_sbtab(self) -> SBtab.SBtabDocument:
        """Generate a report (in SBtab format)."""
        sbtabdoc = SBtab.SBtabDocument("report")

        # add a table with the optimized metabolite concentrations
        met_data = []
        for row in self.compound_df.itertuples():
            met_data.append(
                (
                    "concentration",
                    row.compound_id,
                    f"{row.concentration.m_as('M'):.3e}",
                )
            )
        met_df = pd.DataFrame(
            columns=["!QuantityType", "!Compound", "!Value"], data=met_data
        )
        met_sbtab = SBtab.SBtabTable.from_data_frame(
            met_df,
            table_id="Predicted concentrations",
            table_type="Quantity",
            unit="M",
        )
        sbtabdoc.add_sbtab(met_sbtab)

        # add a table with the optimized reaction Gibbs energies
        rxn_data = []
        for row in self.reaction_df.itertuples():
            rxn_data.append(
                (
                    "reaction gibbs energy",
                    row.reaction_id,
                    f"{row.optimized_dg_prime.m_as('kJ/mol'):.3e}",
                )
            )
        rxn_df = pd.DataFrame(
            columns=["!QuantityType", "!Reaction", "!Value"], data=rxn_data
        )
        rxn_sbtab = SBtab.SBtabTable.from_data_frame(
            rxn_df,
            table_id="Predicted Gibbs energies",
            table_type="Quantity",
            unit="kJ/mol",
        )
        sbtabdoc.add_sbtab(rxn_sbtab)

        return sbtabdoc
