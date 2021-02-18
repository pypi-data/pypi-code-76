#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"

"""High-level interface to run impedance computations."""

import warnings

import numpy as np

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.frequential import FrequentialSolver


class ImpedanceComputation:
    """ Compute the input impedance of a geometry at the frequencies specified.
    Different options can be indicated.

    Parameters
    ----------
    fs : numpy.array
        Frequencies at which to compute the impedance.
    files : text files
        Geometry of the instrument. For more information on the file
        structures.
        See also : openwind.technical.InstrumentGeometry
    temperature : float or callable, optional
        Temperature along the instrument in Celsius degree. Default {25}
        See also : opewind.continuous.InstrumentPhysics
    losses : bool or {'bessel', 'wl','keefe','diffrepr', 'diffrepr+'}, optional
        Whether/how to take into account viscothermal losses. Default is True.
        If 'diffrepr+', use diffusive representation with explicit
        additional variables.
        See also : openwind.continuous.losses_model
    compute_method : {'FEM', 'TMM'}, optional
        Method chose to compute the frequency response. 'FEM' = finite elements
        method; 'TMM' = transfer matrix method. Default {'FEM'}
        See also : openwind.frequential.FrequentialSolver, \
                  openwind.frequential.FrequentialTMM
    l_ele, order : list, optional, only used for FEM
        Elements lengths and orders. Default: {None}, automatic meshing.
        See also : openwind.discretization.Mesh
    nb_sub: integer, optional, only used for TMM
        Number of subdivisions. Default: {1}
        See also : openwind.frequential.FrequentialTMM
    convention: {'PH1', 'VH1'}, optional, only used for FEM
        Convention chooses whether P (pressure) or V (flow) is the H1 variable.
        Default is {'PH1'}.
        See also : openwind.continuous.InstrumentPhysics
    nondim : bool, optional
        Nondimensionalization mode. If activated, the physical parameters
        are nondimensionalized so that they are closer to 1. Default {False}.
        See also: openwind.continuous.InstrumentPhysics
    radiation_category : {'unflanged', 'infinite_flanged', ...}, optional
        Type of the radiation.
        See also: openwind.continuous.InstrumentPhysics
    discontinuity_mass : Boolean, optional
        If true, acoustic mass is included in the junction between two
        pipes with different cross section. The default is True.
    matching_volume : boolean, optional
        Include or not the matching volume between the main and the side
        tubes in the masses of the T-joint junctions. The default is False.

    """
    FMIN_disc = 2000.0 # provides a mesh adapted to at least FMIN_disc Hz

    def __init__(self, frequencies, *files, player = None, temperature=None, losses=True,
                  compute_method='FEM', l_ele=None, order=None, nb_sub=1, note=None,
                  convention='PH1', nondim=True, radiation_category='unflanged',
                  spherical_waves=False, discontinuity_mass=True,
                  matching_volume=False):

        self.frequencies = frequencies
        if not player:
            player = Player()
        if not temperature:
            temperature=25
            warnings.warn('The default temperature is 25 degrees Celsius.')

        if losses == 'diffrepr+':
            # Use Diffusive Representation with additional variables
            losses = 'diffrepr'
            diff_repr_vars = True
        else:
            diff_repr_vars = False

        self.__instrument_geometry = InstrumentGeometry(*files)
        self.__instru_physics = InstrumentPhysics(self.__instrument_geometry, temperature, player=player,
                                      losses=losses,
                                      radiation_category=radiation_category,
                                      nondim=nondim, convention=convention,
                                      spherical_waves=spherical_waves,
                                      discontinuity_mass=discontinuity_mass,
                                      matching_volume=matching_volume)

        FMAX = np.max([np.max(frequencies), ImpedanceComputation.FMIN_disc])
        shortest_lambda = 346.3 / FMAX

        kwargs = {'diffus_repr_var':diff_repr_vars,
                  'l_ele':l_ele,
                  'order':order,
                  'shortestLbd':shortest_lambda,
                  'note':note,
                  'nb_sub':nb_sub}

        self.__freq_model = FrequentialSolver(self.__instru_physics, frequencies,
                                           compute_method=compute_method,
                                           **kwargs)
        self.__freq_model.solve()

        # Small hack : give visibility to ALL the attributes of __freq_model
        # self.__dict__.update(self.__freq_model.__dict__)

        self.impedance = self.__freq_model.imped # /freq_model.get_ZC_adim()
        self.Zc = self.__freq_model.get_ZC_adim()

    def __repr__(self):
        return ("<openwind.ImpedanceComputation("
                "\n{},".format(repr(self.__instru_physics)) +
                "\n{},".format(repr(self.__freq_model)) +
                "\n)>")

    def __str__(self):
        return ("{}\n\n" + 30*'*' + "\n\n{}").format(self.__instru_physics,
                                                     self.__freq_model)

    def set_note(self, note):
        self.__freq_model.set_note(note)
        self.__freq_model.solve()
        self.impedance = self.__freq_model.imped

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies
        self.__freq_model.set_frequencies(frequencies)
        self.__freq_model.solve()
        self.impedance = self.__freq_model.imped

    def plot_instrument(self, figure=None, **kwargs):
        self.__instrument_geometry.plot_InstrumentGeometry(figure=figure, **kwargs)

    def plot_impedance(self, **kwargs):
        """Plot the impedance of the instrument."""
        self.__freq_model.plot_impedance(**kwargs)

    def write_impedance(self, filename):
        self.__freq_model.write_impedance(filename)

    def resonance_frequencies(self, k=5):
        return self.__freq_model.resonance_frequencies(k)

    def antiresonance_frequencies(self, k=5):
        return self.__freq_model.antiresonance_frequencies(k)

    def discretization_infos(self):
        self.__freq_model.discretization_infos()

    def instrument_infos(self):
        print(self.__instrument_geometry)
        self.__instru_physics.player.display()

    def get_bore(self):
        return self.__instrument_geometry

    def get_all_notes(self):
        """
        Return all the notes specified in the fingering chart

        Returns
        -------
        list[string]
            The list of the notes names
        """
        return self.__instrument_geometry.fingering_chart.all_notes()

    def get_nb_dof(self):
        return self.__freq_model.n_tot
