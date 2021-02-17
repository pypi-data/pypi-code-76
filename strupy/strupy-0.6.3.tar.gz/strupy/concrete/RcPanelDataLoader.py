'''
--------------------------------------------------------------------------
Copyright (C) 2015-2020 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of StruPy.
StruPy structural engineering design Python package.
https://bitbucket.org/struthonteam/strupy

StruPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with StruPy; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

File changes:
- python3 compatibility checked
- ROBOTcsvloader() upgraded 
- ROBOTcsvloader() upgraded to ROBOT2016 or lower
- MECWAYloader() upgraded for Mecway 7
- MECWAYloader() added
- multi loadcase import implemented
- ROBOTcsvloader() added
- RFEMxlsloader() upgraded for RFEM 5 output file
- RFEMxlsloader() upgraded
'''

import os
import uuid

from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from tkinter.simpledialog import askstring

import numpy as np
import xlrd
import csv
import easygui

import strupy.units as u

class RcPanelDataLoader():

    def __init__(self):
        print("RcPanelDataLoader init")
        self.initialdir=os.path.dirname(__file__)
        
    def RFEMxlsloader(self, rcpanel, rcpanelload, progress=None):
        #--deleting object data 
        rcpanel.clear_arrays_data()
        rcpanelload.clear_arrays_data()
        #--loading xls files and recognizing surface/result sheets
        from tkinter import Tk
        from tkinter.filedialog import askopenfilenames
        surface_sheet = None
        result_sheet = None
        tryNumber = 1
        while not (surface_sheet and result_sheet):
            root = Tk()
            root.withdraw()
            #----
            ask_text = 'Choose'
            if not surface_sheet:
                ask_text += ' [surface]'
            if not result_sheet:
                ask_text += ' [result]' 
            ask_text += ' xls Rfem output file(s)'
            #----
            filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('xls file', '*.xls')], initialdir=self.initialdir)
            for filename in filename_list:
                if not filename == '':
                    self.initialdir = os.path.dirname(filename)
                book = xlrd.open_workbook(filename)
                result_sheet_list = []
                case_list = []
                for i in book.sheet_names():
                    if '1.4' in i:
                        surface_sheet = book.sheet_by_name(i) #<<<<<<<< surface_sheet
                    if ('Surfaces - Base' in i) or ('Surfaces - Basic' in i) or ('Powierzchnie - Podst' in i)  :
                        result_sheet = book.sheet_by_name(i) #<<<<<<<< result_sheet
                        result_sheet_list.append(result_sheet)
                        case_list.append(i)
            if tryNumber == 4:
                return 0
            tryNumber +=1
        root.destroy()
        #----function for finding column number with some text
        def find_column(headerTextlist, sheet, row):
            find_result = None
            for i in range(40):
                for text in headerTextlist:
                    try:
                        if text == str(sheet.col_values(i)[row]):
                            find_result = [i, str(sheet.col_values(i)[row])]
                            return find_result
                    except IndexError:
                        pass
            if not find_result:
                find_result = ['Not found', None]
            return find_result
        #----
        if progress:
            progress.setValue(20)
        #--finding solver data units
        #----thickness unit
        header = find_column(['d [mm]', 'd [cm]', 'd [m]'], surface_sheet, 1)[1]
        if '[mm]' in header:
            solverunit_thickness = u.mm
        elif '[cm]' in header:
            solverunit_thickness = u.cm
        elif '[m]' in header:
            solverunit_thickness = u.m
        else :
            solverunit_thickness = None
        #----coordinate unit   
        header = find_column([  'Grid Point Coordinates [m]',
                                'Grid Point Coordinates [cm]', 
                                'Grid Point Coordinates [mm]',
                                'Współrzędne punktów rastru [m]',
                                'Współrzędne punktów rastru [cm]',
                                'Współrzędne punktów rastru [mm]'], result_sheet, 0)[1]
        if 'mm' in header:
            solverunit_coord = u.m
        elif 'cm' in header:
            solverunit_coord = u.cm
        elif 'm' in header:
            solverunit_coord = u.m
        else :
            solverunit_coord = None      
        #----internale forces moment unit
        header = find_column([  'Moments [Nm/m]',
                                'Moments [kNm/m]',
                                'Momenty [Nm/m]',
                                'Momenty [kNm/m]'], result_sheet, 0)[1]
        if '[Nm/m]' in header:
            solverunit_moment = u.Nm
        elif '[kNm/m]' in header:
            solverunit_moment = u.kNm
        else :
            solverunit_moment = None      
        #----internale forces force unit
        #print(result_sheet.col_values(10)[0].encode('cp1250'))
        header = find_column([  'Axial Forces [N/m]',
                                'Axial Forces [kN/m]',
                                'Siły osiowe [N/m]',
                                'Siły osiowe [kN/m]'], result_sheet, 0)[1]
        if '[N/m]' in header:
            solverunit_force = u.N
        elif '[kN/m]' in header:
            solverunit_force = u.kN
        else :
            solverunit_force = None      
        #--preparing dictionary with surface number as keys
        col_surface_number = find_column(['Surface', 'Pow.'], surface_sheet, 0)[0]
        surface_number = np.array(surface_sheet.col_values(col_surface_number)[2:])
        surface_number  = np.vectorize(int)(surface_number)
        col_surface_thickness = find_column(['d [mm]', 'd [cm]', 'd [m]'], surface_sheet, 1)[0]
        surface_thickness = np.array(surface_sheet.col_values(col_surface_thickness)[2:])
        thicknessdict = dict(zip(surface_number, surface_thickness))
        emptyrecord = []
        for key in thicknessdict:
            if thicknessdict[key] == '':
                emptyrecord.append(key)
        for i in emptyrecord:
            thicknessdict.pop(i)
        for key in thicknessdict:
            thicknessdict[key] = float(thicknessdict[key])
        #----
        if progress:
            progress.setValue(40)
        #--panel properties in rcpanel
        col_surfaceID = find_column(['No.', 'nr'], result_sheet, 1)[0]
        rcpanel.surfaceID = result_sheet.col_values(col_surfaceID)[2:]
        for i in range(len(rcpanel.surfaceID)):
            if rcpanel.surfaceID[i] == '':
                rcpanel.surfaceID[i] = rcpanel.surfaceID[i-1]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        col_coord_Xp = find_column(['X'], result_sheet, 1)[0]
        rcpanel.coord_Xp = np.array(result_sheet.col_values(col_coord_Xp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        col_coord_Yp = find_column(['Y'], result_sheet, 1)[0]
        rcpanel.coord_Yp  = np.array(result_sheet.col_values(col_coord_Yp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        col_coord_Zp = find_column(['Z'], result_sheet, 1)[0]
        rcpanel.coord_Zp = np.array(result_sheet.col_values(col_coord_Zp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.h = np.vectorize(lambda x: thicknessdict[x])(rcpanel.surfaceID) * (solverunit_thickness / rcpanel.h_unit).asNumber()
        #--unexpected value detect and replace in result data from RFEM
        def unexpected_replace(value):
            if value in ['-', 'The result value in the point is not defined']:
                value = 0.0
                print('unexpected value replaced')
            return float(value)
        #--panel internal forces in rcpanelload
        for case_number in range(len(result_sheet_list)):
            case_name = case_list[case_number][:4]
            result_sheet = result_sheet_list[case_number]
            #----
            col_moment_mx = find_column(['mx'], result_sheet, 1)[0]
            moment_mx = result_sheet.col_values(col_moment_mx)[2:]
            moment_mx = np.vectorize(unexpected_replace)(moment_mx)
            rcpanelload.moment_mx= np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mx = []
            #----
            col_moment_my = find_column(['my'], result_sheet, 1)[0]
            moment_my = result_sheet.col_values(col_moment_my)[2:]
            moment_my = np.vectorize(unexpected_replace)(moment_my)      
            rcpanelload.moment_my= np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_my = []
            #----
            col_moment_mxy = find_column(['mxy'], result_sheet, 1)[0]
            moment_mxy = result_sheet.col_values(col_moment_mxy)[2:]
            moment_mxy = np.vectorize(unexpected_replace)(moment_mxy)
            rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mxy = []
            #----
            col_force_vx = find_column(['vx'], result_sheet, 1)[0]
            force_vx = result_sheet.col_values(col_force_vx)[2:]
            force_vx = np.vectorize(unexpected_replace)(force_vx)
            rcpanelload.force_vx= np.array(force_vx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vx = []
            #----
            col_force_vy = find_column(['vy'], result_sheet, 1)[0]
            force_vy = result_sheet.col_values(col_force_vy)[2:]
            force_vy = np.vectorize(unexpected_replace)(force_vy)
            rcpanelload.force_vy= np.array(force_vy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vy = []
            #----
            col_force_nx = find_column(['nx'], result_sheet, 1)[0]
            force_nx = result_sheet.col_values(col_force_nx)[2:]
            force_nx = np.vectorize(unexpected_replace)(force_nx)
            rcpanelload.force_nx= np.array(force_nx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nx = []
            #----
            col_force_ny = find_column(['ny'], result_sheet, 1)[0]
            force_ny = result_sheet.col_values(col_force_ny)[2:]
            force_ny = np.vectorize(unexpected_replace)(force_ny)
            rcpanelload.force_ny= np.array(force_ny) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_ny = []
            #----
            col_force_nxy = find_column(['nxy'], result_sheet, 1)[0]
            force_nxy = result_sheet.col_values(col_force_nxy)[2:]
            force_nxy = np.vectorize(unexpected_replace)(force_nxy)
            rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nxy = []
            #---adding new case in load object
            rcpanelload.casename = case_name
            rcpanelload.add_loadcase()
            rcpanelload.set_activeloadcase(case_name)
        #----
        if progress:
            progress.setValue(80)
            progress.setValue(0)

    def ROBOTcsvloader(self, rcpanel, rcpanelload, progress=None):
        '''
        Example csv files format we needs to load data (EN langiage shown, PL language also posilbe)
        Names of this files is not important - what is inside is auto recognized
        
        panels.csv
        -----------------
        Panel;Thickness (in)
        1;36.00
        9;24.00
        13;24.00
        14;24.00
        (...)
        -----------------
        
        nodes.csv
        -----------------
        Node;X (ft);Y (ft);Z (ft)
        1;0.0;0.0;0.0;
        5;0.0;32.00;12.00;
        6;24.00;32.00;12.00;
        7;48.00;32.00;12.00;
        8;72.00;32.00;12.00;
        (...)
        -----------------
        
        result.csv 
        -----------------
        Panel;Node;Case;MXX (kipft/ft);MYY (kipft/ft);MXY (kipft/ft);NXX (kip/ft);NYY (kip/ft);NXY (kip/ft);QXX (kip/ft);QYY (kip/ft)
        9; 1; 201 (C);-0.42;14.28;1.62;5.57;23.76;-7.33;0.20;-6.83
        9; 1; 202 (C);-1.82;16.62;2.54;7.60;25.69;-12.81;0.37;-7.82
        9; 1; 203 (C);-1.30;15.25;2.15;6.71;23.96;-10.73;0.27;-7.15
        9; 5; 201 (C);37.04;-40.36;33.87;2.03;-485.34;221.87;-66.49;49.06
        9; 5; 202 (C);49.89;-72.65;58.95;9.07;-849.29;388.77;-110.17;85.03
        9; 5; 203 (C);45.45;-60.69;49.66;6.48;-714.65;327.04;-94.04;71.69
        9; 31; 201 (C);36.97;-39.82;-33.43;1.73;-479.13;-219.02;65.73;48.39
        9; 31; 202 (C);48.34;-69.83;-56.64;8.11;-816.61;-373.76;106.02;81.64
        9; 31; 203 (C);44.36;-58.62;-47.96;5.75;-690.51;-315.96;90.99;69.18
        (...)
        -----------------
        '''
        #----------------------------------------------------------------------
        #----deleting object data 
        rcpanel.clear_arrays_data()
        rcpanelload.clear_arrays_data()
        #----------------------------------------------------------------------
        #----loading csv files and recognizing surface, result and node sheets
        from tkinter import Tk
        from tkinter.filedialog import askopenfilenames
        surface_sheet = None
        result_sheet = None
        node_sheet = None
        tryNumber = 1
        while not (surface_sheet and result_sheet and node_sheet):
            root = Tk()
            root.withdraw()
            #----
            ask_text = 'Choose'
            if not surface_sheet:
                ask_text += ' [surface]'
            if not result_sheet:
                ask_text += ' [result]' 
            if not node_sheet:
                ask_text += ' [node]' 
            ask_text += ' csv Robot output file(s)'
            #----
            filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('csv file', '*.csv')], initialdir=self.initialdir)
            for filename in filename_list:
                if not filename == '':
                    self.initialdir = os.path.dirname(filename) 
                #----solving posiible problems in csv from robot
                with open(filename, 'r') as file :
                    filedata = file.read()
                    #----solving possible '/ ' problem in robot csv output (in force data possible)
                    filedata = filedata.replace('/ ', '; ') #replacing '/ ' on '; ' '
                    #----solving possible delimiter problem - it must be ; anyway ---------
                    filedata = filedata.replace(',', ';') #replacing ', ' on '; '
                    #----solving possible *;;;; problem at end of node file - delete it
                    filedata = filedata.replace('*;;;;\n', '') #deleting '*;;;;'
                    filedata = filedata.replace('*;;;\n', '') #deleting '*;;;'
                with open(filename, 'w') as file:
                    file.write(filedata)
                #----opening csv file with reader
                csvfile = open(filename, 'rt')
                reader = csv.reader(csvfile, delimiter=';')
                #----extrating rows to temporary list
                sheet = []
                for row in reader:
                    sheet.append(row)
                #----util function that check, is there are columns headers we looking for
                def IsInHeader(sheet, textlist):
                    answer = True
                    for text in textlist:
                        if not text in str(sheet[0]):
                            answer = False
                    return answer
                #----recognizing in case PL language inside robot export
                if IsInHeader(sheet, ['Panel', 'Grubosc']):
                    surface_sheet = sheet #<<<<<<<< surface_sheet
                if IsInHeader(sheet, ['Panel', 'Wezel', 'Przypadek', 'MXX', 'MYY', 'MXY', 'NXX', 'NYY', 'NXY', 'QXX', 'QYY']):
                    result_sheet = sheet #<<<<<<<< result_sheet
                if IsInHeader(sheet, ['Wezel', 'X', 'Y', 'Z']):
                    node_sheet = sheet #<<<<<<<< node_sheet
                #----recognizing in case EN language inside robot export
                if IsInHeader(sheet, ['Panel', 'Thickness']):
                    surface_sheet = sheet #<<<<<<<< surface_sheet
                if IsInHeader(sheet, ['Panel', 'Node', 'Case', 'MXX', 'MYY', 'MXY', 'NXX', 'NYY', 'NXY', 'QXX', 'QYY']):
                    result_sheet = sheet #<<<<<<<< result_sheet
                if IsInHeader(sheet, ['Node', 'X', 'Y', 'Z']):
                    node_sheet = sheet #<<<<<<<< node_sheet
            if tryNumber == 3: # it give user chance to select files again if not all sheets found
                return 0
            tryNumber +=1
        root.destroy()
        #----------------------------------------------------------------------
        #----util function for finding column number with some text in header
        def find_column(headerTextlist, sheet):
            find_result = None
            for i in range(len(sheet[0])):
                for text in headerTextlist:
                    if text in str(sheet[0][i]):
                        find_result = [i, str(sheet[0][i])]
            if not find_result:
                find_result = [None, None]
            return find_result
        #----------------------------------------------------------------------
        #----recognizing solver data units
        #----thickness unit
        header = find_column(['Thickness', 'Grubosc'], surface_sheet)[1]
        if 'mm' in header:
            solverunit_thickness = u.mm
        elif 'cm' in header:
            solverunit_thickness = u.cm
        elif 'm' in header:
            solverunit_thickness = u.m
        elif 'ft' in header:
            solverunit_thickness = u.ft
        elif 'in' in header:
            solverunit_thickness = u.inch
        else :
            solverunit_thickness = None        
        #----point coordinate unit   
        header = find_column(['X'], node_sheet)[1]
        if 'mm' in header:
            solverunit_coord = u.mm
        elif 'cm' in header:
            solverunit_coord = u.cm
        elif 'm' in header:
            solverunit_coord = u.m
        elif 'ft' in header:
            solverunit_coord = u.ft
        elif 'in' in header:
            solverunit_coord = u.inch
        else :
            solverunit_coord = None
        print('--------- coordinat unit ' + str(solverunit_coord))
        #----internale forces - moment unit
        header = find_column(['MXX'], result_sheet)[1]
        if '(Nm/m)' in header:
            solverunit_moment = u.Nm/u.m * u.m
        elif '(kNm/m)' in header:
            solverunit_moment = u.kNm/u.m * u.m
        elif '(kipft/ft)' in header:
            solverunit_moment = u.kipft/u.ft * u.m
        else :
            solverunit_moment = None
        print('--------- moment unit ' + str(solverunit_moment)) 
        #----internale forces - force unit
        header = find_column(['NXX'], result_sheet)[1]
        if '(N/m)' in header:
            solverunit_force = u.N/u.m * u.m
        elif '(kN/m)' in header:
            solverunit_force = u.kN/u.m * u.m
        elif '(kip/ft)' in header:
            solverunit_force = u.kip/u.ft * u.m
        else :
            solverunit_force = None
        print('--------- force unit ' + str(solverunit_force))
        #----------------------------------------------------------------------
        #----extracting loadcases to result_sheet_list
        col_case_name = find_column(['Przypadek', 'Case'], result_sheet)[0]
        case_name_list = [row[col_case_name] for row in result_sheet][1:]
        case_name_list = list(set(case_name_list))#delete duplicates
        result_sheet_list = []
        for casename in case_name_list:
            tmp = []
            tmp.append(result_sheet[0])
            for row in result_sheet:
                if row[col_case_name] == casename:
                    tmp.append(row)
            result_sheet_list.append(tmp)
        del result_sheet # finaly deleting no more needed result_sheet 
        #----------------------------------------------------------------------
        #----preparing thickness dictionary with surface number as keys
        col_surface_number = find_column(['Panel'], surface_sheet)[0]
        surface_number = [row[col_surface_number] for row in surface_sheet][1:]
        surface_number  = np.vectorize(int)(surface_number)
        col_surface_thickness = find_column(['Grubosc', 'Thickness'], surface_sheet)[0]
        surface_thickness = [row[col_surface_thickness] for row in surface_sheet][1:]
        surface_thickness = np.vectorize(float)(surface_thickness)
        surface_thickness  = np.vectorize(float)(surface_thickness)
        thicknessdict = dict(zip(surface_number, surface_thickness))
        #----------------------------------------------------------------------
        if progress:
            progress.setValue(40)
        #----------------------------------------------------------------------
        #----preparing coordinate dictionares with node number as keys
        col_node_number = find_column(['Wezel', 'Node'], node_sheet)[0]
        node_number = [row[col_node_number] for row in node_sheet][1:]
        node_number  = np.vectorize(int)(node_number)
        #----
        col_coord_x = find_column(['X'], node_sheet)[0]
        coord_x = [row[col_coord_x] for row in node_sheet][1:]
        coord_x = np.vectorize(lambda x: x.replace(',', '.'))(coord_x)
        coord_x = np.vectorize(float)(coord_x)
        #----
        col_coord_y = find_column(['Y'], node_sheet)[0]
        coord_y = [row[col_coord_y] for row in node_sheet][1:]
        coord_y = np.vectorize(lambda x: x.replace(',', '.'))(coord_y)
        coord_y = np.vectorize(float)(coord_y)        
        #----
        col_coord_z = find_column(['Z'], node_sheet)[0]
        coord_z = [row[col_coord_z] for row in node_sheet][1:]
        coord_z = np.vectorize(lambda x: x.replace(',', '.'))(coord_z)
        coord_z = np.vectorize(float)(coord_z)
        #----         
        coord_x_dict = dict(zip(node_number, coord_x))
        coord_y_dict = dict(zip(node_number, coord_y))
        coord_z_dict = dict(zip(node_number, coord_z))
        #----------------------------------------------------------------------
        #----writing panel properties in rcpanel obiect
        col_surfaceID = find_column(['Panel'], result_sheet_list[0])[0]
        rcpanel.surfaceID = [row[col_surfaceID] for row in result_sheet_list[0]][1:]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        #----
        col_nodeNum = find_column(['Wezel', 'Node'], result_sheet_list[0])[0]
        nodeNum = [row[col_nodeNum] for row in result_sheet_list[0]][1:]
        nodeNum = np.array(nodeNum)
        nodeNum  = np.vectorize(int)(nodeNum)
        rcpanel.coord_Xp = np.vectorize(lambda x: coord_x_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.coord_Yp  = np.vectorize(lambda x: coord_y_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.coord_Zp = np.vectorize(lambda x: coord_z_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.h = np.vectorize(lambda x: thicknessdict[x])(rcpanel.surfaceID) * (solverunit_thickness / rcpanel.h_unit).asNumber()
        #----------------------------------------------------------------------
        #----writing internal forces in rcpanelload obiect
        rcpanelload.clear_arrays_data() # clear data in load obiect
        for case_number in range(len(result_sheet_list)):
            #----
            caseload_sheet = result_sheet_list[case_number]
            case_name = case_name_list[case_number]
            #----
            col_moment_mx = find_column(['MXX'], caseload_sheet)[0]
            moment_mx = [row[col_moment_mx] for row in caseload_sheet][1:]
            moment_mx = np.vectorize(lambda x: x.replace(',', '.'))(moment_mx)
            moment_mx = - np.vectorize(float)(moment_mx)
            rcpanelload.moment_mx= np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mx = []
            #----
            col_moment_my = find_column(['MYY'], caseload_sheet)[0]
            moment_my = [row[col_moment_my] for row in caseload_sheet][1:]
            moment_my = np.vectorize(lambda x: x.replace(',', '.'))(moment_my)
            moment_my = - np.vectorize(float)(moment_my)
            rcpanelload.moment_my= np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_my = []
            #----
            col_moment_mxy = find_column(['MXY'], caseload_sheet)[0]
            moment_mxy = [row[col_moment_mxy] for row in caseload_sheet][1:]
            moment_mxy = np.vectorize(lambda x: x.replace(',', '.'))(moment_mxy)
            moment_mxy = np.vectorize(float)(moment_mxy)
            rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mxy = []
            #----
            col_force_vx = find_column(['QXX'], caseload_sheet)[0]
            force_vx = [row[col_force_vx] for row in caseload_sheet][1:]
            force_vx = np.vectorize(lambda x: x.replace(',', '.'))(force_vx)
            force_vx = np.vectorize(float)(force_vx)
            rcpanelload.force_vx= np.array(force_vx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vx = []
            #----
            col_force_vy = find_column(['QYY'], caseload_sheet)[0]
            force_vy = [row[col_force_vy] for row in caseload_sheet][1:]
            force_vy = np.vectorize(lambda x: x.replace(',', '.'))(force_vy)
            force_vy = np.vectorize(float)(force_vy)
            rcpanelload.force_vy= np.array(force_vy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vy = []        
            #----
            col_force_nx = find_column(['NXX'], caseload_sheet)[0]
            force_nx = [row[col_force_nx] for row in caseload_sheet][1:]
            force_nx = np.vectorize(lambda x: x.replace(',', '.'))(force_nx)
            force_nx = np.vectorize(float)(force_nx)
            rcpanelload.force_nx= np.array(force_nx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nx = []          
            #----
            col_force_ny = find_column(['NYY'], caseload_sheet)[0]
            force_ny = [row[col_force_ny] for row in caseload_sheet][1:]
            force_ny = np.vectorize(lambda x: x.replace(',', '.'))(force_ny)
            force_ny = np.vectorize(float)(force_ny)
            rcpanelload.force_ny= np.array(force_ny) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_ny = []
            #----
            col_force_nxy = find_column(['NXY'], caseload_sheet)[0]
            force_nxy = [row[col_force_nxy] for row in caseload_sheet][1:]
            force_nxy = np.vectorize(lambda x: x.replace(',', '.'))(force_nxy)
            force_nxy = np.vectorize(float)(force_nxy)
            rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nxy = []
            #---adding new case in load object
            rcpanelload.casename = case_name
            rcpanelload.add_loadcase()
            rcpanelload.set_activeloadcase(case_name)
        #----------------------------------------------------------------------
        if progress:
            progress.setValue(80)
            progress.setValue(0)

    def MECWAYloader(self, rcpanel, rcpanelload, progress=None, mode = 'csv'):
        #=========================================================
        #=========== FOR MECWAY 7 of 6 if detected ===============
        #=========================================================
        root = Tk()
        root.withdraw()
        #--object data clear
        if rcpanelload.loadcasecontainer: # if there already data in rcpanelload
            msg = 'It look like there some data already exist, what do you want to do?'
            option = easygui.choicebox(msg, 'New data option', ['Add new LoadCase', 'Clear all and crate new data'])
            if option == 'Clear all and crate new data':
                rcpanel.clear_arrays_data()
                rcpanelload.clear_arrays_data()
        else:
            rcpanel.clear_arrays_data()
            rcpanelload.clear_arrays_data()            
        #==========================================
        #--loading data
        data_sheet = None
        #----
        def IsInHeader(sheet, textlist):
            answer = True
            for text in textlist:
                if not text in sheet[0]:
                    answer = False
            return answer
        #----loading data from csv file
        if mode =='csv':
            tryNumber = 1
            while not data_sheet:
                ask_text = 'Choose Mecway data csv file'
                #----
                filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('csv file', '*.csv')], initialdir=self.initialdir)
                for filename in filename_list:
                    if not filename == '':
                        self.initialdir = os.path.dirname(filename)
                    csvfile = open(filename, 'rt')
                    reader = csv.reader(csvfile, delimiter=',')
                    #----extrating rows to temporary list
                    sheet = []
                    for row in reader:    
                        sheet.append(row)
                    #----recognizing
                    if IsInHeader(sheet, ['Moment per Length U', 'Moment per Length V']):
                        data_sheet = sheet
                    else:
                        easygui.msgbox('This is not Mecway output file', '>>>! ! ! ! ! ! ! !<<<')
                #----
                if tryNumber == 3:
                    return 0
                tryNumber +=1
            root.destroy()
        #----loading data from clipboard
        elif mode =='clipboard':
            #----geting clippoard with tkinter help
            data = root.clipboard_get()
            #----deleting not neded element from as text data
            data = data.replace("\r", '')
            #----transforming text in to 2d list
            data =  data.split('\n') #--each row
            for i in range(len(data)):#--each parameter
                tmp = data[i].split('\t')
                data[i] = tmp
            #----recognizing
            if IsInHeader(data, ['Moment per Length U', 'Moment per Length V']):
                data.pop() # there is empty list on the end and must be deleted
                data_sheet = data
            else:
                easygui.msgbox('This is not Mecway data in clipboard', '>>>! ! ! ! ! ! ! !<<<')
                return 0
        else:
            return 0
        #==========================================
        #----if it is Mecway 6 output with loadcase inside table? if yes then go to MECWAY6loader (old version)
        if IsInHeader(data_sheet, ['Load case']): #If true it probably Mecway6
            self.MECWAY6loader(rcpanel, rcpanelload, progress, mode) 
            return 0
        #==========================================
        #----function for finding column number with some text in header
        def find_column(headerTextlist, sheet):
            find_result = None
            for i in range(len(sheet[0])):
                for text in headerTextlist:
                    if text == str(sheet[0][i]):
                        find_result = [i, str(sheet[0][i])]
            if not find_result:
                find_result = ['Not found', None]
            return find_result
        #==========================================
        #--recognizing solver data units  - not posible for data from Mecway - must be defined with user help
        #----thickness unit
        solverunit_thickness = u.cm
        #----point coordinate unit  
        solverunit_coord = u.m
        #----internale forces - moment unit
        solverunit_moment = u.kNm
        #----internale forces - force unit
        solverunit_stress = u.MPa
        #==========================================
        #--asking user about data unit standard
        text = 'Default units: \n'
        text += 'thickness x ' + str(solverunit_thickness) + '\n'
        text += 'coordinate x ' + str(solverunit_coord) + '\n'
        text += 'moment x ' + str(solverunit_moment) + '\n'
        text += 'stress x ' + str(solverunit_stress) + '\n'
        input_mode = easygui.ynbox(text, 'Is this your Mecway units?')
        #----
        def choose(msg='Choose xxx', values=[1, 2, 3, 4, 5]):
            selected = easygui.choicebox(msg, 'Select unit', values)
            for i in values:
                if selected == str(i):
                    return i
        #----asking user about units if other than default
        if not input_mode:
            solverunit_thickness = choose('Choose thickness unit', [u.mm, u.cm, u.m])
            solverunit_coord = choose('Choose coordinate unit', [u.mm, u.cm, u.m])
            solverunit_moment = choose('Choose moment unit', [u.Nm, u.kNm])
            solverunit_stress = choose('Choose stress unit', [u.Pa, u.kPa, u.MPa])       
        #==========================================
        #--finding average value - two method available (1)on elements or (2)on mesh point
        #----data_sheet element format change in to float
        for i in range(1, len(data_sheet)):
            for j in range(len(data_sheet[0])):
                try:
                    data_sheet[i][j] = float (data_sheet[i][j])
                except ValueError:
                    pass
        #----temporary sheet
        tmp_sheet = []
        tmp_sheet.append(data_sheet[0]) #copy header name
        #----choice method dialog
        msg = 'Choose method for FE result values \n'
        msg += '(1)Element value - average value for fine element \n'
        msg += '(2)Point value - average value for fine mesh point'
        method = easygui.choicebox(msg, 'Select method', ['Element value', 'Point value'])
        #----average value for fine elements - option (1)
        if method == 'Element value':
            #----list with column for average value to calculate
            col_element = find_column(['Element'], data_sheet)[0]
            collist = []
            for name in [   'X','Y', 'Z',
                            'Stress UU, Midplane', 'Stress VV, Midplane','Stress UV, Midplane',
                            'Moment per Length U', 'Moment per Length V','Moment per Length UV'
                        ]:
                collist.append(find_column([name], data_sheet)[0])
            #---the loop where tmp_sheet is creating
            row = 2
            k=1        
            while row <= (len(data_sheet)-1):
                if data_sheet[row][col_element] == data_sheet[row-1][col_element]:
                    k+=1
                    for col in collist:
                        data_sheet[row-1][col] *= k-1
                        data_sheet[row][col] += data_sheet[row-1][col]
                        data_sheet[row][col] = data_sheet[row][col] / k
                else:
                    k=1
                    tmp_sheet.append(data_sheet[row-1])
                if row == len(data_sheet)-1:
                    tmp_sheet.append(data_sheet[row])
                row += 1
        #---average value for mesh point - option (2)
        if method == 'Point value':
            #sorting data_sheet by coodinate and loadcase
            col_X = find_column(['X'], data_sheet)[0]
            col_Y = find_column(['Y'], data_sheet)[0]
            col_Z = find_column(['Z'], data_sheet)[0]
            header = data_sheet.pop(0)
            #col_case_name = find_column(['Load case'], data_sheet)[0]
            data_sheet.sort(key=lambda x: [x[col_X],x[col_Y],x[col_Z]]) #by coordinate sorting
            #data_sheet.sort(key=lambda x: x[col_case_name])#by load_case sorting
            data_sheet = [header] + data_sheet
            #----list with column for average value to calculate
            
            collist = []
            for name in [   'Stress UU, Midplane', 'Stress VV, Midplane','Stress UV, Midplane',
                            'Moment per Length U', 'Moment per Length V','Moment per Length UV'
                        ]:
                collist.append(find_column([name], data_sheet)[0])
            #---the loop where tmp_sheet is creating
            row = 2
            k=1        
            while row <= (len(data_sheet)-1):
                i = data_sheet[row]#current row list
                j = data_sheet[row - 1]#previous row list
                if [i[col_X],i[col_Y],i[col_Z]] == [j[col_X],j[col_Y],j[col_Z]]:
                    k+=1
                    for col in collist:
                        data_sheet[row-1][col] *= k-1
                        data_sheet[row][col] += data_sheet[row-1][col]
                        data_sheet[row][col] = data_sheet[row][col] / k
                else:
                    k=1
                    tmp_sheet.append(data_sheet[row-1])
                if row == len(data_sheet)-1:
                    tmp_sheet.append(data_sheet[row])
                row += 1
        #---return with data to data_sheet
        data_sheet = tmp_sheet[:][:]
        del tmp_sheet # finaly deleting no more needed tmp_sheet        
        #==========================================
        #--writing panel properties in rcpanel object
        #----
        col_surfaceID = find_column(['Element'], data_sheet)[0]
        rcpanel.surfaceID = [row[col_surfaceID] for row in data_sheet][1:]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        #----
        col_coord_Xp = find_column(['X'], data_sheet)[0]
        rcpanel.coord_Xp = [row[col_coord_Xp] for row in data_sheet][1:]
        rcpanel.coord_Xp = np.array(rcpanel.coord_Xp)
        rcpanel.coord_Xp  = np.vectorize(float)(rcpanel.coord_Xp)
        #----
        col_coord_Yp = find_column(['Y'], data_sheet)[0]
        rcpanel.coord_Yp = [row[col_coord_Yp] for row in data_sheet][1:]
        rcpanel.coord_Yp = np.array(rcpanel.coord_Yp)
        rcpanel.coord_Yp  = np.vectorize(float)(rcpanel.coord_Yp) 
        #----
        col_coord_Zp = find_column(['Z'], data_sheet)[0]
        rcpanel.coord_Zp = [row[col_coord_Zp] for row in data_sheet][1:]
        rcpanel.coord_Zp = np.array(rcpanel.coord_Zp)
        rcpanel.coord_Zp  = np.vectorize(float)(rcpanel.coord_Zp) 
        #----
        col_thickness = find_column(['Material'], data_sheet)[0]
        rcpanel.h = [row[col_thickness] for row in data_sheet][1:]
        def get_num(x):
            return int(''.join(ele for ele in x if ele.isdigit()))
        rcpanel.h = np.vectorize(lambda x: get_num(x))(rcpanel.h)
        rcpanel.h  = np.vectorize(float)(rcpanel.h)
        #==========================================
        #--writing internal forces in rcpanelload object
        #----------------------------------------
        col_moment_mx = find_column(['Moment per Length U'], data_sheet)[0]
        moment_mx = [row[col_moment_mx] for row in data_sheet][1:]
        moment_mx = np.vectorize(float)(moment_mx)
        rcpanelload.moment_mx= - np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
        moment_mx = []
        #----
        col_moment_my = find_column(['Moment per Length V'], data_sheet)[0]
        moment_my = [row[col_moment_my] for row in data_sheet][1:]
        moment_my = np.vectorize(float)(moment_my)
        rcpanelload.moment_my= - np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
        moment_my = []
        #----
        col_moment_mxy = find_column(['Moment per Length UV'], data_sheet)[0]
        moment_mxy = [row[col_moment_mxy] for row in data_sheet][1:]
        moment_mxy = np.vectorize(float)(moment_mxy)
        rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
        moment_mxy = []
        #----!!!!!!!!!!!!!!! no vx in Mecway output data
        rcpanelload.force_vx= np.zeros(len(rcpanelload.moment_mxy))
        #----!!!!!!!!!!!!!!! no vx in Mecway output data
        rcpanelload.force_vy= np.zeros(len(rcpanelload.moment_mxy))
        #----
        col_force_nx = find_column(['Stress UU, Midplane'], data_sheet)[0]
        force_nx = [row[col_force_nx] for row in data_sheet][1:]
        force_nx = np.vectorize(float)(force_nx) # but this is a stress
        force_nx = force_nx * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
        rcpanelload.force_nx= np.array(force_nx) * (solverunit_stress / rcpanelload.force_unit).asNumber()
        force_nx = []          
        #----
        col_force_ny = find_column(['Stress VV, Midplane'], data_sheet)[0]
        force_ny = [row[col_force_ny] for row in data_sheet][1:] # but this is a stress
        force_ny = np.vectorize(float)(force_ny)# but this is a stress
        force_ny = force_ny * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
        rcpanelload.force_ny= np.array(force_ny) * (solverunit_stress / rcpanelload.force_unit).asNumber()
        force_ny = []
        #----
        col_force_nxy = find_column(['Stress UV, Midplane'], data_sheet)[0]
        force_nxy = [row[col_force_nxy] for row in data_sheet][1:]
        force_nxy = np.vectorize(float)(force_nxy) # but this is a stress
        force_nxy = force_nxy * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
        rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_stress / rcpanelload.force_unit).asNumber()
        force_nxy = []
        #---adding new case in load object
        randon_loadcase_name = 'LoadCase-' + uuid.uuid1().hex[:3].upper()
        user_loadcase_name = easygui.enterbox('Enter this lodcase name', 'Loadcase name', default=randon_loadcase_name) #aking user about name
        rcpanelload.casename = user_loadcase_name
        rcpanelload.add_loadcase()
        rcpanelload.set_activeloadcase(user_loadcase_name)
        #==========================================
        if progress:
            progress.setValue(80)
            progress.setValue(0)

    def MECWAY6loader(self, rcpanel, rcpanelload, progress=None, mode = 'csv'):
        #========================================
        #=========== FOR MECWAY 6 ===============
        #========================================
        root = Tk()
        root.withdraw()
        #--object data clear
        rcpanel.clear_arrays_data()
        rcpanelload.clear_arrays_data()
        #==========================================
        #--loading data
        data_sheet = None
        #----
        def IsInHeader(sheet, textlist):
            answer = True
            for text in textlist:
                if not text in sheet[0]:
                    answer = False
            return answer
        #----loading data from csv file
        if mode =='csv':
            tryNumber = 1
            while not data_sheet:
                ask_text = 'Choose Mecway6 data csv file'
                #----
                filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('csv file', '*.csv')], initialdir=self.initialdir)
                for filename in filename_list:
                    if not filename == '':
                        self.initialdir = os.path.dirname(filename)
                    csvfile = open(filename, 'rb')
                    reader = csv.reader(csvfile, delimiter=',')
                    #----extrating rows to temporary list
                    sheet = []
                    for row in reader:    
                        sheet.append(row)
                    #----recognizing
                    if IsInHeader(sheet, ['Moment per Length U', 'Load case']):
                        data_sheet = sheet
                    else:
                        easygui.msgbox('This is not Mecway output file', '>>>! ! ! ! ! ! ! !<<<')
                #----
                if tryNumber == 3:
                    return 0
                tryNumber +=1
            root.destroy()
        #----loading data from clipboard
        elif mode =='clipboard':
            #----geting clippoard with Tkinter help
            data = root.clipboard_get()
            #----deleting not neded element from as text data
            data = data.replace("\r", '')
            #----transforming text in to 2d list
            data =  data.split('\n') #--each row
            for i in range(len(data)):#--each parameter
                tmp = data[i].split('\t')
                data[i] = tmp
            #----recognizing
            if IsInHeader(data, ['Moment per Length U', 'Load case']):
                data.pop() # there is empty list on the end and must be deleted
                data_sheet = data
            else:
                easygui.msgbox('This is not Mecway data in clipboard', '>>>! ! ! ! ! ! ! !<<<')
                return 0
        else:
            return 0
        #==========================================
        #----function for finding column number with some text in header
        def find_column(headerTextlist, sheet):
            find_result = None
            for i in range(len(sheet[0])):
                for text in headerTextlist:
                    if text == str(sheet[0][i]):
                        find_result = [i, str(sheet[0][i])]
            if not find_result:
                find_result = ['Not found', None]
            return find_result
        #==========================================
        #--recognizing solver data units  - not posible for data from Mecway - must be defined with user help
        #----thickness unit
        solverunit_thickness = u.cm
        #----point coordinate unit  
        solverunit_coord = u.m
        #----internale forces - moment unit
        solverunit_moment = u.kNm
        #----internale forces - force unit
        solverunit_stress = u.MPa
        #==========================================
        #--asking user about data unit standard
        text = 'Default units: \n'
        text += 'thickness x ' + str(solverunit_thickness) + '\n'
        text += 'coordinate x ' + str(solverunit_coord) + '\n'
        text += 'moment x ' + str(solverunit_moment) + '\n'
        text += 'stress x ' + str(solverunit_stress) + '\n'
        input_mode = easygui.ynbox(text, 'Is this your Mecway units?')
        #----
        def choose(msg='Choose xxx', values=[1, 2, 3, 4, 5]):
            selected = easygui.choicebox(msg, 'Select unit', values)
            for i in values:
                if selected == str(i):
                    return i
        #----asking user about units if other than default
        if not input_mode:
            solverunit_thickness = choose('Choose thickness unit', [u.mm, u.cm, u.m])
            solverunit_coord = choose('Choose coordinate unit', [u.mm, u.cm, u.m])
            solverunit_moment = choose('Choose moment unit', [u.Nm, u.kNm])
            solverunit_stress = choose('Choose stress unit', [u.Pa, u.kPa, u.MPa])       
        #==========================================
        #--finding average value - two method available (1)on elements or (2)on mesh point
        #----data_sheet element format change in to float
        for i in range(1, len(data_sheet)):
            for j in range(len(data_sheet[0])):
                try:
                    data_sheet[i][j] = float (data_sheet[i][j])
                except ValueError:
                    pass
        #----temporary sheet
        tmp_sheet = []
        tmp_sheet.append(data_sheet[0]) #copy header name
        #----choice method dialog
        msg = 'Choose method for FE result values \n'
        msg += '(1)Element value - average value for fine element \n'
        msg += '(2)Point value - average value for fine mesh point'
        method = easygui.choicebox(msg, 'Select method', ['Element value', 'Point value'])
        #----average value for fine elements - option (1)
        if method == 'Element value':
            #----list with column for average value to calculate
            col_element = find_column(['Element'], data_sheet)[0]
            collist = []
            for name in [   'X','Y', 'Z',
                            'Stress UU, Midplane', 'Stress VV, Midplane','Stress UV, Midplane',
                            'Moment per Length U', 'Moment per Length V','Moment per Length UV'
                        ]:
                collist.append(find_column([name], data_sheet)[0])
            #---the loop where tmp_sheet is creating
            row = 2
            k=1        
            while row <= (len(data_sheet)-1):
                if data_sheet[row][col_element] == data_sheet[row-1][col_element]:
                    k+=1
                    for col in collist:
                        data_sheet[row-1][col] *= k-1
                        data_sheet[row][col] += data_sheet[row-1][col]
                        data_sheet[row][col] = data_sheet[row][col] / k
                else:
                    k=1
                    tmp_sheet.append(data_sheet[row-1])
                if row == len(data_sheet)-1:
                    tmp_sheet.append(data_sheet[row])
                row += 1
        #---average value for mesh point - option (2)
        if method == 'Point value':
            #sorting data_sheet by coodinate and loadcase
            col_X = find_column(['X'], data_sheet)[0]
            col_Y = find_column(['Y'], data_sheet)[0]
            col_Z = find_column(['Z'], data_sheet)[0]
            col_case_name = find_column(['Load case'], data_sheet)[0]
            data_sheet.sort(key=lambda x: [x[col_X],x[col_Y],x[col_Z]]) #by coordinate sorting
            data_sheet.sort(key=lambda x: x[col_case_name])#by load_case sorting
            #----list with column for average value to calculate
            collist = []
            for name in [   'Stress UU, Midplane', 'Stress VV, Midplane','Stress UV, Midplane',
                            'Moment per Length U', 'Moment per Length V','Moment per Length UV'
                        ]:
                collist.append(find_column([name], data_sheet)[0])
            #---the loop where tmp_sheet is creating
            row = 2
            k=1        
            while row <= (len(data_sheet)-1):
                i = data_sheet[row]#current row list
                j = data_sheet[row - 1]#previous row list
                if [i[col_X],i[col_Y],i[col_Z]] == [j[col_X],j[col_Y],j[col_Z]]:
                    k+=1
                    for col in collist:
                        data_sheet[row-1][col] *= k-1
                        data_sheet[row][col] += data_sheet[row-1][col]
                        data_sheet[row][col] = data_sheet[row][col] / k
                else:
                    k=1
                    tmp_sheet.append(data_sheet[row-1])
                if row == len(data_sheet)-1:
                    tmp_sheet.append(data_sheet[row])
                row += 1
        #---return with data to data_sheet
        data_sheet = tmp_sheet[:][:]
        del tmp_sheet # finaly deleting no more needed tmp_sheet
        #==========================================
        #--extracting loadcases to data_sheet_list
        col_case_name = find_column(['Load case'], data_sheet)[0]
        case_name_list = [row[col_case_name] for row in data_sheet][1:]
        case_name_list = list(set(case_name_list))#delete duplicates
        data_sheet_list = []
        for casename in case_name_list:
            tmp = []
            tmp.append(data_sheet[0])
            for row in data_sheet:
                if row[col_case_name] == casename:
                    tmp.append(row)
            data_sheet_list.append(tmp)
        del data_sheet # finaly deleting no more needed data_sheet
        #==========================================
        #--writing panel properties in rcpanel object
        #----
        col_surfaceID = find_column(['Element'], data_sheet_list[0])[0]
        rcpanel.surfaceID = [row[col_surfaceID] for row in data_sheet_list[0]][1:]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        #----
        col_coord_Xp = find_column(['X'], data_sheet_list[0])[0]
        rcpanel.coord_Xp = [row[col_coord_Xp] for row in data_sheet_list[0]][1:]
        rcpanel.coord_Xp = np.array(rcpanel.coord_Xp)
        rcpanel.coord_Xp  = np.vectorize(float)(rcpanel.coord_Xp)
        #----
        col_coord_Yp = find_column(['Y'], data_sheet_list[0])[0]
        rcpanel.coord_Yp = [row[col_coord_Yp] for row in data_sheet_list[0]][1:]
        rcpanel.coord_Yp = np.array(rcpanel.coord_Yp)
        rcpanel.coord_Yp  = np.vectorize(float)(rcpanel.coord_Yp) 
        #----
        col_coord_Zp = find_column(['Z'], data_sheet_list[0])[0]
        rcpanel.coord_Zp = [row[col_coord_Zp] for row in data_sheet_list[0]][1:]
        rcpanel.coord_Zp = np.array(rcpanel.coord_Zp)
        rcpanel.coord_Zp  = np.vectorize(float)(rcpanel.coord_Zp) 
        #----
        col_thickness = find_column(['Material'], data_sheet_list[0])[0]
        rcpanel.h = [row[col_thickness] for row in data_sheet_list[0]][1:]
        def get_num(x):
            return int(''.join(ele for ele in x if ele.isdigit()))
        rcpanel.h = np.vectorize(lambda x: get_num(x))(rcpanel.h)
        rcpanel.h  = np.vectorize(float)(rcpanel.h)
        #==========================================
        #--writing internal forces in rcpanelload object
        rcpanelload.clear_arrays_data() # clear data in load obiect
        for case_number in range(len(data_sheet_list)):
            #----
            caseload_sheet = data_sheet_list[case_number]
            case_name = case_name_list[case_number]
            #----
            col_moment_mx = find_column(['Moment per Length U'], caseload_sheet)[0]
            moment_mx = [row[col_moment_mx] for row in caseload_sheet][1:]
            moment_mx = np.vectorize(float)(moment_mx)
            rcpanelload.moment_mx= - np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mx = []
            #----
            col_moment_my = find_column(['Moment per Length V'], caseload_sheet)[0]
            moment_my = [row[col_moment_my] for row in caseload_sheet][1:]
            moment_my = np.vectorize(float)(moment_my)
            rcpanelload.moment_my= - np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_my = []
            #----
            col_moment_mxy = find_column(['Moment per Length UV'], caseload_sheet)[0]
            moment_mxy = [row[col_moment_mxy] for row in caseload_sheet][1:]
            moment_mxy = np.vectorize(float)(moment_mxy)
            rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mxy = []
            #----!!!!!!!!!!!!!!! no vx in Mecway output data
            rcpanelload.force_vx= np.zeros(len(rcpanelload.moment_mxy))
            #----!!!!!!!!!!!!!!! no vx in Mecway output data
            rcpanelload.force_vy= np.zeros(len(rcpanelload.moment_mxy))
            #----
            col_force_nx = find_column(['Stress UU, Midplane'], caseload_sheet)[0]
            force_nx = [row[col_force_nx] for row in caseload_sheet][1:]
            force_nx = np.vectorize(float)(force_nx) # but this is a stress
            force_nx = force_nx * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
            rcpanelload.force_nx= np.array(force_nx) * (solverunit_stress / rcpanelload.force_unit).asNumber()
            force_nx = []          
            #----
            col_force_ny = find_column(['Stress VV, Midplane'], caseload_sheet)[0]
            force_ny = [row[col_force_ny] for row in caseload_sheet][1:] # but this is a stress
            force_ny = np.vectorize(float)(force_ny)# but this is a stress
            force_ny = force_ny * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
            rcpanelload.force_ny= np.array(force_ny) * (solverunit_stress / rcpanelload.force_unit).asNumber()
            force_ny = []
            #----
            col_force_nxy = find_column(['Stress UV, Midplane'], caseload_sheet)[0]
            force_nxy = [row[col_force_nxy] for row in caseload_sheet][1:]
            force_nxy = np.vectorize(float)(force_nxy) # but this is a stress
            force_nxy = force_nxy * rcpanel.h * rcpanel.h_unit.asUnit(u.m).asNumber() # now is as internal force
            rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_stress / rcpanelload.force_unit).asNumber()
            force_nxy = []
            #---adding new case in load object
            rcpanelload.casename = case_name
            rcpanelload.add_loadcase()
            rcpanelload.set_activeloadcase(case_name)
        #==========================================
        if progress:
            progress.setValue(80)
            progress.setValue(0)

# Test if main
if __name__ == '__main__':
    from RcPanel import RcPanel
    from RcPanelLoad import RcPanelLoad
    from RcPanelViewer import RcPanelViewer
    panel = RcPanel()
    load = RcPanelLoad()
    loader = RcPanelDataLoader()
    viewer = RcPanelViewer()
    panel.h_unit = u.mm
    panel.coord_unit = u.m
    load.moment_unit = u.kNm
    load.force_unit = u.kN
    #loader.RFEMxlsloader(panel, load)
    #loader.ROBOTcsvloader(panel, load)
    loader.MECWAYloader(panel, load)
    viewer.assignPanelObiect(panel)
    viewer.assignPanelLoadObiect(load)
    panel.calculate_flatten_coordinates()
    panel.set_transf_matrix_for_view('Front')
    #viewer.plot_coordinates()
    #viewer.plot_thickness()
    #viewer.plot_nx()
    #print(panel.coord_Xp)
    print (load.get_loadcasenamelist())
    
    for case in load.get_loadcasenamelist():
        print('---------------------------')
        load.set_activeloadcase(case)
        print (load.casename)
        print(len(panel.coord_Xp), len(panel.h), len(load.force_nx))
        print('---------------------------')
 
    #for i in range(0, len(panel.coord_Xp)):
    #    print(i, panel.coord_Xp[i], panel.coord_Yp[i], panel.coord_Zp[i], panel.surfaceID[i], load.force_nx[i])