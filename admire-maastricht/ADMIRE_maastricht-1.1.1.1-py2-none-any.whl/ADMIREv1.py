import sys
sys.path.append('C:\\myokit\\myokit')
import myokit
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt4 import QtCore, QtGui, uic 
from os import walk
import csv 
import os

from . import Qt5file

print("ADMIRE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")

#form_class = uic.loadUiType("ADMIRE.ui")[0]                 # Load the UI
model1 = 0
data1b = 1
data1 = 1
data1_ref = 1
settingValuesforAAD = 0
 
#class MyWindowClass(QtGui.QMainWindow, form_class):
class MyWindowClass(QtWidgets.QMainWindow, Qt5file.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        #QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.statusBar()
        
        self.spinAADConcentration.valueChanged.connect(self.processAADConcentration)
        
        self.spinICaL.valueChanged.connect(self.updateSlide)
        self.spinIK1.valueChanged.connect(self.updateSlide)
        self.spinIKr.valueChanged.connect(self.updateSlide)
        self.spinIKs.valueChanged.connect(self.updateSlide)
        self.spinIf.valueChanged.connect(self.updateSlide)
        self.spinINa.valueChanged.connect(self.updateSlide)
        self.spinINaL.valueChanged.connect(self.updateSlide)
        self.spinINaK.valueChanged.connect(self.updateSlide)
        self.spinINCX.valueChanged.connect(self.updateSlide)
        self.spinIto.valueChanged.connect(self.updateSlide)
        
        self.spinAADConcentration_3.valueChanged.connect(self.processAADConcentration)
        
        self.spinICaL_2.valueChanged.connect(self.updateSlide2)
        self.spinIK1_2.valueChanged.connect(self.updateSlide2)
        self.spinIKr_2.valueChanged.connect(self.updateSlide2)
        self.spinIKs_2.valueChanged.connect(self.updateSlide2)
        self.spinIf_2.valueChanged.connect(self.updateSlide2)
        self.spinINa_2.valueChanged.connect(self.updateSlide2)
        self.spinINaL_2.valueChanged.connect(self.updateSlide2)
        self.spinINaK_2.valueChanged.connect(self.updateSlide2)
        self.spinINCX_2.valueChanged.connect(self.updateSlide2)
        self.spinIto_2.valueChanged.connect(self.updateSlide2)
        
        self.slideICaL_2.valueChanged.connect(self.updateSpin2)
        self.slideIK1_2.valueChanged.connect(self.updateSpin2)
        self.slideIKr_2.valueChanged.connect(self.updateSpin2)
        self.slideIKs_2.valueChanged.connect(self.updateSpin2)
        self.slideIf_2.valueChanged.connect(self.updateSpin2)
        self.slideINa_2.valueChanged.connect(self.updateSpin2)
        self.slideINaL_2.valueChanged.connect(self.updateSpin2)
        self.slideINaK_2.valueChanged.connect(self.updateSpin2)
        self.slideINCX_2.valueChanged.connect(self.updateSpin2)
        self.slideIto_2.valueChanged.connect(self.updateSpin2)
        
        self.cmdRun.clicked.connect(self.startSimulation)
        self.cmdReset.clicked.connect(self.resetSimulation)
        
        #self.s1s2_button.clicked.connect(self.s1s2protocol)        
        
        self.export_1.clicked.connect(self.savecsv1)     
        
        self.resetaxes_button.clicked.connect(self.resetaxes)
        
        self.cmbModel1.currentIndexChanged.connect(self.populateOutputBox)
        self.cmbOutput1Top.currentIndexChanged.connect(self.updateOutput)        
        self.cmbOutput1Bottom.currentIndexChanged.connect(self.updateOutput)                            
        
        self.xaxis_mdl1_from.valueChanged.connect(self.xaxis_adjustment1)
        self.xaxis_mdl1_to.valueChanged.connect(self.xaxis_adjustment1)
        
        self.ref_mdl1_top.stateChanged.connect(self.plotselection)
        self.aad1_mdl1_top.stateChanged.connect(self.plotselection)
        self.aad2_mdl1_top.stateChanged.connect(self.plotselection)
        self.ref_mdl1_bottom.stateChanged.connect(self.plotselection)
        self.aad1_mdl1_bottom.stateChanged.connect(self.plotselection)
        self.aad2_mdl1_bottom.stateChanged.connect(self.plotselection)        
        
        mdldirectory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'models')
        (_, _, filenames) = next(walk(mdldirectory))
        for fn in filenames:
            if fn.endswith('.mmt'):
                self.cmbModel1.addItem(fn[:(len(fn)-4)])         
		#(_, _, filenames) = walk('models/').next()
         
    def processAADConcentration(self):
        global settingValuesforAAD
        if self.sender().objectName() == 'spinAADConcentration':
            age = self.spinAADConcentration.value()
        else:
            age = self.spinAADConcentration_3.value()            
            
        blockICaL = 0
        blockIK1 = 0
        blockIKr = 0
        blockIKs = 0
        blockIf = 0
        blockINa = 0
        blockINaL = 0
        blockINaK = 0
        blockINCX = 0
        blockIto = 0
        
    def updateSlide(self):
        global settingValuesforAAD
        sending_spin = self.sender()
        
        if sending_spin.objectName() == 'spinICaL':
            self.slideICaL.setValue(sending_spin.value())
        
        if sending_spin.objectName() == 'spinIK1':
            self.slideIK1.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinIKr':
            self.slideIKr.setValue(sending_spin.value())
        
        if sending_spin.objectName() == 'spinIKs':
            self.slideIKs.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinIf':
            self.slideIf.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinINa':
            self.slideINa.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinINaL':
            self.slideINaL.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinINaK':
            self.slideINaK.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinINCX':
            self.slideINCX.setValue(sending_spin.value())

        if sending_spin.objectName() == 'spinIto':
            self.slideIto.setValue(sending_spin.value())

    def updateSlide2(self):
        global settingValuesforAAD
        sending_spin2 = self.sender()
        
        if sending_spin2.objectName() == 'spinICaL_2':
            self.slideICaL_2.setValue(sending_spin2.value())
        
        if sending_spin2.objectName() == 'spinIK1_2':
            self.slideIK1_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinIKr_2':
            self.slideIKr_2.setValue(sending_spin2.value())
        
        if sending_spin2.objectName() == 'spinIKs_2':
            self.slideIKs_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinIf_2':
            self.slideIf_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinINa_2':
            self.slideINa_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinINaL_2':
            self.slideINaL_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinINaK_2':
            self.slideINaK_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinINCX_2':
            self.slideINCX_2.setValue(sending_spin2.value())

        if sending_spin2.objectName() == 'spinIto_2':
            self.slideIto_2.setValue(sending_spin2.value())

    def updateSpin2(self):
        global settingValuesforAAD
        sending_slide2 = self.sender()
        
        if sending_slide2.objectName() == 'slideICaL_2':
            self.spinICaL_2.setValue(sending_slide2.value())
        
        if sending_slide2.objectName() == 'slideIK1_2':
            self.spinIK1_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideIKr_2':
            self.spinIKr_2.setValue(sending_slide2.value())
        
        if sending_slide2.objectName() == 'slideIKs_2':
            self.spinIKs_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideIf_2':
            self.spinIf_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideINa_2':
            self.spinINa_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideINaL_2':
            self.spinINaL_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideINaK_2':
            self.spinINaK_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideINCX_2':
            self.spinINCX_2.setValue(sending_slide2.value())

        if sending_slide2.objectName() == 'slideIto_2':
            self.spinIto_2.setValue(sending_slide2.value())
            
    def populateOutputBox(self):
        global model1
        global data1
        global data1_ref
        
        sending_cmb = self.sender()
        mdldirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        mdlname = sending_cmb.currentText() + ".mmt"
        mdlpath = mdldirectory + "\\" + mdlname
        #mdlname = "models/" + sending_cmb.currentText() + ".mmt"
        print(mdlname)
                
        if sending_cmb.objectName() == 'cmbModel1': 
            data1 = 1
            #model1, p1, s1 = myokit.load(mdlname)
            model1, p1, s1 = myokit.load(mdlpath)

            self.cmbOutput1Top.clear()
            self.cmbOutput1Bottom.clear()
            #for s in model1.states():
            #    self.cmbOutput1Top.addItem(s.qname())
            #    self.cmbOutput1Bottom.addItem(s.qname())
            
            self.startSimulation(1)
            self.ref_mdl1_top.setChecked(True)
            self.aad1_mdl1_top.setChecked(True)
            self.aad2_mdl1_top.setChecked(True)
            self.ref_mdl1_bottom.setChecked(True)
            self.aad1_mdl1_bottom.setChecked(True)
            self.aad2_mdl1_bottom.setChecked(True)            
            
            #print(data1.variable_info())
            model_vars = data1[0].variable_info()
            for items in sorted(model_vars):                
                self.cmbOutput1Top.addItem(items)
                self.cmbOutput1Bottom.addItem(items)
            
            ind_Vm_top = self.cmbOutput1Top.findText('output.Vm')
            if ind_Vm_top >= 0:
                self.cmbOutput1Top.setCurrentIndex(ind_Vm_top)
                
            ind_Cai_bottom = self.cmbOutput1Bottom.findText('output.Cai')
            if ind_Cai_bottom >= 0:
                self.cmbOutput1Bottom.setCurrentIndex(ind_Cai_bottom)            
        
    def updateOutput(self):
        global data1b        
        global data1
        global data1_ref
        global model1
        
        sending_cmb = self.sender()
        print("Sender = " + sending_cmb.objectName())
        
        if sending_cmb.currentText() != "":
        
            if sending_cmb.objectName() == 'cmbOutput1Top':
                if data1 != 1:
                    self.mplOutput1Top.axes.clear()
                    #self.mplOutput1Top.axes.hold(True)
                    for k, item in enumerate(data1):
                        cur_data1_ref = data1_ref[k]
                        cur_data1 = data1[k]
                        cur_data1b = data1b[k]
                        if self.aad1_mdl1_top.isChecked():                        
                            self.mplOutput1Top.axes.plot(cur_data1[model1.time()],cur_data1[sending_cmb.currentText()],'-r')
                        if self.aad2_mdl1_top.isChecked():                        
                            self.mplOutput1Top.axes.plot(cur_data1b[model1.time()],cur_data1b[sending_cmb.currentText()],'-b')
                        if self.ref_mdl1_top.isChecked():                        
                            self.mplOutput1Top.axes.plot(cur_data1_ref[model1.time()],cur_data1_ref[sending_cmb.currentText()],'-k')
                        self.mplOutput1Top.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
                #else:
                #    self.mplOutput1Top.axes.plot(data1_ref[model1.time()],data1_ref[sending_cmb.currentText()],'-k')
                self.mplOutput1Top.draw()

            if sending_cmb.objectName() == 'cmbOutput1Bottom':
                if data1 != 1:
                    self.mplOutput1Bottom.axes.clear()
                    #self.mplOutput1Bottom.axes.hold(True)
                    for k, item in enumerate(data1):
                        cur_data1_ref = data1_ref[k]
                        cur_data1 = data1[k]
                        cur_data1b = data1b[k]                        
                        if self.aad1_mdl1_bottom.isChecked():                        
                            self.mplOutput1Bottom.axes.plot(cur_data1[model1.time()],cur_data1[sending_cmb.currentText()],'-r')
                        if self.aad2_mdl1_bottom.isChecked():                        
                            self.mplOutput1Bottom.axes.plot(cur_data1b[model1.time()],cur_data1b[sending_cmb.currentText()],'-b')
                        if self.ref_mdl1_bottom.isChecked():                        
                            self.mplOutput1Bottom.axes.plot(cur_data1_ref[model1.time()],cur_data1_ref[sending_cmb.currentText()],'-k')
                        self.mplOutput1Bottom.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())            
                    #self.mplOutput1Bottom.axes.plot(data1[model1.time()],data1[sending_cmb.currentText()],'-r', data1b[model1.time()],data1b[sending_cmb.currentText()],'-b', data1_ref[model1.time()],data1_ref[sending_cmb.currentText()],'-k')
                #else:
                #    self.mplOutput1Bottom.axes.plot(data1_ref[model1.time()],data1_ref[sending_cmb.currentText()],'-k')
                self.mplOutput1Bottom.draw()            

    def resetSimulation(self):
        global settingValuesforAAD
        
        self.slideICaL.setSliderPosition(0)
        self.slideIK1.setSliderPosition(0)
        self.slideIKr.setSliderPosition(0)
        self.slideIKs.setSliderPosition(0)
        self.slideIf.setSliderPosition(0)
        self.slideINa.setSliderPosition(0)
        self.slideINaL.setSliderPosition(0)
        self.slideINaK.setSliderPosition(0)
        self.slideINCX.setSliderPosition(0)
        self.slideIto.setSliderPosition(0)
        
        self.spinICaL.setValue(0)
        self.spinIK1.setValue(0)
        self.spinIKr.setValue(0)
        self.spinIKs.setValue(0)
        self.spinIf.setValue(0)
        self.spinINa.setValue(0)
        self.spinINaL.setValue(0)
        self.spinINaK.setValue(0)
        self.spinINCX.setValue(0)
        self.spinIto.setValue(0)        
        
        self.slideICaL_2.setSliderPosition(0)
        self.slideIK1_2.setSliderPosition(0)
        self.slideIKr_2.setSliderPosition(0)
        self.slideIKs_2.setSliderPosition(0)
        self.slideIf_2.setSliderPosition(0)
        self.slideINa_2.setSliderPosition(0)
        self.slideINaL_2.setSliderPosition(0)
        self.slideINaK_2.setSliderPosition(0)
        self.slideINCX_2.setSliderPosition(0)
        self.slideIto_2.setSliderPosition(0)

        self.spinICaL_2.setValue(0)
        self.spinIK1_2.setValue(0)
        self.spinIKr_2.setValue(0)
        self.spinIKs_2.setValue(0)
        self.spinIf_2.setValue(0)
        self.spinINa_2.setValue(0)
        self.spinINaL_2.setValue(0)
        self.spinINaK_2.setValue(0)
        self.spinINCX_2.setValue(0)
        self.spinIto_2.setValue(0)   
        
        self.txtRateModel1.setText("60")
        self.spinStimDur1.setValue(1.0)
        self.spinStimAmp1.setValue(50)
        self.spinPrepacingModel1.setValue(100)
        self.spinShowbeatsModel1.setValue(3)
        self.stimamp.setValue(-120)
        self.I_hyper.setValue(0.0)
        
        self.spinCao1.setValue(2.00)
        self.spinKo1.setValue(4.00)
        self.spinNao1.setValue(140.00)
        
        self.xaxis_mdl1_from.setValue(0)
        self.xaxis_mdl1_to.setValue(1000) 
        
        self.spinAADConcentration.setValue(30.0)    
        self.spinAADConcentration_3.setValue(30.0)  
                
        self.ref_mdl1_top.setChecked(True)
        self.aad1_mdl1_top.setChecked(True)
        self.aad2_mdl1_top.setChecked(True)
        self.ref_mdl1_bottom.setChecked(True)
        self.aad1_mdl1_bottom.setChecked(True)
        self.aad2_mdl1_bottom.setChecked(True)
        
    def startSimulation(self, flag=3):                  # CtoF button event handler
        global model1, data1, data1_ref, data1b
        #global protocol1, protocol2
        if flag == False:
            flag = 3
            
        print("Simulation starting... flag = " + str(flag))
        progrep = MyokitProgressReporter(self.statusBar())
                
        if flag == 1 or flag == 3:
            #Extract BCLs
            bcls = self.txtRateModel1.text().split(",")
            data1_ref = []
            data1 = []
            data1b = []
            self.mplOutput1Top.axes.clear()
            self.mplOutput1Bottom.axes.clear()
            self.lblAPDCaTModel1Ctrl.setText("")
            self.lblAPDCaTModel1Alt.setText("")
            self.lblAPDCaTModel1Alt_2.setText("")
            for k, bcl_text in enumerate(bcls):             
                bcl = 1000 * 60.0 / float(bcl_text) #self.spinRateModel1.value()
                stimdur = self.spinStimDur1.value()
                stimamp = 0.01 * self.spinStimAmp1.value()
                prebeats = self.spinPrepacingModel1.value()
                showbeats = self.spinShowbeatsModel1.value()
                  
                p = myokit.Protocol()
                p.schedule(stimamp,10,stimdur,bcl,0)
                
                s = myokit.Simulation(model1, p)
                s.set_constant('parameters.Ca_o', self.spinCao1.value())
                s.set_constant('parameters.K_o', self.spinKo1.value())
                s.set_constant('parameters.Na_o', self.spinNao1.value())   

                age = 30 #self.spinAADConcentration.value()
                age_ncxb = -0.022731 * age + 0.841199
                age_sercab = 0.005793 * age + 0.532222
                age_cal_buff = -0.001973 * age + 0.283936
                age_calSR_buff = -0.007122 * age + 12.466850
                age_steep_ical = -0.154673 * age - 0.454007
                age_V_shift_ical = 0.75 * age - 42.5
                age_icalb = -0.042499 * age + 1.871332
                age_ik1b = -11.67 + (11.67)/(1+10**((67.45 - age)*(-0.03752)))                
                age_Cm = 20 + (57.17 - 20)/(1+10**((34.14 - age)*(-0.03764)))
                #age_ik1b = -0.2025 * age + 7.8
                #age_Cm = -0.6315 * age + 60.26
                age_factor_icab = 0.094065 * age + 0.841047                    
                s.set_constant("cell.Cm", age_Cm)
                s.set_constant("parameters.age_INCX_Block", age_ncxb)
                s.set_constant("parameters.JsercaB", age_sercab)
                s.set_constant("calcium.Buf_C", age_cal_buff)
                s.set_constant("calcium.Buf_SR", age_calSR_buff)
                s.set_constant("ical.steep1", age_steep_ical)
                s.set_constant("parameters.age_ICaL_Block", age_icalb)
                s.set_constant("parameters.age_IK1_Block", age_ik1b)
                s.set_constant("ical.shift_act", age_V_shift_ical)
                s.set_constant("icab.factor_icab", age_factor_icab)
                s.set_constant('membrane.stim_amplitude', self.stimamp.value())
                s.set_constant("membrane.I_hyper", self.I_hyper.value())
                
                progrep.msgvar = "Model 1 - Control Condition -"
                s.pre(prebeats*bcl, progress=progrep)
                data1_ref_temp = s.run(showbeats*bcl, progress=progrep, log=myokit.LOG_STATE+myokit.LOG_INTER+myokit.LOG_BOUND)
                data1_ref.append(data1_ref_temp)                
                apds1_ref = data1_ref_temp.apd(v='output.Vm', threshold=0.9*np.min(data1_ref_temp['output.Vm']))
                CaT_ref = np.max(data1_ref_temp['output.Cai']) - np.min(data1_ref_temp['output.Cai']) 
                #Syst_ref = np.max(data1_ref_temp['output.Cai'])                       
                #Diast_ref = np.min(data1_ref_temp['output.Cai'])
                dvdt_ref = np.diff(data1_ref_temp['output.Vm']) / np.diff(data1_ref_temp[model1.time()])
                dvdtmax_ref = np.max(dvdt_ref)     
                if len(apds1_ref['duration']) > 0:
                    self.lblAPDCaTModel1Ctrl.setText("%s\n %.1f Hz REF - APD: %d ms // dV/dt_max: %d mV/ms // CaT: %d nM" % (self.lblAPDCaTModel1Ctrl.text(), (1000/bcl), apds1_ref['duration'][0], dvdtmax_ref, 1000*CaT_ref))
                else:
                    self.lblAPDCaTModel1Ctrl.setText("%s\n %.1f Hz REF - APD: ? ms // dV/dt_max: ? mV/ms // CaT: ? nM" % (self.lblAPDCaTModel1Ctrl.text(), (1000/bcl)))  

               #mdlname = "models/" + self.cmbModel1.currentText() + ".mmt"
                #print(mdlname)
               
                #m1, p1, s1 = myokit.load(mdlname)
                s = myokit.Simulation(model1, p)
                s.set_constant('parameters.Ca_o', self.spinCao1.value())
                s.set_constant('parameters.K_o', self.spinKo1.value())
                s.set_constant('parameters.Na_o', self.spinNao1.value())            
    
                s.set_constant('parameters.ICaL_Block', self.spinICaL.value() / 100.0)
                s.set_constant('parameters.IK1_Block', self.spinIK1.value() / 100.0)
                s.set_constant('parameters.IKr_Block', self.spinIKr.value() / 100.0)
                s.set_constant('parameters.IKs_Block', self.spinIKs.value() / 100.0)
                s.set_constant('parameters.If_Block', self.spinIf.value() / 100.0)
                s.set_constant('parameters.INa_Block', self.spinINa.value() / 100.0)
                s.set_constant('parameters.INaL_Block', self.spinINaL.value() / 100.0)
                s.set_constant('parameters.INaK_Block', self.spinINaK.value() / 100.0)
                s.set_constant('parameters.INCX_Block', self.spinINCX.value() / 100.0)
                s.set_constant('parameters.Ito_Block', self.spinIto.value() / 100.0)

                age = self.spinAADConcentration.value()
                age_ncxb = -0.022731 * age + 0.841199
                age_sercab = 0.005793 * age + 0.532222
                age_cal_buff = -0.001973 * age + 0.283936
                age_calSR_buff = -0.007122 * age + 12.466850
                age_steep_ical = -0.154673 * age - 0.454007
                age_V_shift_ical = 0.75 * age - 42.5
                age_icalb = -0.042499 * age + 1.871332
                age_ik1b = -11.67 + (11.67)/(1+10**((67.45 - age)*(-0.03752)))                
                age_Cm = 20 + (57.17 - 20)/(1+10**((34.14 - age)*(-0.03764)))                
                #age_ik1b = -0.2025 * age + 7.8
                #age_Cm = -0.6315 * age + 60.26
                age_factor_icab = 0.094065 * age + 0.841047   
                s.set_constant("cell.Cm", age_Cm)
                s.set_constant("parameters.age_INCX_Block", age_ncxb)
                s.set_constant("parameters.JsercaB", age_sercab)
                s.set_constant("calcium.Buf_C", age_cal_buff)
                s.set_constant("calcium.Buf_SR", age_calSR_buff)
                s.set_constant("ical.steep1", age_steep_ical)
                s.set_constant("parameters.age_ICaL_Block", age_icalb)
                s.set_constant("parameters.age_IK1_Block", age_ik1b)
                s.set_constant("ical.shift_act", age_V_shift_ical)
                s.set_constant("icab.factor_icab", age_factor_icab)
                s.set_constant('membrane.stim_amplitude', self.stimamp.value())  
                s.set_constant("membrane.I_hyper", self.I_hyper.value())
                                        
                progrep.msgvar = "- Cell 1 -"
                s.pre(prebeats*bcl, progress=progrep)
                data1_temp = s.run(showbeats*bcl, progress=progrep, log=myokit.LOG_STATE+myokit.LOG_INTER+myokit.LOG_BOUND)
                data1.append(data1_temp)               
                apds1_alt = data1_temp.apd(v='output.Vm', threshold=0.9*np.min(data1_temp['output.Vm']))
                CaT_alt = np.max(data1_temp['output.Cai']) - np.min(data1_temp['output.Cai']) 
                #Syst_alt = np.max(data1_temp['output.Cai'])                       
                #Diast_alt = np.min(data1_temp['output.Cai'])   
                dvdt_alt = np.diff(data1_temp['output.Vm']) / np.diff(data1_temp[model1.time()])
                dvdtmax_alt = np.max(dvdt_alt)                               
                #self.lblAPDCaTModel2Alt.setText('APD: ' + str(apds2_alt[0]) + ' ms / CaT: ' + str(CaT_alt) + ' uM')
                if len(apds1_alt['duration']) > 0:
                    self.lblAPDCaTModel1Alt.setText("%s\n %.1f Hz Cell 1 - APD: %d ms // dV/dt_max: %d mV/ms // CaT: %d nM" % (self.lblAPDCaTModel1Alt.text(), (1000/bcl), apds1_alt['duration'][0], dvdtmax_alt, 1000*CaT_alt))
                else:
                    self.lblAPDCaTModel1Alt.setText("%s\n %.1f Hz Cell 1 - APD: ? ms // dV/dt_max: ? mV/ms // CaT: ? nM" % (self.lblAPDCaTModel1Alt.text(), (1000/bcl)))            
                
                        
                s = myokit.Simulation(model1, p)
                s.set_constant('parameters.Ca_o', self.spinCao1.value())
                s.set_constant('parameters.K_o', self.spinKo1.value())
                s.set_constant('parameters.Na_o', self.spinNao1.value())            
    
                s.set_constant('parameters.ICaL_Block', self.spinICaL_2.value() / 100.0)
                s.set_constant('parameters.IK1_Block', self.spinIK1_2.value() / 100.0)
                s.set_constant('parameters.IKr_Block', self.spinIKr_2.value() / 100.0)
                s.set_constant('parameters.IKs_Block', self.spinIKs_2.value() / 100.0)
                s.set_constant('parameters.If_Block', self.spinIf_2.value() / 100.0)
                s.set_constant('parameters.INa_Block', self.spinINa_2.value() / 100.0)
                s.set_constant('parameters.INaL_Block', self.spinINaL_2.value() / 100.0)
                s.set_constant('parameters.INaK_Block', self.spinINaK_2.value() / 100.0)
                s.set_constant('parameters.INCX_Block', self.spinINCX_2.value() / 100.0)
                s.set_constant('parameters.Ito_Block', self.spinIto_2.value() / 100.0)

                age = self.spinAADConcentration_3.value()
                age_ncxb = -0.022731 * age + 0.841199
                age_sercab = 0.005793 * age + 0.532222
                age_cal_buff = -0.001973 * age + 0.283936
                age_calSR_buff = -0.007122 * age + 12.466850
                age_steep_ical = -0.154673 * age - 0.454007
                age_V_shift_ical = 0.75 * age - 42.5
                age_icalb = -0.042499 * age + 1.871332
                age_ik1b = -11.67 + (11.67)/(1+10**((67.45 - age)*(-0.03752)))                
                age_Cm = 20 + (57.17 - 20)/(1+10**((34.14 - age)*(-0.03764)))                
                #age_ik1b = -0.2025 * age + 7.8
                #age_Cm = -0.6315 * age + 60.26
                age_factor_icab = 0.094065 * age + 0.841047  
                s.set_constant("cell.Cm", age_Cm)
                s.set_constant("parameters.age_INCX_Block", age_ncxb)
                s.set_constant("parameters.JsercaB", age_sercab)
                s.set_constant("calcium.Buf_C", age_cal_buff)
                s.set_constant("calcium.Buf_SR", age_calSR_buff)
                s.set_constant("ical.steep1", age_steep_ical)
                s.set_constant("parameters.age_ICaL_Block", age_icalb)
                s.set_constant("parameters.age_IK1_Block", age_ik1b)
                s.set_constant("ical.shift_act", age_V_shift_ical)
                s.set_constant("icab.factor_icab", age_factor_icab)
                s.set_constant('membrane.stim_amplitude', self.stimamp.value())  
                s.set_constant("membrane.I_hyper", self.I_hyper.value())
                
                progrep.msgvar = "- Cell 2 -"
                s.pre(prebeats*bcl, progress=progrep)
                data1b_temp = s.run(showbeats*bcl, progress=progrep, log=myokit.LOG_STATE+myokit.LOG_INTER+myokit.LOG_BOUND)
                data1b.append(data1b_temp)                
                apds1b_alt = data1b_temp.apd(v='output.Vm', threshold=0.9*np.min(data1b_temp['output.Vm']))
                CaTb_alt = np.max(data1b_temp['output.Cai']) - np.min(data1b_temp['output.Cai']) 
                #Systb_alt = np.max(data1b_temp['output.Cai'])                       
                #Diastb_alt = np.min(data1b_temp['output.Cai'])                         
                dvdtb_alt = np.diff(data1b_temp['output.Vm']) / np.diff(data1b_temp[model1.time()])
                dvdtmaxb_alt = np.max(dvdtb_alt)                                   
                #self.lblAPDCaTModel2Alt.setText('APD: ' + str(apds2_alt[0]) + ' ms / CaT: ' + str(CaT_alt) + ' uM')
                if len(apds1b_alt['duration']) > 0:
                    self.lblAPDCaTModel1Alt_2.setText("%s\n %.1f Hz Cell 2 - APD: %d ms // dV/dt_max: %d mV/ms // CaT: %d nM" % (self.lblAPDCaTModel1Alt_2.text(), (1000/bcl), apds1b_alt['duration'][0], dvdtmaxb_alt, 1000*CaTb_alt))
                else:
                    self.lblAPDCaTModel1Alt_2.setText("%s\n %.1f Hz Cell 2 - APD: ? ms // dV/dt_max: ? mV/ms // CaT: ? nM" % (self.lblAPDCaTModel1Alt_2.text(), (1000/bcl)))            
                               
            if len(self.cmbOutput1Top.currentText()) > 1:
                #self.mplOutput1Top.axes.hold(True)
                #self.mplOutput1Bottom.axes.hold(True)
                for k, item in enumerate(data1):
                    data1_temp = data1[k]
                    data1b_temp = data1b[k]
                    data1_ref_temp = data1_ref[k] 
                    if self.aad1_mdl1_top.isChecked():
                        self.mplOutput1Top.axes.plot(data1_temp[model1.time()],data1_temp[self.cmbOutput1Top.currentText()],'-r')
                    if self.aad2_mdl1_top.isChecked():
                        self.mplOutput1Top.axes.plot(data1b_temp[model1.time()],data1b_temp[self.cmbOutput1Top.currentText()],'-b')
                    if self.ref_mdl1_top.isChecked():
                        self.mplOutput1Top.axes.plot(data1_ref_temp[model1.time()],data1_ref_temp[self.cmbOutput1Top.currentText()],'-k')
                    if self.aad1_mdl1_bottom.isChecked():
                        self.mplOutput1Bottom.axes.plot(data1_temp[model1.time()],data1_temp[self.cmbOutput1Bottom.currentText()],'-r')
                    if self.aad2_mdl1_bottom.isChecked():
                        self.mplOutput1Bottom.axes.plot(data1b_temp[model1.time()],data1b_temp[self.cmbOutput1Bottom.currentText()],'-b')
                    if self.ref_mdl1_bottom.isChecked():
                        self.mplOutput1Bottom.axes.plot(data1_ref_temp[model1.time()],data1_ref_temp[self.cmbOutput1Bottom.currentText()],'-k')
                self.mplOutput1Top.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
                self.mplOutput1Bottom.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
                self.mplOutput1Top.draw()                
                self.mplOutput1Bottom.draw()
    
    def plotselection(self):
        global data1_ref, data1, data1b
        
        if len(self.cmbOutput1Top.currentText()) > 1:
            self.mplOutput1Top.axes.clear()
            self.mplOutput1Bottom.axes.clear()          
            #self.mplOutput1Top.axes.hold(True)
            #self.mplOutput1Bottom.axes.hold(True)
            for k, item in enumerate(data1):
                data1_temp = data1[k]
                data1b_temp = data1b[k]
                data1_ref_temp = data1_ref[k] 
                if self.aad1_mdl1_top.isChecked():
                    self.mplOutput1Top.axes.plot(data1_temp[model1.time()],data1_temp[self.cmbOutput1Top.currentText()],'-r')
                if self.aad2_mdl1_top.isChecked():
                    self.mplOutput1Top.axes.plot(data1b_temp[model1.time()],data1b_temp[self.cmbOutput1Top.currentText()],'-b')
                if self.ref_mdl1_top.isChecked():
                    self.mplOutput1Top.axes.plot(data1_ref_temp[model1.time()],data1_ref_temp[self.cmbOutput1Top.currentText()],'-k')
                if self.aad1_mdl1_bottom.isChecked():
                    self.mplOutput1Bottom.axes.plot(data1_temp[model1.time()],data1_temp[self.cmbOutput1Bottom.currentText()],'-r')
                if self.aad2_mdl1_bottom.isChecked():
                    self.mplOutput1Bottom.axes.plot(data1b_temp[model1.time()],data1b_temp[self.cmbOutput1Bottom.currentText()],'-b')
                if self.ref_mdl1_bottom.isChecked():
                    self.mplOutput1Bottom.axes.plot(data1_ref_temp[model1.time()],data1_ref_temp[self.cmbOutput1Bottom.currentText()],'-k')
            self.mplOutput1Top.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
            self.mplOutput1Bottom.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
            self.mplOutput1Top.draw()                
            self.mplOutput1Bottom.draw()        

    def xaxis_adjustment1(self): 
        self.mplOutput1Top.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
        self.mplOutput1Top.draw()
        self.mplOutput1Bottom.axes.set_xlim(self.xaxis_mdl1_from.value(), self.xaxis_mdl1_to.value())
        self.mplOutput1Bottom.draw()
            
    def resetaxes(self):
        self.xaxis_mdl1_from.setValue(0)
        self.xaxis_mdl1_to.setValue(1000)
            
    def savecsv1(self):
        global model1, data1, data1_ref, data1b

        export_mdl1 = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', "CSV (*.csv);;Text (*.txt);;All Files (*.*)")
        main1 = export_mdl1[0][:-4]
        ext1 = export_mdl1[0][-4:]
        export_mdl1_top = ''.join(main1)+("_Top")+''.join(ext1)
        
        with open(export_mdl1_top,'wb') as f1_top:
            for k, item in enumerate(data1):
                #print k
                data1_temp = data1[k]
                data1b_temp = data1b[k]
                data1_ref_temp = data1_ref[k] 
                max_length = np.max([len(data1_ref_temp[model1.time()]),len(data1_temp[model1.time()]),len(data1b_temp[model1.time()])])
                time1_ref_temp = np.concatenate((data1_ref_temp[model1.time()], np.zeros(max_length-len(data1_ref_temp[model1.time()])+1)))
                time1_temp = np.concatenate((data1_temp[model1.time()], np.zeros(max_length-len(data1_temp[model1.time()])+1)))
                time1b_temp = np.concatenate((data1b_temp[model1.time()], np.zeros(max_length-len(data1b_temp[model1.time()])+1)))
                val1_ref_temp = np.concatenate((data1_ref_temp[self.cmbOutput1Top.currentText()], np.zeros(max_length-len(data1_ref_temp[self.cmbOutput1Top.currentText()])+1)))
                val1_temp = np.concatenate((data1_temp[self.cmbOutput1Top.currentText()], np.zeros(max_length-len(data1_temp[self.cmbOutput1Top.currentText()])+1)))
                val1b_temp = np.concatenate((data1b_temp[self.cmbOutput1Top.currentText()], np.zeros(max_length-len(data1b_temp[self.cmbOutput1Top.currentText()])+1)))
                np.savetxt(f1_top, np.c_[time1_ref_temp, val1_ref_temp, time1_temp, val1_temp, time1b_temp, val1b_temp], delimiter=',', footer='\n\n')
               
                #np.savetxt(f1_top, np.c_[data1_ref_temp[model1.time()], data1_ref_temp[self.cmbOutput1Top.currentText()], data1_temp[self.cmbOutput1Top.currentText()], data1b_temp[self.cmbOutput1Top.currentText()]], delimiter=',')

        export_mdl1_bottom = ''.join(main1)+("_Bottom")+''.join(ext1)
       
        with open(export_mdl1_bottom,'wb') as f1_bottom:
            for k, item in enumerate(data1):
                data1_temp = data1[k]
                data1b_temp = data1b[k]
                data1_ref_temp = data1_ref[k] 
                max_length = np.max([len(data1_ref_temp[model1.time()]),len(data1_temp[model1.time()]),len(data1b_temp[model1.time()])])
                time1_ref_temp = np.concatenate((data1_ref_temp[model1.time()], np.zeros(max_length-len(data1_ref_temp[model1.time()])+1)))
                time1_temp = np.concatenate((data1_temp[model1.time()], np.zeros(max_length-len(data1_temp[model1.time()])+1)))
                time1b_temp = np.concatenate((data1b_temp[model1.time()], np.zeros(max_length-len(data1b_temp[model1.time()])+1)))
                val1_ref_temp = np.concatenate((data1_ref_temp[self.cmbOutput1Bottom.currentText()], np.zeros(max_length-len(data1_ref_temp[self.cmbOutput1Bottom.currentText()])+1)))
                val1_temp = np.concatenate((data1_temp[self.cmbOutput1Bottom.currentText()], np.zeros(max_length-len(data1_temp[self.cmbOutput1Bottom.currentText()])+1)))
                val1b_temp = np.concatenate((data1b_temp[self.cmbOutput1Bottom.currentText()], np.zeros(max_length-len(data1b_temp[self.cmbOutput1Bottom.currentText()])+1)))
                np.savetxt(f1_bottom, np.c_[time1_ref_temp, val1_ref_temp, time1_temp, val1_temp, time1b_temp, val1b_temp], delimiter=',', footer='\n\n')
    
                #np.savetxt(f1_bottom, np.c_[data1_ref_temp[model1.time()], data1_ref_temp[self.cmbOutput1Bottom.currentText()], data1_temp[self.cmbOutput1Bottom.currentText()], data1b_temp[self.cmbOutput1Bottom.currentText()]], delimiter=',')
    
class MyokitProgressReporter(myokit.ProgressReporter):
    target = None
    msgvar = None
    def __init__(self, tar=None):
        self.target = tar
        
    def enter(self, msg=None):        
        print("Starting sim...")

    def exit(self):
        #self.target.clearMessage()
        print("Done!")
    
    def update(self, progress):
        val = progress * 100.0
        #print("Progress = " + str(progress))
        #self.target.setValue(int(val))
        self.target.showMessage(self.msgvar + " Progress: " + str(val) + "%", 2000);
        
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
        #QtGui.QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
        return True
        
def run():
    app = QtWidgets.QApplication(sys.argv)
    #app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()

run()