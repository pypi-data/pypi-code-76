#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!!! Smiti/Anna, I expect the complete unit will be more complex that what I
# laid out below, put your names before me if you contribute more, you can add
# your email address if wanted

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>
    Smiti Mittal
    Anna Kogler

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''

# %%

import math
from thermosteam import (Reaction as Rxn, ParallelReaction as ParallelRxn)
#!!! Change this to relative importing when compiled into qsdsan
from qsdsan import Equipment, SanUnit, WasteStream
# from .. import SanUnit, Equipment # relative importing

isinstance = isinstance

__all__ = ('Electrode', 'ElectroChemCell')

# =============================================================================
# Firstly construct the different equipment for the unit
# Below is an example for electrode
# =============================================================================

# Be sure to include documentation and examples
class Electrode(Equipment):
    '''
    Electrodes to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.
    
    Parameters
    ----------
    electrode_type : str
        Type of the electrode, can only be "anode" or "cathode".
    material: str
        Material of the electrode.
    unit_cost: float
        Unit cost of the electrode, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the electrode in m2.
    
    See Also
    --------
    :class:`ElectroChemCell`
    
    '''
    
    # Include all attributes (no properties) in addition to the ones in the
    # parent `Equipment` class
    # Using __slots__ can improve computational efficiency when the class does not
    # have many attributes
    __slots__ = ('_type', '_material', '_N', 'unit_cost', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 BM=1., lifetime=10000, lifetime_unit='hr',
                 electrode_type='anode', # note that I prefer not to use 'type' because it's a builtin function
                 material='graphite', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self, name, design_units, BM, lifetime, lifetime_unit)
        self.electrode_type = electrode_type
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Equipment` must have a `_design` and a `_cost` method
    def _design(self):
        linked_unit = self.linked_unit
        # Suppose the electrode number depends on the total mass flow rate (kg/hr)
        Q = linked_unit.F_mass_in
        N = self._N = math.ceil(Q/10)
        design = {
            f'Number of {self.electrode_type}': N,
            f'Material of {self.electrode_type}': self.material,
            f'Surface area of {self.electrode_type}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.electrode_type}': 'm2'}
        return design
        
    # All subclasses of `Equipment` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def electrode_type(self):
        '''[str] Type of the electrode, either "anode" or "cathode".'''
        return self._type
    @electrode_type.setter
    def electrode_type(self, i):
        if i.lower() in ('anode', 'cathode'):
            self._type = i
        else:
            raise ValueError(f'Electrode can only be "anode" or "cathode", not {i}.')
    
    @property
    def material(self):
        '''[str] Material of the electrode.'''
        return self._material
    @material.setter
    def material(self, i):
        material = i.lower()
        if material == 'graphite':
            # You can have some default unit cost based on the material,
            # I'm just making up numbers
            # But be careful that by doing this, you might overwriter users' input
            if not self.unit_cost:
                self.unit_cost = 50
        self._material = material
    
    
    # Note that here we don't have the `setter`, this means we prevent the user
    # from setting N - it is supposed to be calculated from the flow information.
    @property
    def N(self):
        return self._N


# %%

# =============================================================================
# Then we can construct the unit with the different equipment
# =============================================================================

#!!! Note `Electrode` and `ElectroChemCell` has not been include in `qsdsan` now,
# so to actual run the example below, first run this script, then change
# `qs.sanunits.Electrode` to `Electrode` and `qs.sanunits.ElectroChemCell` to `ElectroChemCell`

class ElectroChemCell(SanUnit):
    '''
    Electrochemical cell for nutrient recovery.
    
    This unit has the following equipment:
        - :class:`Electrode`
    
    Parameters
    ----------
    reflux_ratio : float
        Cell operating reflux ratio
    ammonia_recovery : float
        Recovery of ammonia during cell operation.
    kW : float
        Electricity consumption in kW.
    
    Examples
    --------
    >>> # Set components
    >>> import qsdsan as qs
    >>> kwargs = dict(particle_size='Soluble',
    ...               degradability='Undegradable',
    ...               organic=False)
    >>> H2O = qs.Component.from_chemical('H2O', phase='l', **kwargs)
    >>> NH3 = qs.Component.from_chemical('NH3', phase='g', **kwargs)
    >>> NH3.particle_size = 'Dissolved gas'
    >>> NH4OH = qs.Component.from_chemical('NH4OH', phase='l', **kwargs)
    >>> H2SO4 = qs.Component.from_chemical('H2SO4', phase='l', **kwargs)
    >>> AmmoniumSulfate = qs.Component.from_chemical('AmmoniumSulfate', phase='l',
    ...                                              **kwargs)
    >>> CleaningAgent = qs.Component('CleaningAgent', MW=1, phase='l', **kwargs)
    >>> cmps = qs.Components((H2O, NH3, NH4OH, H2SO4, AmmoniumSulfate, CleaningAgent))
    >>> # Assuming all has the same molar volume as water for demonstration purpose
    >>> for cmp in cmps:
    ...     cmp.copy_models_from(H2O, names=['V'])
    ...     cmp.default()
    >>> qs.set_thermo(cmps)
    >>> # Set waste streams
    >>> influent = qs.WasteStream('influent', H2O=1000, NH4OH=50)
    >>> sulfuric_acid = qs.WasteStream('sulfuric_acid', price=1)
    >>> cleaning_agent = qs.WasteStream('cleaning_agent', price=5)
    >>> # Set anode and cathode
    >>> anode = qs.sanunits.Electrode(name='anode', electrode_type='anode',
    ...                               material='graphite', surface_area=10)
    >>> anode
    <Electrode: anode>
    >>> cathode = qs.sanunits.Electrode(name='cathode', electrode_type='cathode',
    ...                                 material='carbon', surface_area=10, unit_cost=1)
    >>> cathode
    <Electrode: cathode>
    >>> # Set the unit
    >>> U1 = qs.sanunits.ElectroChemCell('U1', ins=(influent, '', sulfuric_acid, cleaning_agent),
    ...                                 outs=('recovered', 'reflux', 'fugative_NH3'),
    ...                                 equipments=(anode, cathode))
    >>> U1.ins[1] = U1.outs[1]
    >>> # Simulate and look at the results
    >>> U1.simulate()
    >>> U1.diagram()
    >>> U1.show()
    ElectroChemCell: U1
    ins...
    [0] influent
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): H2O    1e+06
                     NH4OH  5e+04
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
         TN         : 19424.5 mg/L
         TKN        : 19424.5 mg/L
    
    [1] reflux  from  ElectroChemCell-U1
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): H2O            1.03e+05
                     CleaningAgent  1.03
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
    
    [2] sulfuric_acid
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow: 0
    
        WasteStream-specific properties: None for empty WasteStreams
    [3] cleaning_agent
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): CleaningAgent  10.3
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
    
    outs...
    [0] recovered
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): H2O            9.23e+05
                     CleaningAgent  9.26
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
    
    [1] reflux  to  ElectroChemCell-U1
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): H2O            1.03e+05
                     CleaningAgent  1.03
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
    
    [2] fugative_NH3
        phase: 'l', T: 298.15 K, P: 101325 Pa
        flow (g/hr): NH3  2.43e+04
    
        WasteStream-specific properties:
         pH         : 7.0
         Alkalinity : 2.5 mg/L
    >>> U1.results()
    Electro chem cell                             Units        U1
    Power               Rate                         kW         1
                        Cost                     USD/hr    0.0782
    Design              Number of anode                       116
                        Material of anode                graphite
                        Surface area of anode        m2        10
                        Number of cathode                     116
                        Material of cathode                carbon
                        Surface area of cathode      m2        10
    Purchase cost       anode                       USD      11.6
                        cathode                     USD       116
    Total purchase cost                             USD       128
    Utility cost                                 USD/hr    0.0782
    Additional OPEX                              USD/hr         0
    '''

    def __init__(self, ID='', ins=None, outs=(),
                 equipments=(), reflux_ratio=0.1, ammonia_recovery=0.9, kW=1):
        if isinstance(equipments, Equipment):
            equipments = (equipments,)
        SanUnit.__init__(self, ID, ins, outs, equipments=equipments)
        self.reflux_ratio = reflux_ratio
        self.kW = kW
        self.recovery_rxn =  ParallelRxn([
    #   Reaction definition                         Reactant      Conversion
    Rxn('NH4OH -> NH3 + H2O',                        'NH4OH',         1),
    Rxn('2 NH3 + H2SO4 -> AmmoniumSulfate + 2 H2O',   'NH3',    ammonia_recovery)
    ])

    _N_ins = 4
    _N_outs = 3
    
    def _run(self):
        influent, recycled, acid, cleaner = self.ins
        recovered, reflux, fugative = self.outs
        
        mixture = WasteStream()
        # Stoichiometrically with 10% extra
        acid.imol['H2SO4'] = influent.imol['NH3']/2*1.1
        cleaner.empty()
        # Assuming 1 w/v% loading
        cleaner.imass['CleaningAgent'] = self.F_vol_in * 0.01

        mixture.mix_from(self.ins)
        self.recovery_rxn(mixture.mol)
        
        fugative.copy_flow(mixture, 'NH3', remove=True)
        reflux.mol = mixture.mol * self.reflux_ratio
        recovered.mass = mixture.mass - reflux.mass
        
    def _design(self):
        self.add_equipment_design()
        self.power_utility(self.kW)
    
    def _cost(self):
        self.add_equipment_cost()

    @property
    def ammonia_recovery(self):
        return self.recovery_rxn.X[1]
    @ammonia_recovery.setter
    def ammonia_recovery(self, i):
        self.recovery_rxn.X[1] = i








