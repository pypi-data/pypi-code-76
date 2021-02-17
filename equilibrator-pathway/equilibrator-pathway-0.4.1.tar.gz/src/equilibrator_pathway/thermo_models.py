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
import logging
from typing import Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from cvxpy import Maximize, Minimize, Problem, Variable
from cvxpy.constraints.constraint import Constraint
from cvxpy.problems.objective import Objective
from equilibrator_api import Q_, ComponentContribution, R, Reaction, default_T
from equilibrator_cache import Compound

from . import Bounds
from .mdf_solution import PathwayMdfSolution
from .mdmc_solution import PathwayMdmcSolution
from .pathway import Pathway


class ThermodynamicModel(Pathway):
    """Container for doing pathway-level thermodynamic analysis."""

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
        super(ThermodynamicModel, self).__init__(
            reactions=reactions,
            fluxes=fluxes,
            comp_contrib=comp_contrib,
            standard_dg_primes=standard_dg_primes,
            dg_sigma=dg_sigma,
            bounds=bounds,
            config_dict=config_dict,
            compound_id_mapping=compound_id_mapping,
        )

    def _thermo_constraints(
        self,
        ln_conc: Variable,
        B: Variable,
    ) -> Tuple[Variable, List[Constraint], List[Constraint]]:
        """Create primal LP problem for Min-max Thermodynamic Driving Force.

        Returns
        -------
        the linear problem object, and the three types of variables as arrays.
        """

        _rt = (R * default_T).m_as("kJ/mol")
        dg_prime = (
            self.standard_dg_primes.m_as("kJ/mol")
            + _rt * self.S.T.values @ ln_conc
        )

        if self.dg_sigma is not None:
            # define the ΔG'0 covariance eigenvariables
            Nq = self.dg_sigma.shape[1]
            y = Variable(shape=Nq, name="covariance eigenvalues")
            y_constraints = [-self.stdev_factor <= y, y <= self.stdev_factor]
            dg_prime += self.dg_sigma.m_as("kJ/mol") @ y
        else:
            # even if the covariance is not provided, we still add
            # a placeholder variable named 'y' (to make the downstream code
            # simpler).
            y = Variable(shape=1, name="covariance eigenvalues")
            y_constraints = [y == 0]

        dg_constraints = []
        for i, direction in enumerate(np.diag(self.I_dir)):
            if direction != 0:
                dg_constraints += [direction * dg_prime[i] <= -B]
            else:
                dg_constraints += [direction * dg_prime[i] <= 1]  # placeholder

        return y, y_constraints, dg_constraints

    def _conc_constraints(
        self,
        ln_conc: Variable,
        constant_only: bool = False,
    ) -> Tuple[List[Constraint], List[Constraint]]:
        """Add lower and upper bounds for the log concentrations.

        Arguments
        ---------
        ln_conc : Variable
            the log-concentration variable, size should be (self.Nc, )
        constant_only : bool
            if True, only add bounds to the "constant" compounds, i.e. ones
            with 0 standard deviation
        """
        c_lbs = []
        c_ubs = []
        for j in range(self.Nc):
            if constant_only and self.ln_conc_sigma[j] > self.MINIMAL_STDEV:
                continue
            lb = (
                self.ln_conc_mu[j]
                - self.CONFIDENCE_INTERVAL * self.ln_conc_sigma[j]
            )
            ub = (
                self.ln_conc_mu[j]
                + self.CONFIDENCE_INTERVAL * self.ln_conc_sigma[j]
            )
            c_lbs += [ln_conc[j] >= lb]
            c_ubs += [ln_conc[j] <= ub]
        return c_lbs, c_ubs

    def mdf_analysis(self) -> PathwayMdfSolution:
        """Find the MDF (Max-min Driving Force).

        Returns
        -------
        a PathwayMDFData object with the results of MDF analysis.
        """
        # ln-concentration variables (where the units are in M before taking
        # the log)
        ln_conc = Variable(shape=self.Nc, name="log concentrations")
        c_lbs, c_ubs = self._conc_constraints(ln_conc)

        # the margin variable representing the MDF in units of kJ/mol
        B = Variable(shape=1, name="minimum driving force")
        y, y_constraints, dg_constraints = self._thermo_constraints(ln_conc, B)

        objective = Maximize(B)

        prob = Problem(
            objective, y_constraints + dg_constraints + c_lbs + c_ubs
        )
        prob.solve()
        if prob.status != "optimal":
            logging.warning("LP status %s", prob.status)
            raise Exception("Cannot solve MDF optimization problem")

        reaction_prices = np.array(
            [float(c.dual_value) for c in dg_constraints]
        ).round(5)
        compound_prices = np.array(
            [float(u.dual_value - l.dual_value) for l, u in zip(c_lbs, c_ubs)]
        ).round(5)

        return PathwayMdfSolution(
            self,
            score=prob.value,
            ln_conc=ln_conc.value,
            y=y.value,
            reaction_prices=reaction_prices,
            compound_prices=compound_prices,
        )

    def get_zscores(self, ln_conc: Iterable) -> Iterable:
        return map(
            lambda x: (x[0] - x[1]) / x[2] if x[2] > self.MINIMAL_STDEV else 0,
            zip(ln_conc, self.ln_conc_mu, self.ln_conc_sigma),
        )

    def _make_zscore_objective(self, ln_conc: Variable) -> Objective:
        """Set the Z-score as the new objective."""
        zscores = [z ** 2 for z in self.get_zscores(ln_conc)]
        return Minimize(sum(zscores))

    def mdmc_analysis(
        self,
        min_lb: float = 0.0,
        max_lb: Optional[float] = 10.0,
        n_steps: int = 100,
    ) -> PathwayMdmcSolution:
        """Find the MDMC (Maximum Driving-force and Metabolic Consistency.

        :return: a PathwayMdmcSolution object with the results of MDMC analysis.
        """
        # ln-concentration variables (where the units are in M before taking
        # the log)
        ln_conc = Variable(shape=self.Nc, name="log concentrations")
        c_lbs, c_ubs = self._conc_constraints(ln_conc, constant_only=True)

        # the margin variable representing the MDF in units of kJ/mol
        B = Variable(shape=1, name="minimum driving force")
        y, y_constraints, dg_constraints = self._thermo_constraints(ln_conc, B)

        objective = self._make_zscore_objective(ln_conc)

        # scan through a range of DF lower bounds to find all possible Pareto
        # optimal solutions to the bi-optimization problem (MDF and Z-score)
        data = []
        for lb in np.linspace(min_lb, max_lb, n_steps):
            prob = Problem(
                objective,
                y_constraints + dg_constraints + c_lbs + c_ubs + [B >= lb],
            )
            prob.solve(solver="OSQP")
            if prob.status != "optimal":
                logging.warning("LP status %s", prob.status)
                raise Exception("Cannot solve MDF optimization problem")

            data.append((lb, "primal", "obj", "mdmc", 0, prob.value))
            data += [
                (lb, "primal", "var", "log_conc", i, ln_conc.value[i])
                for i in range(self.Nc)
            ]
            if self.dg_sigma is not None:
                Nq = self.dg_sigma.shape[1]
                data += [
                    (
                        lb,
                        "primal",
                        "var",
                        "covariance_eigenvalue",
                        i,
                        y.value[i],
                    )
                    for i in range(Nq)
                ]
            data += [
                (
                    lb,
                    "shadow_price",
                    "cnstr",
                    "driving_force",
                    j,
                    float(dg_constraints[j].dual_value),
                )
                for j in range(self.Nr)
            ]
            zscores = self.get_zscores(ln_conc.value)
            for j, zscore in enumerate(zscores):
                data.append((lb, "zscore", "var", "log_conc", j, zscore))

        solution_df = pd.DataFrame(
            data=data,
            columns=[
                "df_lb",
                "value_type",
                "var_type",
                "var_name",
                "index",
                "value",
            ],
        )
        return PathwayMdmcSolution(self, solution_df)
