#!/usr/bin/env python
# coding: utf-8
# get_ipython().run_line_magic('matplotlib', 'notebook')

import sys
try:
    import pysoleno.pysoleno as pysol
except:
    get_ipython().system('{sys.executable} -m pip install --user pysoleno')

import os
import copy
import numpy as np
import yaml
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist
import pysoleno.pysoleno as pysol

class Coil():
    def __init__(self, name):
        self.name = name
        self.input_folder = os.path.join(os.getcwd(), "Inputs")
        # if output_folder == "":
            # self.output_folder = os.path.join(os.path.join(os.getcwd(), "Outputs"), self.name)
        # else:
        self.output_folder = os.path.join(os.getcwd(), "LEDET")
        self.coil = self.read_yaml('coil', self.name)['coil']
        quench_scenario = "S.1"
        self.quench = self.read_yaml('quench', quench_scenario)['quench']
        self.wire = self.read_yaml('wire', self.coil['wire'])['wire']
        self.s = pysol.PySoleno()
        self.Nloop = 6

        ind_Mat_csv = f"{self.name}_selfMutualInductanceMatrix.csv"
        Ind_Mat_folder = os.path.join(os.path.join(self.output_folder, self.name), "Input")
        if not os.path.exists(Ind_Mat_folder):
            os.makedirs(Ind_Mat_folder)
        self.Ind_Mat = os.path.join(Ind_Mat_folder, ind_Mat_csv)

        B_field_map2d = f"{self.name}_All_NoIron_NoSelfField.map2d"
        map2d_folder = os.path.join(os.path.join(self.output_folder, 'Field maps'), self.name)
        if not os.path.exists(map2d_folder):
            os.makedirs(map2d_folder)
        self.map2d = os.path.join(map2d_folder, B_field_map2d)


    def read_yaml(self, type, name):
        """
        Reads yaml file and returns it as dictionary
        :param type: type of file, e.g.: quench, coil, wire
        :param name: file name, e.g. ColSol.1
        :return: dictionary for file named: type.name.yam
        """
        with open(os.path.join(self.input_folder, f"{type}.{name}.yaml"), 'r') as stream:
            data = yaml.safe_load(stream)
        return data

    def n_layers(self):
        """
        Number of layers in a coil
        """
        return int(np.fix((self.coil['A2'] - self.coil['A1'])/self.wire['sh_i']))


    def n_turns_per_layer(self):
        """
        Number of turns per layers in a coil
        """
        return int(np.fix((self.coil['B2'] - self.coil['B1']) / self.wire['sw_i']))


    def n_turs(self):
        """
        Number of turns in a coil
        """
        return self.n_turns_per_layer() * self.n_layers()


    def turn_pos(self):
        """
        Positions of centres of turns as a grid
        """
        f_layer_m_t_r = self.coil['A1'] + self.wire['sh_i'] / 2                                     # first layer middle turn radial position
        l_layer_m_t_r = f_layer_m_t_r + (self.n_layers()-1) * self.wire['sh_i']                     # last layer middle turn radial position
        r_pos = np.linspace(f_layer_m_t_r, l_layer_m_t_r, self.n_layers(), endpoint=True)           # layers middle turns radial positions
        f_layer_m_t_z = self.coil['B1'] + self.wire['sw_i'] / 2                                     # first layer middle turn axial position
        l_layer_m_t_z = f_layer_m_t_z + (self.n_turns_per_layer()-1) * self.wire['sw_i']            # last layer middle turn axial position
        z_pos = np.linspace(f_layer_m_t_z, l_layer_m_t_z, self.n_turns_per_layer(), endpoint=True)  # layers middle turns axial positions
        rr_pos, zz_pos = np.meshgrid(r_pos, z_pos)
        return rr_pos, zz_pos

    def coil_set(self):
        """
        Returns coils parameters as a tuple in pysoleno input format. All are SI units.
        """
        f_layer_s_t_r = self.coil['A1']                                                         # first layer start turn radial position
        l_layer_e_t_r = self.coil['A1'] + (self.n_layers()-1) * self.wire['sh_i']               # last layer end turn radial position
        Rin = np.linspace(f_layer_s_t_r, l_layer_e_t_r, self.n_layers(), endpoint=True)         # layers start turns radial positions
        Rout = Rin + self.wire['sh_i']                                                          # layers end turns radial positions
        Zlow = np.ones_like(Rin) * self.coil['B1']                                              # layers start axial positions
        Zhigh= np.ones_like(Rin) * self.coil['B2']                                              # layers end axial positions
        I = np.ones_like(Rin) * self.coil['I']                                                  # layers current
        Nturns = np.ones_like(Rin, dtype=np.int32) * self.n_turns_per_layer()                   # layers number of turns
        Nloop = np.ones_like(Rin, dtype=np.int32) * self.Nloop                                  # leyers number of iteration loops in soleno calculations
        return Rin, Rout, Zlow, Zhigh, I, Nturns, Nloop

    def calc_L_tot(self):
        """
        Total self inductance of a coil in H
        """
        return self.s.calcM([self.coil['A1']], [self.coil['A2']], [self.coil['B1']], [self.coil['B2']], [self.coil['I']], [self.n_turs()], [self.Nloop])[0][0]

    def calc_L_M(self):
        """
        Calculates mutual inductance matrix in a standard format in H
        """
        return self.s.calcM(*self.coil_set())

    def calc_Br_Bz(self):
        """
        Returns positions of turns centres and radial and axial field components in T
        """
        rr_pos, zz_pos = self.turn_pos()
        Br, Bz = self.s.calcB(rr_pos, zz_pos, *self.coil_set())
        return rr_pos, zz_pos, Br, Bz

    def save_L_M(self):
        """
        Saves mutula inductance matrix as to csv in LEDET format.
        """
        with open(self.Ind_Mat, 'w') as fp:
            fp.write("Extended self mutual inductance matrix [H/m]\n")
            np.savetxt(fp, self.calc_L_M(), '%6.16e', ',')

    def save_Bmod(self):
        """
        Saves coil field map in LEDET format (i.e. as ROXIE format)
        """
        block = np.repeat(np.arange(1, self.n_layers() + 1, dtype=np.int32), self.n_turns_per_layer())
        conductor = np.arange(1, self.n_turs() + 1, dtype=np.int32)
        number = np.arange(1, self.n_turs() + 1, dtype=np.int32)
        rr_pos, zz_pos, Br, Bz = self.calc_Br_Bz()
        area = np.zeros_like(number)
        current = np.ones_like(number) * self.coil['I']
        fill_fac = np.zeros_like(number)
        output = np.array([block, conductor, number, rr_pos.flatten('F')*1000, zz_pos.flatten('F')*1000, Br.flatten('F'), Bz.flatten('F'), area, current, fill_fac]).T

        with open(self.map2d, 'w') as fp:
            #fp.write(','.join(ar.dtype.names) + '\n')
            fp.write("BL. COND. NO. R-POS/MM Z-POS/MM BR/T BZ/T AREA/MM**2 CURRENT FILL FAC.  \n\n")
            np.savetxt(fp, output, '%d %d %d %6.5f %6.5f %6.5f %6.5f %6.5f %6.5f %6.5f', ',')

    def print_summary(self):
        """
        Prints main parameters of a coil
        """
        print(f"Coil name = {self.name}")
        print(f"Layers = {self.n_layers()}")
        print(f"Turns per layer = {self.n_turns_per_layer()}")
        print(f"Turns = {self.n_turs()}")
        L = self.calc_L_tot()
        E = 0.5 * L * self.coil['I']**2
        print(f"L = {L:.3f} H")
        print(f"E = {1e-3*E:.3f} kJ")

    def save_files(self):
        """
        Saves mutual inductance and field map for LEDET. This goes into specific folders.
        """
        self.save_L_M()
        self.save_Bmod()
        print("Soleno files written")

class NB_LEDET():
    def __init__(self,  nameMagnet, model_no, LEDET_folder="", rewsol=True):
        self.nameMagnet = nameMagnet
        self.model_no = model_no
        if LEDET_folder == "":
            self.LEDET_folder = os.getcwd()
        else:
            self.LEDET_folder = LEDET_folder
        nameFileLEDET = self.nameMagnet + f'_{int(model_no)}' + '.xlsx'
        self.excel_file_path = os.path.join(
            os.path.join(os.path.join(os.path.join(self.LEDET_folder, 'LEDET'), self.nameMagnet), "Input"),
            nameFileLEDET)
        self.c = Coil(self.nameMagnet)
        if rewsol:
            self.c.save_files()
        quench_file = "S.1"
        self.q = self.c.read_yaml("quench", quench_file)
        self.T00 = self.c.coil['T']  # [K]
        self.I00 = self.c.coil['I']  # [A]      # why this is not the same as for field maps
        self.nGroupsDefined = self.c.n_layers()  # number of layers
        self.nT = self.nGroupsDefined * [self.c.n_turns_per_layer()]  # Number of half-turns in each group

        self.selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}  # Define style for plots
        self.verbose = False  # If this variable is set to True, many comments will be displayed
        self.l_magnet = 1  # [m] THIS MUST REMAIN =1 for solenoid
        self.max_distance = 1.5E-3  # Prepare input for the function close_pairs_ckdtree

        # Total magnet self-inductance [H]
        self.M_m = np.array([[self.c.calc_L_tot()]])
        if self.c.wire['type'] == 'rect':
            wire_area = ((self.c.wire['sw_i'] - 2 * self.c.wire['si_w']) * (
                        self.c.wire['sh_i'] - 2 * self.c.wire['si_h'])) - ((4 - np.pi) * self.c.wire['scr_i'] ** 2)
            self.ds_inGroup = self.nGroupsDefined * [np.sqrt(
                wire_area * 4 / np.pi)]  # equivalent diameter, d_s = sqrt(4/pi*w_bare*h_bare), without correcting for the corner radius

        self.f_SC_strand_inGroup = self.nGroupsDefined * [1 / (1 + 4.0)]  # fraction of superconductor in the strands

        self.f_ro_eff_inGroup = self.nGroupsDefined * [1]  # Effective transverse resistivity parameter (default=1)

        self.Lp_f_inGroup = self.nGroupsDefined * [self.c.wire['stp']]  # Filament twist-pitch [m]# guess value

        self.RRR_Cu_inGroup = self.nGroupsDefined * [self.c.wire[
                                                         'RRR'] / 1.086]  # RRR of the conductor in each group of cables# 1.086 factor applied to RRR to correct for the fact that the NIST fit considers RRR measured between 273 K (not room temperature) and cryogenic temperature
        self.SCtype_inGroup = self.nGroupsDefined * [
            1]  # type of superconductor (1=Nb-Ti, 2=Nb3Sn(Summer's fit), 3=BSCCO2212, 4=Nb3Sn(Bordini's fit))
        self.STtype_inGroup = self.nGroupsDefined * [1]  # type of stabilizer (1=Cu, 2=Ag)
        self.insulationType_inGroup = self.nGroupsDefined * [2]  # Type of cable insulation (1=G10, 2=kapton)
        self.internalVoidsType_inGroup = self.nGroupsDefined * [
            2]  # Type of filler of voids between adjacent strands (1=G10, 2=kapton, 3=helium, 4=void)# if corner radius modification is introduced, void fraction will become >0
        self.externalVoidsType_inGroup = self.nGroupsDefined * [
            2]  # Type of filler of voids between strands and insulation layers (1=G10, 2=kapton, 3=helium, 4=void)
        self.wBare_inGroup = self.nGroupsDefined * [1.01E-3]  # bare cable width [m] RADIAL direction
        self.hBare_inGroup = self.nGroupsDefined * [1.61E-3]  # bare average cable height [m] AXIAL direction
        self.wIns_inGroup = self.nGroupsDefined * [20E-6]  # insulation thickness in the width direction [m]
        self.hIns_inGroup = self.nGroupsDefined * [20E-6]  # insulation thickness in the height direction [m]
        self.Lp_s_inGroup = self.nGroupsDefined * [100E-3]  # Strand twist-pitch [m] THIS WILL BE IGNORED
        self.R_c_inGroup = self.nGroupsDefined * [100E-6]  # Cross-contact resistance [Ohm] THIS WILL BE IGNORED
        self.Tc0_NbTi_ht_inGroup = self.nGroupsDefined * [9.2]  # Tc0_NbTi_ht_inGroup [K]
        self.Bc2_NbTi_ht_inGroup = self.nGroupsDefined * [14.5]  # Bc2_NbTi_ht_inGroup [T]
        self.c1_Ic_NbTi_inGroup = self.nGroupsDefined * [3336.363785]  # c1_Ic_NbTi_inGroup [A] TODO
        self.c2_Ic_NbTi_inGroup = self.nGroupsDefined * [-248.917389]  # c2_Ic_NbTi_inGroup [A/T] TODO
        self.Tc0_Nb3Sn_inGroup = self.nGroupsDefined * [0]  # Tc0_Nb3Sn [K]
        self.Bc2_Nb3Sn_inGroup = self.nGroupsDefined * [0]  # Bc2_Nb3Sn [T]
        self.Jc_Nb3Sn0_inGroup = self.nGroupsDefined * [0]  # Jc_Nb3Sn0 [A*T^0.5/m^2] Based on short-sample measurement
        self.nHalfTurnsDefined = np.sum(self.nT)
        #  Scale up or down the contribution of heat exchange through the short side of the conductors (useful to change the insulation between coil layers
        insulationBetweenLayers = 0E-6
        insulationAroundCables = self.c.wire['si_h']  # !!!! check what to do with 'si_w  TODO
        self.fScaling_Pex_AlongHeight_Defined = (2 * insulationAroundCables) / (
                    2 * insulationAroundCables + insulationBetweenLayers)
        # # # Quench initiation calculation: Force selected half-turns to quench
        self.iStartQuench = self.c.quench[
            'iStartQuench']  # [1]  # Indices of the half-turns that are set to quench at a given time
        self.tStartQuench = self.c.quench[
            'tStartQuench']  # [9999]  # Time at which each selected half-turn quenches [s]
        self.lengthHotSpot_iStartQuench = [
            10E-3]  # Length of the initial hot-spot [m] (it can be set to a large value to implement a full 2D model)
        self.vQ_iStartQuench = [
            9999]  # Quench propagation velocity [m/s] (you can write 2x higher velocity if the quench propagates in two directions)

        # # # Circuit warm resistance and power-supply crowbar
        self.R_circuit = 0.000  # Resistance of the warm parts of the circuit [Ohm]
        self.R_crowbar = 0.000  # Resistance of crowbar of the power supply [Ohm]
        self.Ud_crowbar = 0.000  # Forward voltage drop of a diode or thyristor in the crowbar of the power supply [V]

        # # # Power supply control
        self.t_PC = 0  # Time when the power supply is switched off and the crowbar is switched on [s]
        self.t_PC_LUT = [-0.02, self.t_PC, self.t_PC + 0.01]  # LUT controlling power supply, Time [s]
        self.I_PC_LUT = [self.I00, self.I00, 0]  # LUT controlling power supply, Current [A]

        # # # Energy-extraction system
        self.tEE = self.c.quench['tEE']  # Time when the energy-extraction system is triggered [s]
        self.R_EE_triggered = self.c.quench['R_EE_triggered']  # Resistance of the energy-extraction system [Ohm]

        # # # Time Vector Definition
        # Time Vector Definition. Parameters used to generate the time vector.
        # Each triplet of numbers defines a time window: first element is the start time, second element is the time step in that window, third element is the end time. It must contain a number of elements multiple of 3. Any time point above t=1000 s will be ignored.
        # start, step, end
        # self.time_vector_params = [-0.06, 2.50E-05, -0.001,
        #                            -0.000975, 2.50E-05, 0.04,
        #                            0.0405, 5.00E-04, 0.1,
        #                            0.101, 1.00E-03, 1]
        self.time_vector_params = [-0.1, 1.00E-03, 3]
        # input_folder = os.path.join(os.getcwd(), "Inputs")
        Rin, Rout, Zlow, Zhigh, self.I, Nturns, Nloop = self.c.coil_set()
        self.headerLines = 1
        self.strandToGroup = np.array([])
        self.strandToHalfTurn = np.array([])
        idx = []
        self.x = []
        self.y = []
        self.Bx = []
        self.By = []
        Area = []
        self.I = []
        fillFactor = []

        # Read file

        file = open(self.c.map2d, "r")
        fileContent = file.read()

        # Separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow) - 1):
            if index > self.headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                self.strandToGroup = np.hstack([self.strandToGroup, int(row[0])])
                self.strandToHalfTurn = np.hstack([self.strandToHalfTurn, int(row[1])])
                idx = np.hstack([idx, float(row[2])])
                self.x = np.hstack([self.x, float(row[3]) / 1000])  # in [m]
                self.y = np.hstack([self.y, float(row[4]) / 1000])  # in [m]
                self.Bx = np.hstack([self.Bx, float(row[5])])
                self.By = np.hstack([self.By, float(row[6])])
                Area = np.hstack([Area, float(row[7])])
                self.I = np.hstack([self.I, float(row[8])])
                fillFactor = np.hstack([fillFactor, float(row[9])])

        self.nStrandsFieldMap = len(self.x)
        # Calculate absolute magnetic field
        self.B = []
        for i in range(self.nStrandsFieldMap):
            self.B = np.hstack([self.B, (self.Bx[i] ** 2 + self.By[i] ** 2) ** .5])
        self.nStrands = len(self.strandToGroup)
        polarities = np.sign(self.I)
        self.nHalfTurns = int(np.max(self.strandToHalfTurn))
        self.nTurns = self.nHalfTurns  # this is specific for solenoids
        self.nGroups = int(np.max(self.strandToGroup));
        self.nS = []
        for ht in range(1, self.nHalfTurns + 1):
            # nS =sum(strandToHalfTurn==ht);
            self.nS = np.hstack(
                [self.nS, np.size(np.where(self.strandToHalfTurn == ht))])  # Number of strands in each half-turn
        self.nS = np.int_(self.nS)
        self.strandToGroup = np.int_(self.strandToGroup)
        self.strandToHalfTurn = np.int_(self.strandToHalfTurn)
        self.halfTurnToTurn = self.strandToHalfTurn

        # Average half-turn positions
        self.x_ave = []
        self.y_ave = []
        for ht in range(1, self.nHalfTurns + 1):
            self.x_ave = np.hstack([self.x_ave, np.mean(self.x[np.where(self.strandToHalfTurn == ht)])])
            self.y_ave = np.hstack([self.y_ave, np.mean(self.y[np.where(self.strandToHalfTurn == ht)])])

        # Average group positions
        self.x_ave_group = []
        self.y_ave_group = []
        for g in range(1, self.nGroups + 1):
            self.x_ave_group = np.hstack([self.x_ave_group, np.mean(self.x[np.where(self.strandToGroup == g)])])
            self.y_ave_group = np.hstack([self.y_ave_group, np.mean(self.y[np.where(self.strandToGroup == g)])])

        # # Definition of groups of conductors
        self.GroupToCoilSection = self.nGroups * [1]
        self.polarities_inGroup = self.nGroups * [+1]

        # Count number of groups defined
        self.nCoilSectionsDefined = np.max(self.GroupToCoilSection)
        self.nGroupsDefined = len(self.GroupToCoilSection)

        # Number of strands in each cable belonging to a particular group
        nStrands_inGroup = self.nGroupsDefined * [1]
        self.nStrands_inGroup = nStrands_inGroup
        # length of each half turn [m] (default=l_magnet)
        self.l_mag_inGroup = 2 * np.pi * (Rin + Rout) / 2  # Length of turns of each layer

        # # # Electrical order of the turns
        # Start and end indices of each group
        indexTstop = np.cumsum(self.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.nT[i]])

        # Calculation of the electrical order of the half-turns
        self.el_order_groups = range(self.nGroupsDefined, 0, -1)  # Electrical order of the groups
        winding_order_groups = int(self.nGroupsDefined / 2) * [0,
                                                               1]  # Winding direction of the turns: following LEDET order (-->0), or its inverse (-->1)

        if len(self.el_order_groups) != self.nGroupsDefined:
            raise Exception(
                'Length of the vector el_order_groups ({}) must be equal to nGroupsDefined={}.'.format(
                    len(self.el_order_groups),
                    self.nGroupsDefined))
        self.el_order_half_turns = [];
        for p in self.el_order_groups:
            for k in range(self.nT[p - 1]):
                if winding_order_groups[p - 1] == 0:
                    self.el_order_half_turns.append(indexTstart[p - 1] + k)
                if winding_order_groups[p - 1] == 1:
                    self.el_order_half_turns.append(indexTstop[p - 1] - k)

        self.el_order_half_turns_Array = np.int_(self.el_order_half_turns)  # this is just used for plotting
        # Inclination of cables with respect to X axis (including transformations for mirror and rotation)
        self.alphasDEG = self.nHalfTurnsDefined * [0]
        # Rotate cable by a certain angle [deg]
        self.rotation_block = self.nHalfTurnsDefined * [0]
        # Mirror cable along the bisector of its quadrant (0=no, 1=yes)
        self.mirror_block = self.nHalfTurnsDefined * [0]
        # Mirror cable along the Y axis (0=no, 1=yes)
        self.mirrorY_block = self.nHalfTurnsDefined * [0]

        # # # Heat exchange between half-turns along the cable wide side
        # Pairs of half-turns exchanging heat along the cable wide side
        self.iContactAlongWidth_From = []
        self.iContactAlongWidth_To = []
        for g in range(self.nGroupsDefined):
            self.iContactAlongWidth_From.extend(range(indexTstart[g], indexTstop[g]))
            self.iContactAlongWidth_To.extend(range(indexTstart[g] + 1, indexTstop[g] + 1))
        pairs_close = close_pairs_ckdtree(np.column_stack((self.x, self.y)),
                                          self.max_distance)  # find all pairs of strands closer than a distance of max_d

        contact_pairs = set([])  # find pairs that belong to half-turns located in different groups
        for p in pairs_close:
            if not self.strandToGroup[p[0]] == self.strandToGroup[p[1]]:
                contact_pairs.add((self.strandToHalfTurn[p[0]], self.strandToHalfTurn[p[1]]))

        self.iContactAlongHeight_From = []
        self.iContactAlongHeight_To = []
        for p in contact_pairs:  # assign the pair values to two distinct vectors
            self.iContactAlongHeight_From.append(p[0])
            self.iContactAlongHeight_To.append(p[1])

        idxSort = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(
            self.iContactAlongHeight_From))]  # find indices to order the vector iContactAlongHeight_From

        # reorder both iContactAlongHeight_From and iContactAlongHeight_To using the indices
        self.iContactAlongHeight_From = [self.iContactAlongHeight_From[i] for i in idxSort]
        self.iContactAlongHeight_To = [self.iContactAlongHeight_To[i] for i in idxSort]
        self.iContactAlongHeight_From_Array = np.int_(self.iContactAlongHeight_From)
        self.iContactAlongHeight_To_Array = np.int_(self.iContactAlongHeight_To)
        self.iContactAlongWidth_From_Array = np.int_(self.iContactAlongWidth_From)
        self.iContactAlongWidth_To_Array = np.int_(self.iContactAlongWidth_To)

        # # # Electrical circuit during powering transient
        # # <img src="../resources/LEDET_CircuitSchematic_Powering.png" width="750"/>

        # # # Electrical circuit during protection transient
        # # <img src="../resources/LEDET_CircuitSchematic_Protection.png" width="750"/>

        # # # CLIQ system
        self.tCLIQ = 99999  # Time when the CLIQ system is triggered [s]
        self.directionCurrentCLIQ = [1]  # Direction of the introduced current change for the chosen CLIQ configuration
        self.nCLIQ = 1  # Number of CLIQ units
        self.U0 = 1000  # CLIQ charging voltage [V]
        self.C = 0.04  # Capacitance of the CLIQ capacitor bank [F]
        self.Rcapa = 0.05  # Resistance of the CLIQ leads [Ohm]

        # # # Quench heater parameters - DUMMY VALUES: THERE ARE NO QUENCH HEATERS

        nHeaterStrips = 1  # Number of quench heater strips to write in the file

        self.tQH = [
            99999]  # Time at which the power supply connected to the QH strip is triggered (Low-field QHs set to a very large value to avoid triggering).
        self.U0_QH = nHeaterStrips * [450]  # Charging voltage of the capacitor connected to the QH strip.
        self.C_QH = nHeaterStrips * [14.1E-3]  # Capacitance of the capacitor connected to the QH strip.
        self.R_warm_QH = nHeaterStrips * [0.50]  # Resistance of the warm leads of the QH strip discharge circuit.
        self.w_QH = nHeaterStrips * [15E-3]  # Width of the non-Cu-plated part of the the QH strip
        self.h_QH = nHeaterStrips * [25E-6]  # Height of the non-Cu-plated part of the QH strip.
        self.s_ins_QH = nHeaterStrips * [
            75E-6]  # Thickness of the insulation layer between QH strip and coil insulation layer.
        self.type_ins_QH = nHeaterStrips * [
            2]  # Type of material of the insulation layer between QH strip and coil insulation layer (1=G10; 2=kapton)
        # Thickness of the insulation layer between QH strip and the helium bath (or the collars); on this side, the QH strip is thermally connected to an infinite thermal sink at constant temperature.
        self.s_ins_QH_He = nHeaterStrips * [150E-6]
        self.type_ins_QH_He = nHeaterStrips * [
            2]  # Type of material of the insulation layer between QH strip and helium bath (1=G10; 2=kapton)
        self.l_QH = nHeaterStrips * [14.3]  # Length of the QH strip.
        self.f_QH = nHeaterStrips * [
            .12 / (.12 + .4)]  # Fraction of QH strip covered by heating stations (not-Cu-plated).

        # # # Heat exchange between quench heater strips and half-turns - DUMMY VALUES: THERE ARE NO QUENCH HEATERS
        self.iQH_toHalfTurn_To = [1]  # Thermal connections between heater strips and half-turns
        self.iQH_toHalfTurn_From = [1]

        # # # Adiabatic hot-spot temperature calculation
        # Time from which the adiabatic hot-spot temperature calculation starts. For each coil section, calculate the adiabatic hot-spot temperature in the highest-field strand/cable [s]
        self.tQuench = self.nCoilSectionsDefined * [-0.05]
        self.initialQuenchTemp = self.nCoilSectionsDefined * [
            10]  # Initial quench temperature in the hot-spot temperature calculation [K]

        # # # Self-mutual inductance matrix between half-turns, and between coil sections
        # Set M_InductanceBlock_m to 0 to force LEDET to import the self-mutual inductances from the .csv file
        self.M_InductanceBlock_m = 0

        # Define to which inductive block each half-turn belongs
        self.HalfTurnToInductanceBlock = []
        for g in range(1, self.nGroupsDefined + 1):
            for j in range(self.nT[g - 1]):
                self.HalfTurnToInductanceBlock.append(g)

        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(self.nT[:-1])]);
        indexTstop = np.cumsum(self.nT);
        self.HalfTurnToGroup = np.zeros((1, self.nHalfTurnsDefined), dtype=int)
        self.HalfTurnToGroup = self.HalfTurnToGroup[0]
        self.HalfTurnToCoilSection = np.zeros((1, self.nHalfTurnsDefined), dtype=int)
        self.HalfTurnToCoilSection = self.HalfTurnToCoilSection[0]
        for g in range(1, self.nGroupsDefined + 1):
            self.HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            self.HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = self.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        indexSstart = np.hstack([1, 1 + np.cumsum(self.nS[:-1])]);
        indexSstop = np.cumsum(self.nS);
        self.strandToGroup = np.zeros((1, self.nStrands), dtype=int)
        self.strandToGroup = self.strandToGroup[0]
        self.strandToCoilSection = np.zeros((1, self.nStrands), dtype=int)
        self.strandToCoilSection = self.strandToCoilSection[0]
        for ht in range(1, self.nHalfTurnsDefined + 1):
            self.strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = self.HalfTurnToGroup[ht - 1]
            self.strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = self.HalfTurnToCoilSection[ht - 1]

        # Field-Map Files Options
        self.Iref = self.I00
        self.flagIron = 0
        self.flagSelfField = 0
        self.columnsXY = [4, 5]
        self.columnsBxBy = [6, 7]
        self.flagPlotMTF = 0

        # Input Generation Options
        self.flag_calculateInductanceMatrix = 0
        self.flag_useExternalInitialization = 0
        self.flag_initializeVar = 0

        # Simulation Run Options
        self.flag_fastMode = 1
        self.flag_controlCurrent = 0
        self.flag_automaticRefinedTimeStepping = 1

        # Simulation Physics Options
        self.flag_IronSaturation = 0  # this was originally set to 1
        self.flag_InvertCurrentsAndFields = 0
        self.flag_ScaleDownSuperposedMagneticField = 1
        self.flag_HeCooling = 0  # was 2 TODO
        self.fScaling_Pex = 1
        self.fScaling_Pex_AlongHeight = self.fScaling_Pex_AlongHeight_Defined
        self.fScaling_MR = 1
        self.flag_scaleCoilResistance_StrandTwistPitch = 0
        self.flag_separateInsulationHeatCapacity = 0
        self.flag_ISCL = 0
        self.fScaling_Mif = 1
        self.fScaling_Mis = 0
        self.flag_StopIFCCsAfterQuench = 0
        self.flag_StopISCCsAfterQuench = 0
        self.tau_increaseRif = 0.005
        self.tau_increaseRis = 0.01
        self.fScaling_RhoSS = 1.09
        self.maxVoltagePC = 10
        self.flag_symmetricGroundingEE = 0
        self.flag_removeUc = 0
        self.BtX_background = 0
        self.BtY_background = 0

        # Post-Processing Options
        self.flag_showFigures = 0
        self.flag_saveFigures = 1
        self.flag_saveMatFile = 1
        self.flag_saveTxtFiles = 0
        self.flag_generateReport = 1
        self.flag_hotSpotTemperatureInEachGroup = 0
        self.MinMaxXY_MTF = [75, 125, -120, 120]
        #
        #
        # # # Define the values of all Plots variables - Change something only if you know what you're doing
        # Define the values of all Plots variables
        self.suffixPlot = ["'_Temperature2D_'"]
        self.typePlot = [4]
        self.outputPlotSubfolderPlot = ["Temperature"]
        self.variableToPlotPlot = ["T"]
        self.selectedStrandsPlot = ["1:nStrands"]
        self.selectedTimesPlot = ["1:n_time"]
        self.labelColorBarPlot = ["'Temperature [K]'"]
        self.minColorBarPlot = ["min(min(variableToPlot))"]
        self.maxColorBarPlot = ["max(max(variableToPlot))"]
        self.MinMaxXYPlot = []
        self.flagSavePlot = [1]
        self.flagColorPlot = [1]
        self.flagInvisiblePlot = [1]
        #
        #
        # # # Define the values of all Variables variables - Change something only if you know what you're doing
        # # Define the values of all Variables variables
        self.variableToSaveTxt = ['time_vector', 'Ia', 'Ib', 'T_ht', 'dT_dt_ht', 'flagQ_ht', 'IifX', 'IifY', 'Iis',
                                  'dIifXDt',
                                  'dIifYDt', 'dIisDt', 'Uc', 'U_QH', 'T_QH', 'time_vector', 'R_CoilSections',
                                  'U_inductive_dynamic_CoilSections']
        self.typeVariableToSaveTxt = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
        self.variableToInitialize = ['Ia', 'Ib', 'T_ht', 'dT_dt_ht', 'flagQ_ht', 'IifX', 'IifY', 'Iis', 'dIifXDt',
                                     'dIifYDt',
                                     'dIisDt', 'Uc', 'U_QH', 'T_QH']
        #

        # # # Differential inductance versus current (Iron-yoke effect) - IMPORT FROM ROXIE
        # Copy/paste the values after calculation using ROXIE or COMSOL or another software
        self.fL_I = [0, 1000]
        self.fL_L = [1.0, 1.0]

        if self.verbose:
            print('Total number of strands in the field-map from ROXIE = {}'.format(self.nStrandsFieldMap))
            print('Peak magnetic field in the field-map from ROXIE = {} T'.format(np.max(self.B)))
            print('Total number of strands = ' + str(self.nStrands))
            print('Total number of half-turns = ' + str(self.nHalfTurns))
            print('Total number of turns = ' + str(self.nTurns))
            print('Total number of groups = ' + str(self.nGroups))
            print(str(self.nCoilSectionsDefined) + ' coil sections defined.')
            print(str(self.nGroupsDefined) + ' groups defined.')
            print(str(self.nHalfTurnsDefined) + ' half-turns defined.')

            print('fScaling_Pex_AlongHeight_Defined = ')
            print(self.fScaling_Pex_AlongHeight_Defined)

            print('The groups will be connected electrically in this order:')
            print(self.el_order_groups)

            print('Calculated electrical order of the half-turns:')
            print('el_order_half_turns = ' + str(self.el_order_half_turns))
            print('Heat exchange along the cable wide side - Calculated indices:')
            print('iContactAlongWidth_From = ')
            print(self.iContactAlongWidth_From)
            print('iContactAlongWidth_To = ')
            print(self.iContactAlongWidth_To)

            print('Heat exchange along the cable narrow side - Calculated indices:')
            print('iContactAlongHeight_From = ')
            print(self.iContactAlongHeight_From)
            print('iContactAlongWidth_To = ')
            print(self.iContactAlongHeight_To)

            print('iQH_toHalfTurn_From = {}'.format(self.iQH_toHalfTurn_From))
            print('iQH_toHalfTurn_To = {}'.format(self.iQH_toHalfTurn_To))
            print('Total magnet self-inductance: ' + str(self.M_m) + ' H')
            print(self.HalfTurnToInductanceBlock)
            # Visualize variable descriptions, names, and values
            print('### "Inputs" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupInputs,
                                                       self.paramLEDET.variablesInputs)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Options" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupOptions,
                                                       self.paramLEDET.variablesOptions)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Plots" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupPlots,
                                                       self.paramLEDET.variablesPlots)

            # Visualize variable descriptions, names, and values
            print('')
            print('### "Variables" variables ###')
            self.paramLEDET.printVariableDescNameValue(self.paramLEDET.variableGroupVariables,
                                                       self.paramLEDET.variablesVariables)

        # # # Calculate approximate quench detection time in case the quench occurs in any half-turn

    def write_ledet_input(self):
        """
        Writes LEDET input excel file to disk
        """
        # Load default LEDET variable descriptions
        self.paramLEDET = ParametersLEDET()

        # Add all Inputs variables to a list - DO NOT CHANGE
        self.paramLEDET.addVariablesInputs(
            self.T00, self.l_magnet, self.I00, self.M_m,
            self.fL_I, self.fL_L,
            self.GroupToCoilSection, self.polarities_inGroup, self.nT,
            self.nStrands_inGroup, self.l_mag_inGroup, self.ds_inGroup,
            self.f_SC_strand_inGroup, self.f_ro_eff_inGroup, self.Lp_f_inGroup,
            self.RRR_Cu_inGroup,
            self.SCtype_inGroup, self.STtype_inGroup, self.insulationType_inGroup,
            self.internalVoidsType_inGroup,
            self.externalVoidsType_inGroup,
            self.wBare_inGroup, self.hBare_inGroup, self.wIns_inGroup, self.hIns_inGroup,
            self.Lp_s_inGroup, self.R_c_inGroup,
            self.Tc0_NbTi_ht_inGroup, self.Bc2_NbTi_ht_inGroup,
            self.c1_Ic_NbTi_inGroup, self.c2_Ic_NbTi_inGroup,
            self.Tc0_Nb3Sn_inGroup, self.Bc2_Nb3Sn_inGroup, self.Jc_Nb3Sn0_inGroup,
            self.el_order_half_turns,
            self.alphasDEG, self.rotation_block, self.mirror_block, self.mirrorY_block,
            self.iContactAlongWidth_From, self.iContactAlongWidth_To,
            self.iContactAlongHeight_From,
            self.iContactAlongHeight_To,
            self.iStartQuench, self.tStartQuench, self.lengthHotSpot_iStartQuench,
            self.vQ_iStartQuench,
            self.R_circuit, self.R_crowbar, self.Ud_crowbar, self.t_PC, self.t_PC_LUT, self.I_PC_LUT,
            self.tEE, self.R_EE_triggered,
            self.tCLIQ, self.directionCurrentCLIQ, self.nCLIQ, self.U0, self.C, self.Rcapa,
            self.tQH, self.U0_QH, self.C_QH, self.R_warm_QH, self.w_QH, self.h_QH, self.s_ins_QH, self.type_ins_QH,
            self.s_ins_QH_He, self.type_ins_QH_He, self.l_QH, self.f_QH,
            self.iQH_toHalfTurn_From, self.iQH_toHalfTurn_To,
            self.tQuench, self.initialQuenchTemp,
            self.HalfTurnToInductanceBlock, self.M_InductanceBlock_m
        )

        # Add all Options variables to a list - DO NOT CHANGE
        self.paramLEDET.addVariablesOptions(
            self.time_vector_params,
            self.Iref, self.flagIron, self.flagSelfField, self.headerLines, self.columnsXY, self.columnsBxBy,
            self.flagPlotMTF,
            self.flag_calculateInductanceMatrix, self.flag_useExternalInitialization, self.flag_initializeVar,
            self.flag_fastMode, self.flag_controlCurrent, self.flag_automaticRefinedTimeStepping,
            self.flag_IronSaturation,
            self.flag_InvertCurrentsAndFields, self.flag_ScaleDownSuperposedMagneticField, self.flag_HeCooling,
            self.fScaling_Pex,
            self.fScaling_Pex_AlongHeight,
            self.fScaling_MR, self.flag_scaleCoilResistance_StrandTwistPitch, self.flag_separateInsulationHeatCapacity,
            self.flag_ISCL, self.fScaling_Mif, self.fScaling_Mis, self.flag_StopIFCCsAfterQuench,
            self.flag_StopISCCsAfterQuench, self.tau_increaseRif,
            self.tau_increaseRis,
            self.fScaling_RhoSS, self.maxVoltagePC, self.flag_symmetricGroundingEE, self.flag_removeUc,
            self.BtX_background, self.BtY_background,
            self.flag_showFigures, self.flag_saveFigures, self.flag_saveMatFile, self.flag_saveTxtFiles,
            self.flag_generateReport,
            self.flag_hotSpotTemperatureInEachGroup, self.MinMaxXY_MTF
        )

        # Define the values of all Plots variables - DO NOT CHANGE
        self.paramLEDET.addVariablesPlots(
            self.suffixPlot, self.typePlot, self.outputPlotSubfolderPlot, self.variableToPlotPlot,
            self.selectedStrandsPlot, self.selectedTimesPlot,
            self.labelColorBarPlot, self.minColorBarPlot, self.maxColorBarPlot, self.MinMaxXYPlot, self.flagSavePlot,
            self.flagColorPlot, self.flagInvisiblePlot
        )

        # Define the values of all Variables variables - DO NOT CHANGE
        self.paramLEDET.addVariablesVariables(
            self.variableToSaveTxt, self.typeVariableToSaveTxt, self.variableToInitialize
        )
        self.text = {'x': [], 'y': [], 't': []}
        paramLEDET_notebook = ParametersLEDET()  # Load default LEDET variable descriptions
        uQuenchDetectionThreshold = 0.1  # [V]# Define quench detection threshold
        iStartQuench = list(
            range(1, self.nHalfTurnsDefined + 1))  # Indices of the half-turns that are set to quench at a given time
        tStartQuench = [9999] * self.nHalfTurnsDefined  # Time at which each selected half-turn quenches [s]
        lengthHotSpot_iStartQuench = [
                                         10E-3] * self.nHalfTurnsDefined  # Length of the initial hot-spot [m] (it can be set to a large value to implement a full 2D model)
        paramLEDET_notebook.localsParser(locals())
        paramLEDET_notebook.localsParser(
            self.__dict__)  # this is very ubly, brut force passing of attributes to local parser. This locals() passing above needs rewrite.
        # paramLEDET_notebook.adjust_vQ(os.path.join(self.c.output_folder, nameMagnet + '_All_NoIron_NoSelfField.map2d'))
        paramLEDET_notebook.adjust_vQ(self.c.map2d)
        self.vQ_iStartQuench = paramLEDET_notebook.getAttribute("Inputs",
                                                                "vQ_iStartQuench")  # Quench propagation velocity [m/s] (you can write 2x higher velocity if the quench propagates in two directions)

        # Set the location and time of the quench
        # halfTurn_start_quench = 1
        # time_start_quench = -0.05
        # tStartQuench[halfTurn_start_quench-1] = time_start_quench

        # Calculate resistance of each turn at T=10 K
        rho_Cu_10K = 1.7E-10  # [Ohm*m] Approximate Cu resistivity at T=10 K, B=0, for RRR=100
        rho_Cu_10K_B = 4E-11  # [Ohm*m/T] Approximate Cu magneto-resistivity factor
        self.rho_ht_10K = []
        self.r_el_ht_10K = []
        self.mean_B_ht = []
        self.tQuenchDetection = []
        for ht in range(1, self.nHalfTurns + 1):
            current_group = self.HalfTurnToGroup[ht - 1]
            mean_B = np.mean(
                self.B[np.where(
                    self.strandToHalfTurn == ht)]) / self.Iref * self.I00  # average magnetic field in the current half-turn
            rho_mean = rho_Cu_10K + rho_Cu_10K_B * mean_B  # average resistivity in the current half-turn
            cross_section = self.nStrands_inGroup[current_group - 1] * np.pi / 4 * self.ds_inGroup[
                current_group - 1] ** 2 * (
                                    1 - self.f_SC_strand_inGroup[current_group - 1])
            r_el_m = rho_mean / cross_section  # Electrical resistance per unit length
            tQD = uQuenchDetectionThreshold / (self.vQ_iStartQuench[
                                                   ht - 1] * r_el_m * self.I00)  # Approximate time to reach the quench detection threshold
            self.mean_B_ht = np.hstack([self.mean_B_ht, mean_B])
            self.rho_ht_10K = np.hstack([self.rho_ht_10K, rho_mean])
            self.r_el_ht_10K = np.hstack([self.r_el_ht_10K, r_el_m])
            self.tQuenchDetection = np.hstack([self.tQuenchDetection, tQD])

        self.paramLEDET.writeFileLEDET(self.excel_file_path, SkipConsistencyCheck=True)  # Write the LEDET input file

        # self.name_file_vQ = self.nameMagnet + 'vQ_I00' + '.csv'  #### Write calculated quench propagation velocities to a .csv file
        # np.savetxt(os.path.join(self.c.output_folder, self.name_file_vQ), self.vQ_iStartQuench, delimiter=",")
        # if self.verbose:
        #     print('Minimum quench detection time = {} ms'.format(min(self.tQuenchDetection * 1e3)))
        #     print('Maximum quench detection time = {} ms'.format(max(self.tQuenchDetection * 1e3)))
        #     print('File {} with calculated quench propagation velocities was written.'.format(self.name_file_vQ))

        print("LEDET inputs written")

    def plotter(self, data, titles, labels, types, texts, size):
        """
        Default plotter for most standard and simple cases
        """
        fig, axs = plt.subplots(nrows=1, ncols=len(data), figsize=size)
        if len(data) == 1:
            axs = [axs]
        for ax, ty, d, ti, l, te in zip(axs, types, data, titles, labels, texts):
            if ty == 'scatter':
                plot = ax.scatter(d['x'], d['y'], s=2, c=d['z'], cmap='jet')  # =cm.get_cmap('jet'))
                if len(te["t"]) != 0:
                    for x, y, z in zip(te["x"], te["y"], te["t"]):
                        ax.text(x, y, z)
            elif ty == 'plot':
                plt.plot
            ax.set_xlabel(l["x"], **self.selectedFont)
            ax.set_ylabel(l["y"], **self.selectedFont)
            ax.set_title(f'{ti}', **self.selectedFont)
            # ax.set_aspect('equal')
            # ax.figure.autofmt_xdate()
            cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(plot, cax=cax, orientation='vertical')
            if len(l["z"]) != 0:
                cbar.set_label(l["z"], **self.selectedFont)
        plt.tight_layout()
        plt.show()
        plt.cla

    def plot_field(self):
        """
        Plot magnetic field components of a coil
        """
        data = [{'x': self.x, 'y': self.y, 'z': self.I},
                {'x': self.x, 'y': self.y, 'z': self.Bx},
                {'x': self.x, 'y': self.y, 'z': self.By},
                {'x': self.x, 'y': self.y, 'z': self.B}]
        titles = ['Current [A]', 'Br [T]', 'Bz [T]', 'Bmod [T]']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_strands_groups_layers(self):
        types = ['scatter'] * 4
        data = [{'x': self.x, 'y': self.y, 'z': self.strandToHalfTurn},
                {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
                {'x': self.x, 'y': self.y, 'z': self.halfTurnToTurn},
                {'x': self.x, 'y': self.y, 'z': self.nS}]
        titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
        t_ht = copy.deepcopy(self.text)
        for ht in range(self.nHalfTurns):
            t_ht['x'].append(self.x_ave[ht])
            t_ht['y'].append(self.y_ave[ht])
            t_ht['t'].append('{}'.format(ht + 1))
        t_ng = copy.deepcopy(self.text)
        for g in range(self.nGroups):
            t_ng['x'].append(self.x_ave_group[g])
            t_ng['y'].append(self.y_ave_group[g])
            t_ng['t'].append('{}'.format(g + 1))
        texts = [t_ht, t_ng, self.text, self.text]
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_polarities(self):
        polarities_inStrand = np.zeros((1, self.nStrands), dtype=int)
        polarities_inStrand = polarities_inStrand[0]
        for g in range(1, self.nGroupsDefined + 1):
            polarities_inStrand[np.where(self.strandToGroup == g)] = self.polarities_inGroup[g - 1]
        data = [{'x': self.x, 'y': self.y, 'z': polarities_inStrand}]
        titles = ['Current polarities']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (5, 5))

    def plot_half_turns(self):
        data = [{'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToGroup},
                {'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToCoilSection},
                {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
                {'x': self.x, 'y': self.y, 'z': self.strandToCoilSection}]
        titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_nonlin_induct(self):
        f = plt.figure(figsize=(7.5, 5))
        plt.plot(self.fL_I, self.fL_L, 'ro-')
        plt.xlabel('Current [A]', **self.selectedFont)
        plt.ylabel('Factor scaling nominal inductance [-]', **self.selectedFont)
        plt.title('Differential inductance versus current', **self.selectedFont)
        plt.xlim([0, self.I00 * 2])
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_psu_and_trig(self):
        # Plot
        f = plt.figure(figsize=(7.5, 5))
        plt.plot([self.t_PC, self.t_PC], [0, 1], 'k--', linewidth=4.0, label='t_PC')
        plt.plot([self.tEE, self.tEE], [0, 1], 'r--', linewidth=4.0, label='t_EE')
        plt.plot([self.tCLIQ, self.tCLIQ], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
        plt.plot([np.min(self.tQH), np.min(self.tQH)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Trigger [-]', **self.selectedFont)
        plt.xlim([1E-4, self.time_vector_params[-1]])
        plt.title('Power suppply and quench protection triggers', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.legend(loc='best')
        plt.show()

    def plot_quench_prop_and_resist(self):
        f = plt.figure(figsize=(16, 6))
        plt.subplot(1, 4, 1)
        # fig, ax = plt.subplots()
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.vQ_iStartQuench)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('2D cross-section Quench propagation velocity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Quench velocity [m/s]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 2)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.rho_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistivity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistivity [$\Omega$*m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 3)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.r_el_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistance per unit length', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistance per unit length [$\Omega$/m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 4)
        plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.tQuenchDetection * 1e3)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Approximate quench detection time', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Time [ms]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')
        plt.show()

    def plot_q_prop_v(self):
        f = plt.figure(figsize=(20, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.mean_B_ht, self.vQ_iStartQuench, 'ko')
        plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
        plt.ylabel('Quench propagation velocity [m/s]', **self.selectedFont)
        plt.title('Quench propagation velocity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        plt.rcParams.update({'font.size': 12})
        plt.subplot(1, 2, 2)
        plt.plot(self.mean_B_ht, self.tQuenchDetection * 1e3, 'ko')
        plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
        plt.ylabel('Approximate quench detection time [ms]', **self.selectedFont)
        plt.title('Approximate quench detection time', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_electrical_order(self):
        plt.figure(figsize=(16, 8))
        plt.subplot(1, 3, 1)
        plt.scatter(self.x_ave, self.y_ave, s=2, c=np.argsort(self.el_order_half_turns_Array))
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.set_cmap('jet')
        cbar = plt.colorbar()
        cbar.set_label('Electrical order [-]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        # Plot
        plt.subplot(1, 3, 2)
        plt.plot(self.x_ave[self.el_order_half_turns_Array - 1], self.y_ave[self.el_order_half_turns_Array - 1], 'k')
        plt.scatter(self.x_ave, self.y_ave, s=2, c=self.nS)
        plt.scatter(self.x_ave[self.el_order_half_turns_Array[0] - 1],
                    self.y_ave[self.el_order_half_turns_Array[0] - 1], s=50, c='b',
                    label='Positive lead')
        plt.scatter(self.x_ave[self.el_order_half_turns_Array[-1] - 1],
                    self.y_ave[self.el_order_half_turns_Array[-1] - 1], s=50, c='r',
                    label='Negative lead')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.legend(loc='lower left')
        # Plot
        plt.subplot(1, 3, 3)
        # plt.plot(x_ave_group[elPairs_GroupTogether_Array[:,0]-1],y_ave_group[elPairs_GroupTogether_Array[:,1]-1],'b')
        plt.scatter(self.x, self.y, s=2, c='k')
        plt.scatter(self.x_ave_group, self.y_ave_group, s=10, c='r')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the groups (only go-lines)', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_heat_exchange_order(self):
        plt.figure(figsize=(10, 10))
        # plot strand positions
        plt.scatter(self.x, self.y, s=2, c='b')
        # plot conductors
        # for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
        #     pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
        #     line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
        #     plt.gca().add_line(line)
        # plot average conductor positions
        # plt.scatter(x_ave, y_ave, s=10, c='r')
        # plot heat exchange links along the cable narrow side
        for i in range(len(self.iContactAlongHeight_From)):
            plt.plot([self.x_ave[self.iContactAlongHeight_From_Array[i] - 1],
                      self.x_ave[self.iContactAlongHeight_To_Array[i] - 1]],
                     [self.y_ave[self.iContactAlongHeight_From_Array[i] - 1],
                      self.y_ave[self.iContactAlongHeight_To_Array[i] - 1]], 'k')
        # plot heat exchange links along the cable wide side
        for i in range(len(self.iContactAlongWidth_From)):
            plt.plot([self.x_ave[self.iContactAlongWidth_From_Array[i] - 1],
                      self.x_ave[self.iContactAlongWidth_To_Array[i] - 1]],
                     [self.y_ave[self.iContactAlongWidth_From_Array[i] - 1],
                      self.y_ave[self.iContactAlongWidth_To_Array[i] - 1]], 'r')
        # plot strands belonging to different conductor groups and clo ser to each other than max_distance
        # for p in pairs_close:
        #     if not strandToGroup[p[0]] == strandToGroup[p[1]]:
        #         plt.plot([X[p[0], 0], X[p[1], 0]], [X[p[0], 1], X[p[1], 1]], c='g')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Heat exchange order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_power_supl_contr(self):
        plt.figure(figsize=(5, 5))
        plt.plot([self.t_PC, self.t_PC], [np.min(self.I_PC_LUT), np.max(self.I_PC_LUT)], 'k--', linewidth=4.0,
                 label='t_PC')
        plt.plot(self.t_PC_LUT, self.I_PC_LUT, 'ro-', label='LUT')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Current [A]', **self.selectedFont)
        plt.title('Look-up table controlling power supply', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def run_LEDET(self):
        LEDET_executable = "LEDET_v2_01_01.exe"
        RunSimulations(self.LEDET_folder, LEDET_executable, self.nameMagnet, Simulations=self.model_no,
                       RunSimulations=False)
        LEDET_exe_path = os.path.join(self.LEDET_folder, LEDET_executable)
        os.chdir(self.LEDET_folder)
        subprocess.call([LEDET_exe_path])


if __name__ == "__main__":
    pass
    # nameMagnet = "ColSol.1"
    # model_no = 0
    # pl = NB_LEDET(nameMagnet, model_no)
    # pl.write_ledet_input()
    # pl.plot_field()
    # pl.plot_strands_groups_layers()
    # pl.plot_polarities()
    # pl.plot_half_turns()
    # pl.plot_nonlin_induct()
    # pl.plot_psu_and_trig()
    # pl.plot_quench_prop_and_resist()
    # pl.plot_q_prop_v()
    # pl.plot_electrical_order()
    # pl.plot_heat_exchange_order()
    # pl.plot_power_supl_contr()