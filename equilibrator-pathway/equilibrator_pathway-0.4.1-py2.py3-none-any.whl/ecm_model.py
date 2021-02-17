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
import warnings
from typing import Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from equilibrator_api import Q_, ComponentContribution
from sbtab import SBtab

from .cost_function import EnzymeCostFunction
from .ecm_solution import PathwayEcmSolution
from .thermo_models import ThermodynamicModel
from .util import ECF_DEFAULTS


class EnzymeCostModel(object):
    """A class for Enzyme Cost Minimization analysis."""

    DATAFRAME_NAMES = {
        "Compound",
        "Reaction",
        "ConcentrationConstraint",
        "Parameter",
        "Flux",
    }

    def __init__(
        self, thermo_model: ThermodynamicModel, param_df: pd.DataFrame
    ):
        self._thermo_model = thermo_model
        self.config_dict = dict(ECF_DEFAULTS)
        self.config_dict.update(self._thermo_model.config_dict)

        # TODO: use the stdev_factor (and the uncertainty estimates for the
        #  Gibbs energies, to somehow weigh the ECF)
        #  stdev_factor = self.config_dict.get("stdev_factor", 1.0)

        (
            rid2crc_gmean,
            rid2crc_fwd,
            rid2crc_rev,
            rid_cid2KMM,
            rid2mw,
            cid2mw,
        ) = EnzymeCostModel.read_parameters(param_df, self.config_dict)

        self.reaction_ids = list(self._thermo_model.reaction_ids)
        self.compound_ids = list(self._thermo_model.compound_ids)
        assert self._thermo_model.standard_dg_primes.check("kJ/mol")
        standard_dg_primes = np.reshape(
            self._thermo_model.standard_dg_primes, (len(self.reaction_ids), 1)
        )

        KMM = EnzymeCostModel._generate_KMM(
            self.compound_ids, self.reaction_ids, rid_cid2KMM
        )

        # we need all fluxes to be positive, so for every negative flux,
        # we multiply it and the corresponding column in S by (-1)
        dir_mat = np.diag(
            np.sign(self._thermo_model.fluxes.magnitude + 1e-10).flat
        )
        flux = dir_mat @ self._thermo_model.fluxes
        S = self._thermo_model.S.values @ dir_mat
        standard_dg = dir_mat @ standard_dg_primes

        # we only need to define get kcat in the direction of the flux
        # if we use the 'gmean' option, that means we assume we only know
        # the geometric mean of the kcat, and we distribute it between
        # kcat_fwd and kcat_bwd according to the Haldane relationship
        # if we use the 'fwd' option, we just take the kcat in the
        # direction of flux (as is) and that would mean that our
        # thermodynamic rate law would be equivalent to calculating the
        # reverse kcat using the Haldane relationship
        assert self.config_dict["kcat_source"] in ["gmean", "fwd"], (
            "unrecognized kcat source: " + self.config_dict["kcat_source"]
        )

        kcat = []
        for rid, d in zip(
            self._thermo_model.reaction_ids, np.diag(dir_mat).flat
        ):
            if self.config_dict["kcat_source"] == "gmean":
                # TODO: calculate the forward kcat using the Haldane relation
                #  and using the KMM matrix
                crc = rid2crc_gmean[rid]
            elif d >= 0:  # the flux in this reaction is forward
                crc = rid2crc_fwd[rid]
            else:  # the flux in this reaction is backward
                crc = rid2crc_rev[rid]
            kcat.append(crc.m_as("1/s"))
        kcat = Q_(kcat, "1/s")

        # TODO: turn this into a warning, if the MW data is missing, try to
        #  assign a default value
        mw_enz = []
        for rid in self.reaction_ids:
            if rid not in rid2mw:
                raise KeyError(f"This reaction is missing an enzyme MW: {rid}")
            mw_enz.append(rid2mw[rid].m_as("Da"))
        mw_enz = Q_(mw_enz, "Da")

        # TODO: fill gaps in MW data by using the equilibrator-cache
        mw_met = []
        for cid in self.compound_ids:
            if cid not in cid2mw:
                raise KeyError(f"This compound is missing a MW: {cid}")
            mw_met.append(cid2mw[cid].m_as("Da"))
        mw_met = Q_(mw_met, "Da")

        # we must remove H2O from the model, since it should not be considered
        # as a "normal" metabolite in terms of the enzyme and metabolite costs
        self.ecf = EnzymeCostFunction(
            S,
            fluxes=flux,
            kcat=kcat,
            standard_dg=standard_dg,
            KMM=KMM,
            ln_conc_lb=self._thermo_model.ln_conc_lb,
            ln_conc_ub=self._thermo_model.ln_conc_ub,
            mw_enz=mw_enz,
            mw_met=mw_met,
            params=self.config_dict,
            idx_water=self._thermo_model.idx_water,
        )

        self._val_df_dict = None
        self._met_conc_unit = Q_("M")
        self._enz_conc_unit = Q_("M")

    @staticmethod
    def from_sbtab(
        filename: Union[str, SBtab.SBtabDocument],
        comp_contrib: Optional[ComponentContribution] = None,
    ) -> "EnzymeCostModel":
        if isinstance(filename, str):
            sbtabdoc = SBtab.read_csv(filename, "pathway")
        elif isinstance(filename, SBtab.SBtabDocument):
            sbtabdoc = filename

        thermo_model = ThermodynamicModel.from_sbtab(sbtabdoc, comp_contrib)

        param_sbtab = sbtabdoc.get_sbtab_by_id("Parameter")
        assert param_sbtab, "Missing table 'Parameter' in the SBtab document"
        param_df = param_sbtab.to_data_frame()

        return EnzymeCostModel(thermo_model, param_df)

    def add_validation_data(
        self, filename: Union[str, SBtab.SBtabDocument]
    ) -> None:
        if isinstance(filename, str):
            sbtabdoc = SBtab.read_csv(filename, "pathway")
        elif isinstance(filename, SBtab.SBtabDocument):
            sbtabdoc = filename

        conc_sbtab = sbtabdoc.get_sbtab_by_id("Concentration")
        self._met_conc_unit = Q_(conc_sbtab.get_attribute("Unit"))
        assert self._met_conc_unit.check("[concentration]"), (
            "Metabolite concentration unit is not a [concentration] quantity",
            self._met_conc_unit,
        )

        enzyme_sbtab = sbtabdoc.get_sbtab_by_id("EnzymeConcentration")
        self._enz_conc_unit = Q_(enzyme_sbtab.get_attribute("Unit"))
        assert self._enz_conc_unit.check("[concentration]"), (
            "Enzyme concentration unit is not a [concentration] quantity",
            self._enz_conc_unit,
        )

        self._val_df_dict = {
            sbtab.table_id: sbtab.to_data_frame() for sbtab in sbtabdoc.sbtabs
        }

    @staticmethod
    def read_parameters(
        parameter_df: pd.DataFrame, ecf_params: dict
    ) -> Tuple[dict, ...]:
        cols = ["QuantityType", "Value", "Compound", "Reaction", "Unit"]

        rid2mw = dict()
        cid2mw = dict()
        rid2crc_gmean = dict()  # catalytic rate constant geomertic mean
        rid2crc_fwd = dict()  # catalytic rate constant forward
        rid2crc_rev = dict()  # catalytic rate constant reverse
        crctype2dict = {
            "catalytic rate constant geometric mean": rid2crc_gmean,
            "substrate catalytic rate constant": rid2crc_fwd,
            "product catalytic rate constant": rid2crc_rev,
        }

        rid_cid2KMM = {}  # Michaelis-Menten constants

        for i, row in parameter_df.iterrows():
            try:
                typ, val, cid, rid, unit = [row[c] for c in cols]
                val = Q_(float(val), unit)

                if typ in crctype2dict:
                    assert val.check(
                        "1/[time]"
                    ), "rate constants must have inverse time units"
                    val.ito("1/s")
                    crctype2dict[typ][rid] = val
                elif typ == "Michaelis constant":
                    assert val.check(
                        "[concentration]"
                    ), "Michaelis constants must have concentration units"
                    val.ito("molar")
                    rid_cid2KMM[rid, cid] = val
                elif typ == "protein molecular mass":
                    assert val.check("[mass]"), f"'{typ}' must have mass units"
                    val.ito("Da")
                    rid2mw[rid] = val
                elif typ == "molecular mass":
                    assert val.check("[mass]"), f"'{typ}' must have mass units"
                    val.ito("Da")
                    cid2mw[cid] = val
                else:
                    warnings.warn("unrecognized Parameter: " + typ)
            except AssertionError:
                raise ValueError(
                    "Syntax error in Parameter table, row %d - %s" % (i, row)
                )
        # make sure not to count water as contributing to the volume or
        # cost of a reaction
        return (
            rid2crc_gmean,
            rid2crc_fwd,
            rid2crc_rev,
            rid_cid2KMM,
            rid2mw,
            cid2mw,
        )

    @staticmethod
    def _generate_KMM(
        cids: List[str], rids: List[str], rid_cid2KMM: dict
    ) -> np.array:
        KMM = np.ones((len(cids), len(rids)))
        for i, cid in enumerate(cids):
            for j, rid in enumerate(rids):
                kmm = rid_cid2KMM.get((rid, cid), Q_(1, "M"))
                KMM[i, j] = kmm.m_as("M")
        return KMM * Q_(1, "M")

    def optimize_ecm(self) -> PathwayEcmSolution:
        return PathwayEcmSolution(self, *self.ecf.optimize_ecm())

    def pareto(self, weights: Iterable[float] = None) -> pd.DataFrame:
        return self.ecf.pareto(weights=weights)

    def _get_measured_metabolite_conc(self) -> Q_:
        assert (
            self._val_df_dict is not None
        ), "cannot validate results because no validation data was given"

        met_conc_df = self._val_df_dict["Concentration"].set_index("Compound")
        met_concentrations = Q_(
            pd.to_numeric(met_conc_df.Value)[self.compound_ids].values,
            self._met_conc_unit,
        )
        return met_concentrations

    def _get_measured_enzyme_conc(self) -> Q_:
        assert (
            self._val_df_dict is not None
        ), "cannot validate results because no validation data was given"

        enz_conc_df = self._val_df_dict["EnzymeConcentration"].set_index(
            "Reaction"
        )
        enz_concentrations = Q_(
            pd.to_numeric(enz_conc_df.Value)[self.reaction_ids].values,
            self._met_conc_unit,
        )
        return enz_concentrations
