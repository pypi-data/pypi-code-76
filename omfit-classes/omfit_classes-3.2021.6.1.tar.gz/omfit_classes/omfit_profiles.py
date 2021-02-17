try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

from omfit_classes.utils_math import *
from omfit_classes.omfit_data import OMFITncDataset, OMFITncDynamicDataset, importDataset
from omas import ODS, omas_environment, cocos_transform, define_cocos
from omfit_classes.omfit_omas_utils import add_generic_OMFIT_info_to_ods

import inspect
import numpy as np
from scipy import constants

__all__ = ['OMFITprofiles', 'OMFITprofilesDynamic']

model_tree_species = ['e', '2H1', '4He2', '6Li3', '10B5', '12C6', '14N7', '20Ne10']
# fmt: off
model_tree_quantities = ['angular_momentum', 'angular_momentum_density', 'angular_momentum_density_{species}', 'angular_momentum_{species}',
'dn_{species}_dpsi', 'dT_{species}_dpsi', 'ELM_phase', 'ELM_since_last', 'ELM_until_next', 'fpol', 'jboot_sauter', 'lnLambda',
'n_{species}', 'nclass_sigma', 'nu_star_{species}', 'nu_{species}', 'omega_gyro_{species}_midplane', 'omega_LX_{species}_midplane',
'omega_N_{species}', 'omega_NTV0_{species}', 'omega_P_{species}', 'omega_plasma_{species}', 'omega_RX_{species}_midplane',
'omega_T_{species}', 'omega_tor_{species}', 'omega_tor_{species}_KDG', 'P_brem', 'P_rad', 'P_rad_cNi', 'P_rad_cW', 'P_rad_nNi', 'P_rad_nW',
'P_rad_ZnNi', 'P_rad_ZnW', 'p_tot', 'p_{species}', 'pres', 'psi', 'psi_n', 'q', 'R_midplane', 'resistivity', 'rho', 'T_{species}', 'time',
'Total_Zeff', 'V_pol_{species}_KDG', 'Zavg_Ni', 'Zavg_W', 'Zeff']
# fmt: on

class OMFITprofiles(OMFITncDataset):
    def __init__(self, filename, data_vars=None, coords=None, attrs=None, comment=''):
        '''
        Data class used by OMFITprofiles, CAKE and other
        OMFIT modules for storing experimental profiles data

        :param filename: filename of the NetCDF file where data will be saved

        :param data_vars: see xarray.Dataset

        :param coords: see xarray.Dataset

        :param attrs: see xarray.Dataset

        :param comment: String that if set will show in the OMFIT tree GUI
        '''
        self.dynaLoad = False
        super().__init__(filename, data_vars=data_vars, coords=coords, attrs=attrs)
        self.OMFITproperties['comment'] = comment

    @property
    def comment(self):
        return self.OMFITproperties['comment']

    @comment.setter
    def comment(self, comment):
        self.OMFITproperties['comment'] = comment

    def __tree_repr__(self):
        if self.comment:
            return self.__class__.__name__ + ': ' + self.comment, []
        else:
            return super().__tree_repr__()

    def mZ(self, species):
        '''
        Parse subscript strings and return ion mass and charge

        :param species: subscript strings such as `e`, `12C6`, `2H1`, 'fast_2H1`, ...

        :return: m and Z
        '''
        species = str(species)
        if species == 'e':
            Z = -1
            m = constants.m_e
        else:
            m = int(re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\1', species))
            name = re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\2', species)
            Z = int(re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\3', species))
            m *= constants.m_u
        return m, Z

    def get_species(self):
        """
        Identify species and ions that have density information
        """
        species = []
        for key in list(self.data_vars.keys()):
            if key.count('_') != 1:
                continue
            s = re.sub('^[nT]_(.*)', r'\1', key)
            if s in ['e', 'b'] or re.match('[0-9]+[a-zA-Z]+[0-9]+', s):
                species.append(s)
        species = tolist(np.unique(species))
        ions = [s for s in species if s not in ['e']]
        ions_with_dens = [i for i in ions if 'n_' + i in self]
        return species, ions, ions_with_dens

    def to_omas(self, ods=None, times=None):
        '''
        :param ods: ODS to which data will be appended

        :return: ods
        '''

        if ods is None:
            ods = ODS()

        if 'device' in self.attrs:
            ods['dataset_description.data_entry.machine'] = self.attrs['device']
        if 'shot' in self.attrs:
            ods['dataset_description.data_entry.pulse'] = self.attrs['shot']

        # identify fitting coordinate
        for fit_coordinate in ['rho', 'psi_n', None]:
            if fit_coordinate in self.dims:
                break
        if fit_coordinate is None:
            raise ValueError("Fit coordinate should be 'rho' or 'psi_n'")

        # general info
        species, ions, ions_with_dens = self.get_species()
        nion = len(ions)
        times = self['time'].values

        # assign both core_profies and edge_profiles but with data from different spatial ranges
        for coredgestring in ['core_profiles', 'edge_profiles']:
            if coredgestring.startswith('core'):
                derived = self.where(self[fit_coordinate] <= 1.0, drop=True)
            else:
                derived = self.where(self[fit_coordinate] > 0.8, drop=True)

            coredge = ods[coredgestring]
            prop = coredge['ids_properties']
            prop['comment'] = 'Data from OMFITprofiles.to_omas()'
            prop['homogeneous_time'] = True

            coredge['time'] = times / 1e3

            for ti, time in enumerate(times):
                profs = coredge[f'profiles_1d.{ti}']
                profs['time'] = time / 1e3
                for q in derived.variables:
                    fit = derived[q]
                    if q in ['time']:
                        continue
                    if q == 'rho':
                        if fit_coordinate == 'rho':
                            profs['grid.rho_tor_norm'] = derived['rho'].values
                        else:
                            profs['grid.rho_tor_norm'] = fit.sel(time=time).values
                    elif q == 'psi_n':
                        if fit_coordinate == 'psi_n':
                            profs['grid.rho_pol_norm'] = derived['psi_n'].values
                        else:
                            profs['grid.rho_pol_norm'] = fit.sel(time=time).values
                    elif q == 'n_e':
                        profs['electrons.density_thermal'] = fit.sel(time=time).values
                    elif q == 'T_e':
                        profs['electrons.temperature'] = fit.sel(time=time).values
                    elif '_' in q and q.split('_', 1)[1] in ions:
                        continue

                # thermal ions
                for ni, ion in enumerate(ions[::-1]):
                    if ion == 'b':
                        continue
                    profi = profs[f'ion.{ni}']
                    profi['density_thermal'] = derived[f'n_{ion}'].sel(time=time).values
                    if f'T_{ion}' in derived:
                        profi['temperature'] = derived[f'T_{ion}'].sel(time=time).values
                    ion_details = list(atomic_element(symbol=ion).values())[0]
                    profi['label'] = ion_details['symbol']
                    profi['z_ion'] = float(ion_details['Z_ion'])
                    profi['multiple_states_flag'] = 0
                    profi['element[0].atoms_n'] = 1
                    profi['element[0].z_n'] = float(ion_details['Z'])
                    profi['element[0].a'] = float(ion_details['A'])
                    profi['multiple_states_flag'] = 0
                    if f'V_tor_{ion}' in derived and not (f'omega_tor_{ion}' in derived and 'R_midplane' in derived):
                        profi['velocity.toroidal'] = derived[f'V_tor_{ion}'].sel(time=time).values
                    elif f'omega_tor_{ion}' in derived and 'R_midplane' in derived:
                        profi['velocity.toroidal'] = (derived[f'omega_tor_{ion}'].sel(time=time) * derived['R_midplane'].sel(time=time)).values
                    if f'V_pol_{ion}' in derived:
                        profi['velocity.poloidal'] = derived[f'V_pol_{ion}'].sel(time=time).values

                # beam ions
                for ion in ions:
                    if ion != 'b':
                        continue
                    ni = len(profs['ion'])
                    for nii in profs['ion']:
                        profi = profs[f'ion.{ni}']
                        if profi['label'] == 'H':
                            ion = '2H1'
                            ni = nii
                            break
                    profi = profs[f'ion.{ni}']
                    profi['density_fast'] = derived[f'n_{ion}'].sel(time=time).values
                    pfast = derived[f'T_{ion}'].sel(time=time).values * constants.e * derived[f'n_{ion}'].sel(time=time).values
                    profi['pressure_fast_perpendicular'] = 2.0 / 3.0 * pfast
                    profi['pressure_fast_parallel'] = 1.0 / 3.0 * pfast
                    ion_details = list(atomic_element(symbol=ion).values())[0]
                    profi['label'] = ion_details['symbol']
                    profi['z_ion'] = float(ion_details['Z_ion'])
                    profi['multiple_states_flag'] = 0
                    profi['element[0].atoms_n'] = 1
                    profi['element[0].z_n'] = float(ion_details['Z'])
                    profi['element[0].a'] = float(ion_details['A'])
                    profi['multiple_states_flag'] = 0

                if 'Total_Zeff' in derived:
                    profs['zeff'] = derived['Total_Zeff'].sel(time=time).values
        return ods

    def model_tree_quantities(self):
        '''
        Returns list of MDS+ model_tree_quantities for all species.
        The function will warn if some of the `model_tree_quantities` are missing in OMFIT-source/omfit/omfit_classes/omfit_profiles.py
        and the model tree should be updated

        :return: list of strings
        '''
        new_model_tree_quantities = set(model_tree_quantities)
        for item in self.variables:
            match = False
            for s in model_tree_species:
                tmp = item.replace(f'_{s}', '_{species}')
                if tmp != item:
                    match = True
                    break
            if match:
                new_model_tree_quantities.add(tmp)
            else:
                new_model_tree_quantities.add(item)
        new_model_tree_quantities = sorted(list(new_model_tree_quantities),key=lambda x:x.lower())
        if new_model_tree_quantities != model_tree_quantities:
            import textwrap
            printe('WARNING!: Update model_tree_quantities in OMFIT-source/omfit/omfit_classes/omfit_profiles.py')
            printe('WARNING!: and update the OMFIT_PROFS MDS+ model tree')
            printe('-'*140)
            printe('# fmt: off')
            printe(textwrap.fill(f'model_tree_quantities = {repr(new_model_tree_quantities)}', width=140))
            printe('# fmt: on')
            printe('-'*140)

        quantities = []
        for item in new_model_tree_quantities:
            if '{' in item:
                for s in model_tree_species:
                    quantities.append(item.format(species=s))
            else:
                quantities.append(item)
        return quantities

    def create_model_tree(self, server, treename='OMFIT_PROFS'):
        '''
        Generate MDS+ model tree

        :param server: MDS+ server

        :param treename: MDS+ treename
        '''
        from omfit_classes.omfit_mds import OMFITmdsConnection
        conn = OMFITmdsConnection(server)

        quantities = {self.mds_translator(k): None for k in self.model_tree_quantities()}
        quantities['__content__'] = ''
        conn.create_model_tree(treename, '', quantities, clear_subtree=True)

    def to_mds(self, server, shot, treename='OMFIT_PROFS'):
        '''
        This script writes the OMFITproflies datase to DIII-D MDS+ and updates d3drdb accordingly

        :param server: MDS+ server

        :param shot: shot to store the data to

        :param treename: MDS+ treename

        :return: runid, treename
        '''
        from omfit_classes.omfit_mds import OMFITmdsConnection
        conn = OMFITmdsConnection(server)

        quantities = self.model_tree_quantities()

        # find next available runid in d3drdb for this shot
        from omfit_classes.omfit_rdb import OMFITrdb
        rdb = OMFITrdb(db='code_rundb', server='d3drdb', by_column=True)
        runs = rdb.select(f"select run_id from plasmas where shot={shot} and code_name='OMFITprofiles'", by_column=True)
        for run in range(1, 9999):
            runid = int('%06d%04d' % (shot, run))
            if not len(runs) or runid not in runs['run_id']:
                break
        print(f'Writing OMFITprofiles to MDS+ {runid}')

        # write to MDS+
        quantities = conn.write_dataset(treename=treename, shot=runid, subtree='', xarray_dataset=self, quantities=quantities, translator=lambda x:self.mds_translator(x))
        conn.write(treename=treename, shot=runid, node='__content__', data=';'.join(quantities))

        # add data to d3drdb (after MDS+ so that this is done only if MDS+ write is successful)
        data = {'code_name': 'OMFITprofiles',
                'shot': shot,
                'experiment': 'DIII-D',
                'run_type': 'user',
                'tree': treename,
                'start_time': np.min(self['time'].values),
                'stop_time': np.max(self['time'].values),
                'mdsserver': server,
                'run_id': runid}
        rdb.insert('plasmas', data, verbose=False)
        pprint(data)

        return runid, treename

    def mds_translator(self, inv=None):
        '''
        Converts strings OMFITprofiles dataset keys to MDS+ nodes less than 12 chars long

        :param inv: tring to which to apply the transformation
                    if `None` the transformation is applied to all of the OMFITprofiles.model_tree_quantities for sanity check

        :return: transformed sting or if inv is None the `mapped_model_2_mds` and `mapped_mds_2_model` dictionaries
        '''
        mapper = SortedDict()
        mapper['angular_momentum_density'] = 'mom_dens'
        mapper['angular_momentum'] = 'mom'
        mapper['midplane'] = 'mid'
        mapper['omega_gyro_'] = 'gyrof_'
        mapper['omega_'] = 'w_'
        mapper['2H1'] = 'D'
        mapper['4He2'] = 'He'
        mapper['6Li3'] = 'Li'
        mapper['10B5'] = 'B'
        mapper['12C6'] = 'C'
        mapper['14N7'] = 'N'
        mapper['20Ne10'] = 'Ne'
        mapper['since_last'] = '_last'
        mapper['until_next'] = '_next'

        if inv is not None:
            for match, sub in mapper.items():
                inv = inv.replace(match, sub)
            if len(inv) > 12:
                raise Exception(f'MDS+ OMFITprofiles quantity is longer than 12 chars: {inv}\nUpdate the mds_translator function accordingly')
            return inv
        else:
            model_tree_quantities = self.model_tree_quantities()
            mapped_model_2_mds = SortedDict()
            mapped_mds_2_model = SortedDict()
            for item0 in model_tree_quantities:
                item = item0
                for match, sub in mapper.items():
                    item = item.replace(match, sub)
                if len(item) > 12:
                    raise Exception(f'MDS+ string is longer than 12 chars: {item}')
                if item0 != item and item in model_tree_quantities:
                    raise Exception(f'MDS+ string shadows something else: {item}')
                if item in mapped_mds_2_model:
                    raise Exception(f'Multiple items map to the same quantity: {item0} {mapped_mds_2_model[item]}')
                mapped_model_2_mds[item0] = item
                mapped_mds_2_model[item] = item0
            return mapped_model_2_mds, mapped_mds_2_model

class OMFITprofilesDynamic(OMFITncDynamicDataset):
    """
    Class for dynamic calculation of derived quantities

    :Examples:

    Initialize the class with a filename and FIT Dataset.
    >> tmp=OMFITprofiles('test.nc', fits=root['OUTPUTS']['FIT'], equilibrium=root['OUTPUTS']['SLICE']['EQ'], root['SETTINGS']['EXPERIMENT']['gas'])

    Accessing a quantity will dynamically calculate it.
    >> print tmp['Zeff']

    Quantities are then stored (they are not calculated twice).
    >> tmp=OMFITprofiles('test.nc',
                          fits=root['OUTPUTS']['FIT'],
                          equilibrium=root['OUTPUTS']['SLICE']['EQ'],
                          main_ion='2H1')
    >> uband(tmp['rho'],tmp['n_2H1'])
    """

    def __init__(self, filename, fits=None, equilibrium=None, main_ion='2H1', **kw):

        OMFITncDataset.__init__(self, filename, **kw)

        if fits:
            self.update(fits)

            # profile fit dimension
            dims = list(self.dims.keys())
            xkey = dims[dims.index('time') - 1]

            # collect some meta data about which particle species have what info available
            self.attrs['main_ion'] = str(main_ion)
            species, ions, ions_with_dens = self.get_species()
            self['species'] = DataArray(species, dims=['species'])
            ions += [self.attrs['main_ion']]
            self['ions'] = DataArray(ions, dims=['ions'])
            ions_with_dens += [self.attrs['main_ion']]
            self['ions_with_dens'] = DataArray(ions_with_dens, dims=['ions_with_dens'])
            ions_with_rot = [key.replace('omega_tor_', '') for key in self if key.startswith('omega_tor') and key != 'omega_tor_e']
            self['ions_with_rot'] = DataArray(ions_with_rot, dims=['ions_with_rot'])

            # interpolate other radial coordinates from equilibrium
            printd('- Interpolating equilibrium quantities')
            needed = {
                'avg_R',
                'avg_R**2',
                'avg_1/R',
                'avg_1/R**2',
                'avg_Btot',
                'avg_Btot**2',
                'avg_vp',
                'avg_q',
                'avg_fc',
                'avg_F',
                'avg_P',
                'geo_psi',
                'geo_R',
                'geo_Z',
                'geo_a',
                'geo_eps',
                'geo_vol',
            }
            eqcoords = needed.intersection(list(equilibrium.keys()))
            for meas in eqcoords:
                if 'profile_' + xkey != meas and 'profile_psi_n' in equilibrium[meas]:
                    yy = []
                    for t in self['time'].values:
                        eq_t = equilibrium.sel(time=t, method='nearest')
                        x = np.squeeze(eq_t['profile_' + xkey])
                        y = np.squeeze(nominal_values(eq_t[meas].values))
                        yy.append(interp1e(x, y)(self[xkey].values))

                        # Ensure that 'q' is not extrapolated outside the separatrix
                        if meas == 'profile_q':
                            mask = self[xkey].values > 1.0
                            yy[-1][mask] = np.nan
                    yy = np.array(yy)
                    key = meas.replace('profile_', '')
                    self[key] = DataArray(
                        yy, coords=[fits['time'], fits[xkey]], dims=['time', xkey], attrs=copy.deepcopy(equilibrium[meas].attrs)
                    )
            self.set_coords(eqcoords)
            # reassign global attrs clobbered when assigning eq DataArrays with attrs
            self.attrs['main_ion'] = str(main_ion)
            self.save()

        self.update_dynamic_keys(self.__class__)

    def __getitem__(self, key):
        # map specific quantities to class functions
        mapper = {}
        mapper['n_' + self.attrs['main_ion']] = 'calc_n_main_ion'
        mapper['T_' + self.attrs['main_ion']] = 'calc_T_main_ion'

        # resolve mappings
        if key not in self:
            if key in mapper:
                getattr(self, mapper[key])()
                if mapper[key] in self._dynamic_keys:
                    self._dynamic_keys.pop(self._dynamic_keys.index(mapper[key]))

        # return value
        return OMFITncDynamicDataset.__getitem__(self, key)

    def mZ(self, species):
        '''
        Parse subscript strings and return ion mass and charge

        :param species: subscript strings such as `e`, `12C6`, `2H1`, 'fast_2H1`, ...

        :return: m and Z
        '''
        species = str(species).replace('fast_', '')
        if species == 'e':
            Z = -1
            m = constants.m_e
        else:
            m = int(re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\1', species))
            name = re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\2', species)
            Z = int(re.sub('([0-9]+)([a-zA-Z]+)([0-9]+)', r'\3', species))
            m *= constants.m_u
        return m, Z

    def get_species(self):
        """
        Identify species and ions that have density information
        """
        species = []
        for key in list(self.data_vars.keys()):
            if key.count('_') != 1:
                continue
            s = re.sub('^[nT]_(.*)', r'\1', key)
            if s in ['e', 'b'] or re.match('[0-9]+[a-zA-Z]+[0-9]+', s):
                species.append(s)
        species = tolist(np.unique(species))
        ions = [s for s in species if s not in ['e']]
        ions_with_dens = [i for i in ions if 'n_' + i in self]
        return species, ions, ions_with_dens

    def calc_n_main_ion(self):
        """
        Density of the main ion species.
        Assumes quasi-neutrality.

        :return: None. Updates the instance's Dataset in place.

        """
        main_ion = str(self.attrs['main_ion'])
        mg, zg = self.mZ(main_ion)
        nz = self['n_e']
        for key in self['ions_with_dens'].values:
            if key != main_ion:
                nz -= self['n_' + key].values * self.mZ(key)[1]
        self['n_' + main_ion] = nz / zg
        invalid = np.where(self['n_' + main_ion].values <= 0)[0]
        if len(invalid) > 0:
            printe('  Had to force main ion density to be always positive!')
            printe('  This will likely present a problem when running transport codes!')
            valid = np.where(self['n_' + main_ion].values > 0)[0]
            self['n_' + main_ion].values[invalid] = np.nanmin(self['n_' + main_ion].values[valid])

    def calc_T_main_ion(self):
        """
        Temperature of the main ion species.
        Assumes it is equal to the measured ion species temperature.
        If there are multiple impurity temperatures measured, it uses the first one.

        :return: None. Updates the instance's Dataset in place.

        """
        main_ion = str(self.attrs['main_ion'])
        impurities_with_temp = [k for k in self['ions'].values if k != 'b' and 'T_' + k in list(self.keys())]
        nwith = len(impurities_with_temp)
        if nwith == 0:
            raise OMFITexception("No main or impurity ion temperatures measured")
        if nwith > 1:
            printw(
                "WARNING: Multiple impurities temperatures measured, setting main ion temperature based on {:}".format(
                    impurities_with_temp[0]
                )
            )
        for ion in impurities_with_temp:
            self['T_' + main_ion] = self[f'T_{ion}'] * 1
            break

    def calc_Zeff(self):
        r"""
        Effective charge of plasma.

        Formula: Z_{eff} = \sum{n_s Z_s^2} / \sum{n_s Z_s}

        :return: None. Updates the instance's Dataset in place.

        """
        # calculate Zeff (not assuming quasi-neutrality)
        nz_sum = np.sum([self['n_' + i].values * self.mZ(i)[1] for i in self['ions_with_dens'].values], axis=0)
        nz2_sum = np.sum([self['n_' + i].values * self.mZ(i)[1] ** 2 for i in self['ions_with_dens'].values], axis=0)
        z_eff = nz2_sum / nz_sum + 0 * self['n_e'].rename('Zeff')
        z_eff.attrs['long_name'] = r'$Z_{eff}$'
        self['Zeff'] = z_eff

    def calc_Total_Zeff(self):
        r"""
        Effective charge of plasma.

        Formula: Z_{eff} = \sum{n_s Z_s^2} / \sum{n_s Z_s}

        :return: None. Updates the instance's Dataset in place.

        """
        main_ion = str(self.attrs['main_ion'])
        mg, zg = self.mZ(main_ion)
        nz = self['n_e']
        for key in self['ions_with_dens'].values:
            if key != main_ion:
                nz -= self['n_' + key].values * self.mZ(key)[1]
        self['n_' + main_ion] = nz / zg
        invalid = np.where(self['n_' + main_ion].values <= 0)[0]
        if len(invalid) > 0:
            printe('  Had to force main ion density to be always positive!')
            printe('  This will likely present a problem when running transport codes!')
            valid = np.where(self['n_' + main_ion].values > 0)[0]
            self['n_' + main_ion].values[invalid] = np.nanmin(self['n_' + main_ion].values[valid])


if __name__ == '__main__':

    # ensure that all specified model_tree_quantities can be translated to have <=12 chars
    for s in model_tree_species:
        for q in model_tree_quantities:
            item0 = q.format(species=s)
            item = OMFITprofiles.mds_translator(None, item0)
