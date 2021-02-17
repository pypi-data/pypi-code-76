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
from scipy.integrate import ode

from .cost_function import EnzymeCostFunction


class EnzymeCostSimulator(object):
    def __init__(self, ecf: EnzymeCostFunction) -> None:
        self.ecf = ecf

        self.idx_fixed = np.where(
            self.ecf.ln_conc_sigma <= self.ecf.MINIMAL_STDEV
        )[0].tolist()

        self.idx_non_fixed = np.where(
            self.ecf.ln_conc_sigma > self.ecf.MINIMAL_STDEV
        )[0].tolist()

        self.E = np.ones(self.ecf.Nr)

    def set_enzyme_concentrations(self, E: np.ndarray) -> None:
        assert E.shape == (self.ecf.Nr,)
        self.E = E

    def _derivaties(self, t, y):
        # we only care about the time derivatives of the internal
        # metabolites (i.e. the first and last one are assumed to be
        # fixed in time)
        ln_conc = np.log(np.array(y))
        v = self.ecf.get_fluxes(ln_conc, self.E)
        dy = self.ecf.S @ v
        dy[self.idx_fixed] = 0
        return dy

    def Simulate(
        self,
        lnC0: np.ndarray,
        t_max: float = 1000.0,
        dt: float = 1.0,
        eps: float = 1e-9,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find the steady-state solution for the metabolite concentrations
        given the enzyme abundances

        Arguments:
            E    - enzyme abundances [gr]
            y0   - initial concentration of internal metabolites
                   (default: MDF solution)
            eps  - the minimal change under which the simulation will stop

        Returns:
            v    - the steady state flux
            y    - the steady state internal metabolite concentrations
        """
        assert lnC0.shape == (self.ecf.Nc,)

        if not self.ecf.is_feasible(lnC0):
            raise ValueError(
                "initial concentrations are not thermodynamically feasible"
            )

        v = self.ecf.get_fluxes(lnC0, self.E)

        T = np.array([0])
        Y = np.exp(lnC0)
        V = v.T

        r = ode(self._derivaties)
        r.set_initial_value(Y.T, 0)

        while r.successful():
            r.integrate(r.t + dt)
            v = self.ecf.get_fluxes(np.log(r.y.squeeze()), self.E)

            T = np.hstack([T, r.t])
            Y = np.vstack([Y, r.y.T])
            V = np.vstack([V, v.T])

            if r.t >= t_max:
                break

            abs_dy = np.abs(self.ecf.S[self.idx_non_fixed, :] @ v)
            print(f"t = {r.t:.2e}, dy = {abs_dy[0]:.2e}")
            if r.t >= 0.05 * t_max:
                if (abs_dy > eps).any():
                    break

        if r.t >= t_max:
            v_inf = np.nan
            lnC_inf = np.nan
        else:
            v_inf = V[-1, 0]
            lnC_inf = np.log(Y[-1, :])

        return v_inf, lnC_inf
