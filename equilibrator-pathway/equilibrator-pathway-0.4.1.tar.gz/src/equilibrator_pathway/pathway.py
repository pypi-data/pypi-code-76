"""analyze pathways using thermodynamic models."""
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
from typing import Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from equilibrator_api import Q_, ComponentContribution, Reaction
from equilibrator_cache import Compound
from sbtab import SBtab

from . import Bounds, StoichiometricModel


class Pathway(StoichiometricModel):
    """A pathway parsed from user input.

    Designed for checking input prior to converting to a stoichiometric model.
    """

    def __init__(
        self,
        reactions: List[Reaction],
        fluxes: Q_,
        comp_contrib: Optional[ComponentContribution] = None,
        standard_dg_primes: Optional[Q_] = None,
        dg_sigma: Optional[Q_] = None,
        bounds: Optional[Bounds] = None,
        config_dict: Optional[Dict[str, str]] = None,
        compound_id_mapping: Callable[[Compound], str] = None,
    ) -> None:
        """Initialize a Pathway object.

        Parameters
        ----------
        reactions : List[Reaction]
            a list of Reaction objects
        fluxes : Quantity
            relative fluxes in same order as
        comp_contrib : ComponentContribution
            a ComponentContribution object
        standard_dg_primes : Quantity, optional
            reaction energies (in kJ/mol)
        dg_sigma : Quantity, optional
            square root of the uncertainty covariance matrix (in kJ/mol)
        bounds : Bounds, optional
            bounds on metabolite concentrations (by default uses the
            "data/cofactors.csv" file in `equilibrator-api`)
        config_dict : dict, optional
            configuration parameters for Pathway analysis
        compound_id_mapping : callable, optional
            a function mapping compounds to their names in the model
        """
        super(Pathway, self).__init__(
            reactions=reactions,
            comp_contrib=comp_contrib,
            standard_dg_primes=standard_dg_primes,
            dg_sigma=dg_sigma,
            bounds=bounds,
            config_dict=config_dict,
            compound_id_mapping=compound_id_mapping,
        )

        assert fluxes.unitless or fluxes.check("[concentration]/[time]")
        self.fluxes = fluxes.flatten()
        assert self.fluxes.shape == (self.Nr,)
        self.I_dir = np.diag(np.sign(self.fluxes.magnitude).flat)

    @property
    def net_reaction(self) -> Reaction:
        """Calculate the sum of all the reactions in the pathway.

        :return: the net reaction
        """
        net_rxn_stoich = self.S @ self.fluxes.magnitude
        net_rxn_stoich = net_rxn_stoich[net_rxn_stoich != 0]
        sparse = net_rxn_stoich.to_dict()
        return Reaction(sparse)

    @property
    def net_reaction_formula(self) -> str:
        """Calculate the sum of all the reactions in the pathway.

        :return: the net reaction formula
        """
        return self._reaction_to_formula(self.net_reaction)

    @classmethod
    def from_network_sbtab(
        cls,
        filename: Union[str, SBtab.SBtabDocument],
        comp_contrib: Optional[ComponentContribution] = None,
        freetext: bool = True,
        bounds: Optional[Bounds] = None,
    ) -> object:
        """Initialize a Pathway object using a 'network'-only SBtab.

        Parameters
        ----------
        filename : str, SBtabDocument
            a filename containing an SBtabDocument (or the SBtabDocument
            object itself) defining the network (topology) only
        comp_contrib : ComponentContribution, optional
            a ComponentContribution object needed for parsing and searching
            the reactions. also used to set the aqueous parameters (pH, I, etc.)
        freetext : bool, optional
            a flag indicating whether the reactions are given as free-text (i.e.
            common names for compounds) or by standard database accessions
            (Default value: `True`)
        bounds : Bounds, optional
            bounds on metabolite concentrations (by default uses the
            "data/cofactors.csv" file in `equilibrator-api`)

        Returns
        -------
            a Pathway object
        """
        (
            reaction_df,
            comp_contrib,
            config_dict,
        ) = StoichiometricModel._read_network_sbtab(
            filename, comp_contrib, freetext
        )
        fluxes = reaction_df.RelativeFlux.apply(float).values * Q_(
            "dimensionless"
        )
        pp = Pathway(
            reactions=reaction_df.Reaction.tolist(),
            fluxes=fluxes,
            comp_contrib=comp_contrib,
            bounds=bounds,
            config_dict=config_dict,
        )
        return pp

    @classmethod
    def from_stoichiometric_model(
        cls, stoich_model: StoichiometricModel
    ) -> "Pathway":
        """Convert a StoichiometricModel into a Pathway.

        Assume all fluxes are 1.
        """
        fluxes = np.ones(len(stoich_model.reactions)) * Q_(1)
        pp = Pathway(
            reactions=stoich_model.reactions,
            fluxes=fluxes,
            comp_contrib=stoich_model.comp_contrib,
            standard_dg_primes=stoich_model.standard_dg_primes,
            dg_sigma=stoich_model.dg_sigma,
            bounds=stoich_model._bounds,
            config_dict=stoich_model.config_dict,
        )
        return pp

    @classmethod
    def from_sbtab(
        cls,
        filename: Union[str, SBtab.SBtabDocument],
        comp_contrib: Optional[ComponentContribution] = None,
    ) -> "Pathway":
        """Parse and SBtabDocument and return a StoichiometricModel.

        Parameters
        ----------
        filename : str or SBtabDocument
            a filename containing an SBtabDocument (or the SBtabDocument
            object itself) defining the pathway
        comp_contrib : ComponentContribution, optional
            a ComponentContribution object needed for parsing and searching
            the reactions. also used to set the aqueous parameters (pH, I, etc.)

        Returns
        -------
        pathway: Pathway
            A Pathway object based on the configuration SBtab

        """
        comp_contrib = comp_contrib or ComponentContribution()

        (
            sbtabdoc,
            reactions,
            reaction_ids,
            standard_dg_primes,
            dg_sigma,
            bounds,
            config_dict,
            compound_to_id,
        ) = cls._read_model_sbtab(filename, comp_contrib)

        # Read the Flux table
        # ---------------------------
        flux_sbtab = sbtabdoc.get_sbtab_by_id("Flux")
        assert flux_sbtab is not None, "Cannot find a 'Flux' table in the SBtab"
        flux_df = flux_sbtab.to_data_frame()
        assert set(flux_df.Reaction.unique()) == set(reaction_ids), (
            r"'Reaction' and 'Flux' tables are not 100% compatible (check"
            r"that the list of IDs is the same"
        )

        fluxes = (
            flux_df.set_index("Reaction")
            .loc[reaction_ids, "Value"]
            .apply(float)
        )

        fluxes = np.array(fluxes.values, ndmin=2, dtype=float).T

        try:
            # convert fluxes to M/s if they are in some other absolute unit
            flux_unit = flux_sbtab.get_attribute("Unit")
            fluxes *= Q_(1.0, flux_unit)
        except SBtab.SBtabError:
            # otherwise, assume these are relative fluxes
            fluxes *= Q_("dimensionless")

        return cls(
            reactions=reactions,
            fluxes=fluxes,
            comp_contrib=comp_contrib,
            standard_dg_primes=standard_dg_primes,
            dg_sigma=None,
            bounds=bounds,
            config_dict=config_dict,
            compound_id_mapping=compound_to_id.get,
        )

    def to_sbtab(self) -> SBtab.SBtabDocument:
        """Export the pathway to an SBtabDocument."""
        sbtabdoc = super(Pathway, self).to_sbtab()

        # add the flux table
        flux_df = pd.DataFrame(
            data=[
                ("rate of reaction", rxn.rid, f"{flux:.3g}")
                for rxn, flux in zip(self.reactions, self.fluxes.magnitude)
            ],
            columns=["!QuantityType", "!Reaction", "!Value"],
        )
        flux_sbtab = SBtab.SBtabTable.from_data_frame(
            df=flux_df, table_id="Flux", table_type="Quantity"
        )
        flux_sbtab.change_attribute("Unit", self.fluxes.units)
        sbtabdoc.add_sbtab(flux_sbtab)

        return sbtabdoc
