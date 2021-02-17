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
import itertools
import logging
from typing import Iterable, Optional, Tuple

import cvxpy as cp
import numpy as np
import pandas as pd
from cvxpy.constraints.constraint import Constraint
from cvxpy.expressions.expression import Expression
from cvxpy.problems.objective import Objective
from equilibrator_api import Q_, R, default_T

from .util import ECF_DEFAULTS


class EnzymeCostFunction(object):

    ECF_LEVEL_NAMES = [
        "capacity [M]",
        "thermodynamic",
        "saturation",
        "allosteric",
    ]
    CONFIDENCE_INTERVAL = 1.96  # TODO: move to params dict
    MINIMAL_STDEV = 1e-3  # for metabolites to be considered "fixed"
    DRIVING_FORCE_LB = 1e-3  # in kJ/mol

    def __init__(
        self,
        S: np.ndarray,
        fluxes: Q_,
        kcat: Q_,
        standard_dg: Q_,
        KMM: Q_,
        ln_conc_lb: np.ndarray,
        ln_conc_ub: np.ndarray,
        mw_enz: Optional[Q_] = None,
        mw_met: Optional[Q_] = None,
        A_act: Optional[np.ndarray] = None,
        A_inh: Optional[np.ndarray] = None,
        K_act: Optional[Q_] = None,
        K_inh: Optional[Q_] = None,
        idx_water: int = -1,
        params: Optional[dict] = None,
    ):
        """Create a Cost Function object.

        Parameters
        ----------
        S: ndarray
            stoichiometric matrix [unitless]
        fluxes: Quantity [concentration]/[time]
            steady-state fluxes [flux units]
        kcat: Quantity [1/time]
            turnover numbers
        standard_dg: Quantity [energy]/[substance]
            standard Gibbs free energies of reaction
        KMM: Quantity [concentration]
            Michaelis-Menten coefficients
        ln_conc_lb: ndarray
            lower bounds on metabolite concentrations [ln M]
        ln_conc_ub: ndarray
            upper bounds on metabolite concentrations [ln M]
        mw_enz: Quantity, optional [mass]
            enzyme molecular weights
        mw_met: Quantity, optional [mass]
            metabolite molecular weights
        A_act: ndarray, optional
            Hill coefficient matrix of allosteric activators
        A_inh: ndarray, optional
            Hill coefficient matrix of allosteric inhibitors
        K_act: Quantity, optional [concentration]
            affinity coefficient matrix of allosteric activators
        K_inh: Quantity, optional [concentration]
            affinity coefficient matrix of allosteric inhibitors
        idx_water: int
            the index of water in the stoichiometric matrix (or -1
            if water is not part of the model)
        params: dict, optional
            dictionary of extra parameters
        """
        self.params = dict(ECF_DEFAULTS)
        if params is not None:
            self.params.update(params)

        self.S = S
        self.idx_water = idx_water

        if fluxes.check("[concentration]/[time]"):
            self.fluxes = fluxes.m_as("M/s").flatten()
        elif fluxes.unitless:
            # relative fluxes are dimensionless
            self.fluxes = fluxes.m_as("").flatten()
        else:
            raise ValueError("Fluxes must be in units of M/s or dimensionless")
        assert (self.fluxes > 0.0).all()

        assert kcat.check("1/[time]")
        self.kcat = kcat.m_as("1/s").flatten()

        assert standard_dg.check("[energy]/[substance]")
        self.standard_dg_over_rt = (
            (standard_dg / (R * default_T)).m_as("").flatten()
        )

        assert KMM.check("[concentration]")
        self.KMM = KMM.m_as("M")

        self.ln_conc_lb = ln_conc_lb.flatten()
        self.ln_conc_ub = ln_conc_ub.flatten()

        # In MDMC we use Z-score to describe distribution within the metabolite
        # so we need to convert the "hard" bounds into a Gaussian distribution
        # we assume that the given bounds represent the 95% confidence interval
        # a the Gaussian distribution (i.e. [mu - 1.96*sigma, mu + 1.96*sigma])
        # Therefore:
        #              mu = (ub + lb) / 2
        #           sigma = (ub - lb) / 3.92
        self.ln_conc_mu = (self.ln_conc_ub + self.ln_conc_lb) / 2.0
        self.ln_conc_sigma = (self.ln_conc_ub - self.ln_conc_lb) / (
            self.CONFIDENCE_INTERVAL * 2.0
        )

        self.Nc, self.Nr = S.shape
        assert self.fluxes.shape == (self.Nr,)
        assert self.kcat.shape == (self.Nr,)
        assert self.standard_dg_over_rt.shape == (self.Nr,)
        assert self.KMM.shape == (self.Nc, self.Nr)
        assert self.ln_conc_lb.shape == (self.Nc,)
        assert self.ln_conc_ub.shape == (self.Nc,)

        self.cids = ["C%04d" % i for i in range(self.Nc)]

        self.S_subs = abs(self.S)
        self.S_prod = abs(self.S)
        self.S_subs[self.S > 0] = 0
        self.S_prod[self.S < 0] = 0

        # if the kcat source is 'gmean' we need to recalculate the
        # kcat_fwd using the formula:
        # kcat_fwd = kcat_gmean * sqrt(kEQ * prod_S(KMM) / prod_P(KMM))

        if self.params["kcat_source"] == "gmean":
            ln_KMM_prod = np.array(np.diag(self.S.T @ np.log(self.KMM)))
            ln_ratio = -ln_KMM_prod - self.standard_dg_over_rt
            factor = np.sqrt(np.exp(ln_ratio))
            self.kcat *= factor

        # molecular weights of enzymes and metabolites
        if mw_enz is None:
            self.mw_enz = np.ones(self.Nr)
        else:
            assert mw_met.check("[mass]")
            self.mw_enz = mw_enz.m_as("Da").flatten()
            assert self.mw_enz.shape == (self.Nr,)
            assert (self.mw_enz > 0.0).all()

        if mw_met is None:
            self.mw_met = np.ones(self.Nc)
        else:
            assert mw_met.check("[mass]")
            self.mw_met = mw_met.m_as("Da").flatten()
            assert self.mw_met.shape == (self.Nc,)
            assert (self.mw_met > 0.0).all()

        # allosteric regulation term

        if A_act is None or K_act is None:
            self.A_act = np.zeros(S.shape)
            self.K_act = np.ones(S.shape)
        else:
            assert S.shape == A_act.shape
            assert S.shape == K_act.shape
            assert K_act.check("[concentration]")
            self.A_act = A_act
            self.K_act = K_act.m_as("M")

        if A_inh is None or K_inh is None:
            self.A_inh = np.zeros(S.shape)
            self.K_inh = np.ones(S.shape)
        else:
            assert S.shape == A_inh.shape
            assert S.shape == K_inh.shape
            assert K_inh.check("[concentration]")
            self.A_inh = A_inh
            self.K_inh = K_inh.m_as("M")

        # if one of the compounds is water, we remove its effect on the
        # saturation, and the MW cost of metabolites
        if self.idx_water > -1:
            self.S_subs[self.idx_water, :] = 0
            self.S_prod[self.idx_water, :] = 0

        # preprocessing: these auxiliary matrices help calculate the ECF3 and
        # ECF4 faster
        self.act_denom = np.diag(self.A_act.T @ np.log(self.K_act))
        self.inh_denom = np.diag(self.A_inh.T @ np.log(self.K_inh))

        try:
            self.ECF = eval("self._ECF%s" % self.params["version"])
        except AttributeError:
            raise ValueError(
                "The enzyme cost function %d is unknown"
                % self.params["version"]
            )

        assert (
            self.params.get("regularization", "volume").lower() == "volume"
        ), (
            "Support to regularizations other than 'volume' was dropped when"
            "moving to CVXPY"
        )
        self.ln_capacity = cp.Constant(np.log(self.fluxes / self.kcat))

    def _driving_forces(self, ln_conc: cp.Variable) -> cp.Expression:
        """
        calculate the driving force for every reaction in every condition
        """
        return -self.standard_dg_over_rt - self.S.T @ ln_conc

    def _ln_eta_thermodynamic(self, ln_conc: cp.Variable) -> cp.Expression:
        """Calculate the minus log value of the thermodynamic efficiencies."""
        return cp.log(1.0 - cp.exp(-self._driving_forces(ln_conc)))

    def _B_matrix(
        self, col_subs: np.ndarray, col_prod: np.ndarray
    ) -> np.ndarray:
        """Build the B matrix for the eta^kin expression.

        row_subs : np.ndarray
            A column from the substrate stoichiometric matrix. We assume
            coefficients represent reactant molecularities so
            only integer values are allowed.

        row_prod : np.ndarray
            A column from the product stoichiometric matrix. We assume
            coefficients represent reactant molecularities so
            only integer values are allowed.
        """

        def K_matrix(n: int) -> np.ndarray:
            """Make the 'K' matrix for the CM rate law."""
            lst = list(itertools.product([0, 1], repeat=n))
            lst.pop(0)  # remove the [0, 0, ..., 0] row
            return np.array(lst)

        def expand_S(coeffs: np.ndarray) -> np.ndarray:
            """Expand a coefficient column into a matrix with duplicates."""
            cs = list(np.cumsum(list(map(int, coeffs.flat))))
            S_tmp = np.zeros((cs[-1], self.Nc))
            for j, (i_from, i_to) in enumerate(zip([0] + cs, cs)):
                S_tmp[i_from:i_to, j] = 1
            return S_tmp

        S_subs = expand_S(col_subs)
        S_prod = expand_S(col_prod)

        A = np.vstack(
            [
                np.zeros((1, self.Nc)),
                K_matrix(S_subs.shape[0]) @ S_subs,
                K_matrix(S_prod.shape[0]) @ S_prod,
            ]
        )

        return A - np.ones((A.shape[0], S_subs.shape[0])) @ S_subs

    def _ln_D_CM_minus_ln_D_S(self, i: int, ln_conc: cp.Variable) -> Expression:
        B = self._B_matrix(self.S_subs[:, i], self.S_prod[:, i])
        return cp.log_sum_exp(B @ (ln_conc - np.log(self.KMM[:, i])))

    def _ln_eta_kinetic(self, ln_conc: cp.Variable) -> Expression:
        """
        the kinetic part of ECF3 and ECF4
        """
        ln_KMM = np.log(self.KMM)
        ln_conc_mat = cp.vstack([ln_conc] * self.Nr).T

        ln_D_S = self.S_subs.T @ (ln_conc_mat - ln_KMM)
        ln_D_P = self.S_prod.T @ (ln_conc_mat - ln_KMM)

        if self.params["denominator"] == "S":
            return cp.Constant(np.zeros(self.Nr))
        elif self.params["denominator"] == "1S":
            return -cp.diag(cp.logistic(-ln_D_S))
        elif self.params["denominator"] == "SP":
            return -cp.diag(cp.logistic(-ln_D_S + ln_D_P))
        elif self.params["denominator"] == "1SP":
            return -cp.diag(cp.logistic(-ln_D_S + cp.logistic(ln_D_P)))
        elif self.params["denominator"] == "CM":
            ln_eta = [
                -self._ln_D_CM_minus_ln_D_S(i, ln_conc) for i in range(self.Nr)
            ]
            return cp.reshape(cp.vstack(ln_eta), (self.Nr,))
        else:
            raise ValueError(
                "unsupported denominator: " + self.params["denominator"]
            )

    def _ln_eta_allosteric(self, ln_conc: cp.Variable) -> Expression:
        ln_K_act = np.log(self.K_act)
        ln_K_inh = np.log(self.K_inh)
        ln_conc_mat = cp.vstack([ln_conc] * self.Nr).T

        # original allosteric term:
        # 1 / (1 + prod(k_a/c_a)) / (1 + prod(c_i/k_i))
        # ln_act = self.A_act.T @ (ln_conc_mat - ln_K_act)
        # ln_inh = self.A_inh.T @ (ln_conc_mat - ln_K_inh)
        # ln_eta_act = -cp.diag(cp.logistic(-ln_act))
        # ln_eta_inh = -cp.diag(cp.logistic(ln_inh))

        # new allosteric term:
        # 1 / prod(1 + k_a/c_a) / prod(1 + c_i/k_i)
        ln_act = self.A_act.T @ cp.logistic(ln_K_act - ln_conc_mat)
        ln_inh = self.A_inh.T @ cp.logistic(ln_conc_mat - ln_K_inh)
        ln_eta_act = -cp.diag(ln_act)
        ln_eta_inh = -cp.diag(ln_inh)

        return ln_eta_act + ln_eta_inh

    def is_feasible(self, ln_conc: np.ndarray) -> bool:
        df = self._driving_forces(ln_conc)
        return (df > 0).all()

    def get_fluxes(self, ln_conc: np.ndarray, E: np.ndarray) -> np.ndarray:
        """Calculate the fluxes based on metabolite and enzyme conc."""
        assert ln_conc.shape == (self.Nc,)
        assert E.shape == (self.Nr,)

        v = self.kcat * E
        v *= np.exp(self._ln_eta_thermodynamic(ln_conc).value)
        v *= np.exp(self._ln_eta_kinetic(ln_conc).value)
        v *= np.exp(self._ln_eta_allosteric(ln_conc))

        return v.squeeze()

    def _ECF1(self, ln_conc: cp.Variable) -> Expression:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            The most basic Enzyme Cost Function (only dependent on flux
            and kcat). Gives the predicted enzyme concentrations in [M]
        """
        # ln_conc is not used for ECF1
        return self.ln_capacity

    def _ECF2(self, ln_conc: cp.Variable) -> Expression:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            The thermodynamic-only Enzyme Cost Function.
            Gives the predicted enzyme concentrations in [M].
        """
        return self._ECF1(ln_conc) - self._ln_eta_thermodynamic(ln_conc)

    def _ECF3(self, ln_conc: cp.Variable) -> Expression:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            An Enzyme Cost Function that integrates kinetic and
            thermodynamic data, but no allosteric regulation.
            Gives the predicted enzyme concentrations in [M].
        """
        return self._ECF2(ln_conc) - self._ln_eta_kinetic(ln_conc)

    def _ECF4(self, ln_conc: cp.Variable) -> Expression:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            The full Enzyme Cost Function, i.e. with kinetic, thermodynamic
            and allosteric data.
            Gives the predicted enzyme concentrations in [M].
        """
        return self._ECF3(ln_conc) - self._ln_eta_allosteric(ln_conc)

    def get_enzyme_cost_partitions(self, ln_conc: np.ndarray) -> np.ndarray:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            A matrix contining the enzyme costs separated to the 4 ECF
            factors (as columns).
            The first column is the ECF1 predicted concentrations in [M].
            The other columns are unitless (added cost, always > 1)
        """
        cap = cp.exp(self.ln_capacity)  # capacity
        trm = cp.exp(-self._ln_eta_thermodynamic(ln_conc))  # thermodynamics
        kin = cp.exp(-self._ln_eta_kinetic(ln_conc))  # kinetics
        alo = cp.exp(-self._ln_eta_allosteric(ln_conc))

        return cp.vstack([cap, trm, kin, alo]).T.value

    def get_volumes(self, ln_conc: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Arguments:
            A single metabolite ln-concentration vector

        Returns:
            Two arrays containing the enzyme volumes and
            metabolite volumes (at the provided point)
        """
        enz_conc = np.exp(self.ECF(ln_conc).value)
        met_conc = np.exp(ln_conc)
        enz_vols = np.multiply(enz_conc, self.mw_enz)
        met_vols = np.multiply(met_conc, self.mw_met)

        # we have to remove the volume of water, otherwise it dominates all
        # other volumes
        met_vols[self.idx_water] = 0.0
        return enz_vols, met_vols

    def _ln_total_enzyme_weight(self, ln_conc: cp.Variable) -> Expression:
        """Calculate the enzyme cost for an input concentration profile."""
        return cp.log_sum_exp(self.ECF(ln_conc) + np.log(self.mw_enz))

    def _ln_total_metabolite_weight(self, ln_conc: cp.Variable) -> Expression:
        """Calculate the enzyme cost for an input concentration profile."""
        return cp.log_sum_exp(ln_conc + np.log(self.mw_met))

    def _create_ecm_problem(
        self, ln_conc: cp.Variable
    ) -> [Objective, Constraint]:
        obj_enz_wgt = cp.Minimize(self._ln_total_enzyme_weight(ln_conc))

        if self.params["objective"] == "enzyme + metabolite":
            obj_met_wgt = cp.Minimize(self._ln_total_metabolite_weight(ln_conc))
            obj_ec = cp.transforms.scalarize.log_sum_exp(
                [obj_enz_wgt, obj_met_wgt], weights=(1.0, 1.0)
            )
        elif self.params["objective"] == "enzyme":
            obj_ec = obj_enz_wgt
        else:
            raise ValueError(
                f"unsupported 'objective' param: {self.params['objective']}"
            )

        constraints = [
            ln_conc >= self.ln_conc_lb,
            ln_conc <= self.ln_conc_ub,
            self._driving_forces(ln_conc) >= self.DRIVING_FORCE_LB,
        ]

        return obj_ec, constraints

    def optimize_ecm(self) -> Tuple[float, np.ndarray]:
        """Minimize enzyme cost.

        Use convex optimization to find the y with the minimal total
        enzyme cost per flux, i.e. sum(ECF(ln_conc)).
        """
        ln_conc = cp.Variable(self.Nc)
        obj_ec, constraints = self._create_ecm_problem(ln_conc)
        prob = cp.Problem(obj_ec, constraints)
        prob.solve()
        if prob.status == cp.OPTIMAL:
            return np.exp(prob.value), ln_conc.value
        elif prob.status == cp.OPTIMAL_INACCURATE:
            logging.warning("ECM solution is 'optimal_inaccurate'")
            return np.exp(prob.value), ln_conc.value
        else:
            raise Exception(prob.status)

    def _calc_z_scores(self, ln_conc: cp.Variable) -> Expression:
        """Calculate individual zscores."""
        return (ln_conc - self.ln_conc_mu) / (self.ln_conc_sigma + 1e-9)

    def _metabolic_adjustment(self, ln_conc: np.ndarray) -> float:
        """Calculate metabolic adjustment score.

        Essentially, it is the sum of Z-scores for the multivariate Gaussian
        distribution of log-concentrations (described by mu and sigma)
        """
        idx = self.ln_conc_sigma >= self.MINIMAL_STDEV
        return sum(cp.power(self._calc_z_scores(ln_conc)[idx], 2))

    def pareto(self, weights: Iterable[float] = None) -> pd.DataFrame:
        """Minimize enzyme cost versus metabolic adjustment (Pareto).

        enzyme cost is defined as in standard ECM.
        metabolic adjustment is the sum of squared Z-scores of the metabolite
        log-concentrations (relative to the prior Gaussian distribution).

        Arguments
        ---------
        weights : Iterable[float]
            the factor for the upper bounds on the ECM objective. Only
            non-negative values are allowed

        Returns
        -------
        results : DataFrame
            a summary table of the results of all optimization runs
        """
        ln_conc = cp.Variable(self.Nc)
        ln_enz_wgt = self._ln_total_enzyme_weight(ln_conc)
        ln_met_wgt = self._ln_total_metabolite_weight(ln_conc)
        constraints = [
            ln_conc >= self.ln_conc_lb,
            ln_conc <= self.ln_conc_ub,
            self._driving_forces(ln_conc) >= self.DRIVING_FORCE_LB,
        ]

        # the two Pareto objectives:
        ln_enz_cst = cp.log_sum_exp(cp.vstack([ln_enz_wgt, ln_met_wgt]))
        met_adj = self._metabolic_adjustment(ln_conc)

        # First find the minimum EC value
        prob = cp.Problem(cp.Minimize(ln_enz_cst), constraints)
        prob.solve()
        ln_min_ec = ln_enz_cst.value

        # scan the Pareto front
        data = []
        if weights is None:
            weights = np.linspace(0, 1, num=30)

        for w in weights:
            # place an upper bound on the ECM objective:
            # ECM < (min(ECM) * exp(w))
            # and the minimize the secondary objective (metabolic adjustment)
            prob = cp.Problem(
                cp.Minimize(met_adj),
                constraints + [ln_enz_cst <= ln_min_ec + w],
            )
            prob.solve()

            if prob.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
                raise Exception(prob.status)

            data += [
                (w, "obj", "enzyme_cost", None, np.exp(ln_enz_cst.value)),
                (w, "obj", "enzyme_weight", None, np.exp(ln_enz_wgt.value)),
                (w, "obj", "metabolite_weight", None, np.exp(ln_met_wgt.value)),
                (w, "obj", "metabolic_adjustment", None, met_adj.value),
            ]

            for j, x in enumerate(ln_conc.value):
                data.append((w, "primal", "log_conc", j, x))
            for j, z_score in enumerate(self._calc_z_scores(ln_conc).value):
                data.append((w, "z_score", "log_conc", j, z_score))
            for i, df in enumerate(self._driving_forces(ln_conc).value):
                data.append((w, "primal", "driving_force", i, df))
            for i, enzyme_conc in enumerate(self.ECF(ln_conc).value):
                data.append((w, "primal", "log_enzyme_conc", i, enzyme_conc))
            for i, eta in enumerate(self._ln_eta_thermodynamic(ln_conc).value):
                data.append((w, "eta", "thermodynamic", i, np.exp(eta)))
            for i, eta in enumerate(self._ln_eta_kinetic(ln_conc).value):
                data.append((w, "eta", "kinetic", i, np.exp(eta)))
            for i, eta in enumerate(self._ln_eta_allosteric(ln_conc).value):
                data.append((w, "eta", "allosteric", i, np.exp(eta)))

        return pd.DataFrame(
            data, columns=["weight", "var_type", "name", "index", "value"]
        )
