from __future__ import division

from pioneer.common import clouds, calibration
from pioneer.common import banks as utils
from pioneer.common.logging_manager import LoggingManager
from pioneer.common.gui import Array, BVH, Product, Transforms

import time
import warnings
try:
    import leddar
except:
    LoggingManager.instance().warning("Could not import 'leddar', no live sensor can be used!")

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, pyqtProperty as Property, Q_ENUMS, QVariant, QObject

import glob
import numpy as np
import os
import pickle
import traceback

class SensorCapture( Product.VariantProduct):
    def __init__(self, parent = None):
        super(SensorCapture, self).__init__(parent)

        self._traces = Product.VariantProduct()
        self._traces.set_producer(self)

        self._calibration = ""
        self._calibration_data = None
        self._specs = None
        self._nChannels = 0

    def calibration_cb(self):
        try:
            with open(self._calibration, 'rb') as f:
                self._calibration_data = pickle.load(f, encoding='latin1')
            self._handle_specs_changed()
        except:
            print(traceback.format_exc())
            self._calibration_data = None

    Product.InputProperty(vars(), str, 'calibration', calibration_cb)


    def _handle_specs_changed(self):
        if not self._specs:
            return

        if self._calibration_data is not None and 'fov' in self._calibration_data:
            self._specs['v_fov'], self._specs['h_fov'] = self._calibration_data['fov']

        self.set_nChannels(self, self._specs['v'] * self._specs['h'])
        self.specsChanged.emit()
    '''
        \note: LiveCapture gets its specs from the sensor.
        Manually setting specs can be used to override sensor specs
    '''
    Product.InputProperty(vars(), QVariant, 'specs', _handle_specs_changed)

    Product.ConstProperty(vars(), Product.VariantProduct, 'traces')

    Product.ROProperty(vars(), int, 'nChannels')

    def _update_with_last_received(self, last_received):

        self._variant = last_received

        if self._calibration_data is not None:
            self._variant['data'] = np.copy(last_received['data']) # we want to keep last_received intact, especially for the 'replay' use case
            self._variant['data']['distances'] -= self._calibration_data['offsets'][self._variant['data']['indices']]

    def _update_traces_with_last_recieved(self, last_traces):
        self._traces._variant = last_traces


class TracesMode(QObject):
    NONE, RAW, PROCESSED = range(3)
class TriggerMode(QObject):
    NONE, SHORT, LONG = [0x00, 0x10, 0x30]
class LiveCapture( SensorCapture ):
    def __init__(self, parent = None):
        super(LiveCapture, self).__init__(parent)
        self._dev = None
        self._ip = ""
        self._oversampling = -1
        self._accumulation = -1
        self._basePoints = -1
        self._tracesROI = [0,1] #offset, count

        self._rejectedFalgs = [0, 3, 4, 9, 3072]  
        


        self._received_echoes = []
        self._n_received = 0
        self._received_traces_raw = []
        self._received_traces_proc = []
        self._received_states = []
        self._running = False
        self._locked = False
        self._tracesMode = TracesMode.NONE
        self._delay = 5000
        self._nDroppedPackages = 0
        self._ts_prev = None
        self._triggerMode = TriggerMode.LONG
        self._lcpgIndex = 0x08
        self._overriden_specs = False
        self._connected = False
        self._emitConnectedChanged = False
        self._properties = list(leddar.property_ids.keys())
        self._calibrating = False
        self._restoringCal = False
        self._calibration_samples = []
        self._calibration_states_samples = []
        self._n_calibration_samples = 100
        self._n_drop_calib_samples = 5
        self._calibrationProgress = 0.0
        self._calibration_wall_distance = 2.0
        self._interpCal = False
        self._dTCorrection = False
        self._dTGainFactor = 0.00489
        self._dTFix = 0.0
        self._aTCorrection = False
        self._aTGainFactor = 0.01521
        self._aTThreshold = 20.0
        self._editingResoSpecs = False
        self._resoSpecsMode = ""
        self._resoSpecsVal = 0





        if not os.path.exists('calib_results/'):
            os.makedirs('calib_results/')
        if not os.path.exists('rcalibration/'):
            os.makedirs('rcalibration/')
        if not os.path.exists('angles_table/'):
            os.makedirs('angles_table/')
        


        self._listFilesRCal = [os.path.basename(x) for x in glob.glob('rcalibration/' + '*.pkl')]
        self._listFilesCustomVAngles = [os.path.basename(x) for x in glob.glob('angles_table/' + '*.txt')]
        self._vtabanglesCorrection = False

        self._scalevangles = 1.0456

        self._savingcalibinto = "calibration.pkl"
        
 

        

    def _disconnect_device(self):
        if self._dev is not None and self._connected:
            self._dev.disconnect()
            self._dev = None
            if not self._overriden_specs:
                self._specs = None

    def _update_traces_roi(self):
        if self._dev is not None and self._connected:
            self._dev.set_traces_to_receive(int(self._tracesROI[0]), int(self._tracesROI[1]))

    TracesMode = TracesMode
    Q_ENUMS(TracesMode)

    def _update_traces_mode(self):
        if self._dev is None or not self._connected:
            return

        try:

            self._update_traces_roi()

            if self._tracesMode == TracesMode.PROCESSED:
                def proc_trace_callback(new_traces):
                    if not self._locked:
                        self._received_traces_proc.append(new_traces)
                        self.makeDirty()

                self._dev.set_data_mask(self._dev.get_data_mask() | leddar.data_masks["PDM_PROCESSED_TRACES"])
                self._dev.set_callback_processed_trace(proc_trace_callback)
            else: 
                self._dev.set_data_mask(self._dev.get_data_mask() & ~leddar.data_masks["PDM_PROCESSED_TRACES"])

            if self._tracesMode == TracesMode.RAW:
                def raw_trace_callback(new_traces):
                    if not self._locked:
                        self._received_traces_raw.append(new_traces)
                        self.makeDirty()

                self._dev.set_data_mask(self._dev.get_data_mask() | leddar.data_masks["PDM_RAW_TRACES"])
                self._dev.set_callback_raw_trace(raw_trace_callback)
            else:
                self._dev.set_data_mask(self._dev.get_data_mask() & ~leddar.data_masks["PDM_RAW_TRACES"])
        except:
            traceback.print_exc()
        

    Product.InputProperty(vars(), int, 'tracesMode', _update_traces_mode)

    Product.InputProperty(vars(), QVariant, 'tracesROI', _update_traces_roi)

    Product.InputProperty(vars(), QVariant, 'rejectedFlags')

    Product.InputProperty(vars(), str, 'ip', _disconnect_device)

    def _update_data_thread(self):
        if self._dev is None or not self._connected:
            return

        self._dev.set_data_thread_delay(self._delay)

        if self._running:
            self._dev.start_data_thread()
        else:
            self._dev.stop_data_thread()

    Product.InputProperty(vars(), bool, 'running', _update_data_thread)

    Product.InputProperty(vars(), int, 'delay', _update_data_thread)

    Product.ROProperty(vars(), int, 'nDroppedPackages')

    Product.ROProperty(vars(), bool, 'connected')

    Product.ROProperty(vars(), float, 'fps')

    Product.ConstProperty(vars(), list, 'properties')

    Product.ROProperty(vars(), QVariant, 'states')
    
    Product.ROProperty(vars(), bool, 'calibrating')

    Product.ROProperty(vars(), float, 'calibrationProgress')

    Product.InputProperty(vars(), bool, 'interpCal')

    Product.InputProperty(vars(), bool, 'dTCorrection')

    Product.InputProperty(vars(), float, 'dTFix')

    Product.InputProperty(vars(), float, 'dTGainFactor')

    Product.InputProperty(vars(), bool, 'aTCorrection')

    Product.InputProperty(vars(), float, 'aTGainFactor')

    Product.InputProperty(vars(), float, 'aTThreshold')

    Product.ROProperty(vars(), bool, 'editingResoSpecs')

    Product.ROProperty(vars(), float, 'resoSpecsVal')

    Product.ROProperty(vars(), bool, 'restoringCal')

    Product.ROProperty(vars(),list, 'listFilesRCal')

    Product.ROProperty(vars(),list, 'listFilesCustomVAngles')

    Product.InputProperty(vars(), bool, 'vtabanglesCorrection')

    Product.InputProperty(vars(), float, 'scalevangles')

    Product.InputProperty(vars(), str, 'savingcalibinto')






    @Slot(int, int, int, result = bool)
    def writeMemory(self, zone, address, value):
        self._dev.write_memory(zone, address, np.array([value], np.uint16))

    @Slot(int, int, int, result = str)
    def readMemory(self, zone, address, n_bytes):
        return str(np.array(self._dev.read_memory(zone, address, n_bytes), np.uint8).tolist())

    @Slot(float, int, result = bool)
    def calibrate(self, wall_distance, n_samples):
        if self._dev and self._connected:
            self._dev.set_calib_values(leddar.calib_types['ID_TIMEBASE_DELAY'], [0.0] * self._nChannels)
            self._calibration_wall_distance = wall_distance
            self._n_calibration_samples = n_samples
            self._calibration_samples = []
            self._calibration_states_samples = []
            self._received_echoes = []
            self.set_calibrating(self, True)
            self.set_calibrationProgress(self, 0.0)
            self.set_restoringCal(self, False)
            
            return True
        return False
    

    @Slot(str, result = bool)
    def restoreCalibration(self, spath_to = "rcalibration/calibration.pkl"):
        if self._dev and self._connected:
            self.set_restoringCal(self, True)
            self._dev.set_calib_values(leddar.calib_types['ID_TIMEBASE_DELAY'],[0.0] * self._nChannels)
            data = pickle.load(open(spath_to, 'rb'))

            self._specs['v'] =  data['v']
            self._specs['h'] = data['h']
            self._specs['v_fov'] = data['v_fov']
            self._specs['h_fov'] = data['h_fov']
            if 'angles' in data:
                self._specs['angles'] = data['data']
                self.scalevangles = data['scaling_angles']
            
            self.dTGainFactor = data['dT_slope']
            self.dTFix = data['dT_ref']
            self.aTGainFactor = data['aT_slope']
            self.aTThreshold = data['aT_threshold']
            self._dev.set_calib_values(leddar.calib_types['ID_TIMEBASE_DELAY'], data['offsets'])
            super(LiveCapture, self)._handle_specs_changed()

            
            return True
        return False

    
    @Slot(str, result = bool)
    def editResoSpecs(self, mode):
        if mode == "NONE":
            self.set_editingResoSpecs(self, False)
            self.set_resoSpecsVal(self,0)

        else:
            self.set_editingResoSpecs(self, True)
            self._resoSpecsMode = mode
            self.set_resoSpecsVal(self,self._specs[mode])
        return True
    
    @Slot(float, result = bool)
    def changeResoSpecs(self, new_value):
        if self._resoSpecsMode == "h_fov" or self._resoSpecsMode == "v_fov":
            self._specs[self._resoSpecsMode] = new_value
        elif self._resoSpecsMode == "h" or self._resoSpecsMode == "v":
            self._specs[self._resoSpecsMode] = int(new_value)
        super(LiveCapture, self)._handle_specs_changed()
        return True
    
    @Slot(str, result = bool)
    def changeAnglesSpecs(self, filename):
        c_filename = 'angles_table/' + filename
        self._specs['angles'] = clouds.custom_v_angles(self._specs, factor=self._scalevangles, filename=c_filename,  dtype = np.float32)

        self._specs['v_fov'] =  np.rad2deg(np.max(self._specs['angles'][:,0]) - np.min(self._specs['angles'][:,0]))
        
        super(LiveCapture, self)._handle_specs_changed()

        return True
        
    
    

    @Slot(str, result = bool)
    def changeIP(self, ip_string):
        if self._dev and self._connected:
            try:
                rv = self._dev.set_IP_config(False, ip_string)
                print(f"ip changed to {self._dev.get_IP_config()}, you need to reboot your device!")
                return rv
            except:
                traceback.print_exc()
                return False

    @Slot(str, QVariant, result = bool)
    def setLeddarProperty(self, name, value):
        if self._dev and self._connected:
            try:
                rv = self._dev.set_property_value(name, str(value))
                self.connectedChanged.emit()
                return rv
            except:
                traceback.print_exc()
                return False
    
    @Slot(str, result = QVariant)
    def getLeddarProperty(self, name):
        if self._dev and self._connected:
            try:
                return self._dev.get_property_value(name)
            except:
                traceback.print_exc()
                return False
        return None

    @Slot(str, result = QVariant)
    def getPropertyAvailableValues(self, name):
        if self._dev and self._connected:
            try:
                rv = self._dev.get_property_available_values(name)
                string_value = self._dev.get_property_value(name)
                if isinstance(rv, dict):
                    if rv['type'] in ['list', 'bitfield']:
                        rv['current'] = string_value
                    return rv
                else:
                    return {'type': 'list', 'data': [current], 'current': current}
            except:
                pass
        return None

    def _update(self):

        if not self._running:
            return

        if self._dev is None or not self._connected:

            self._dev = leddar.Device()

            if not self._dev.connect(self._ip):
                self._connected = False
                self.connectedChanged.emit()
                self._dev = None
                return

            self._connected = True
            self.connectedChanged.emit()
            self._emitConnectedChanged = True

            if self._specs is None:
                self._specs = utils.get_specs(self._dev)
            else:
                self._overriden_specs = True

            self._handle_specs_changed()

            def echo_callback(new_echoes):
                if not self._locked:
                    self._received_echoes.append(new_echoes)
                    self.makeDirty()

            self._dev.set_callback_echo(echo_callback)
            self._dev.set_data_mask(leddar.data_masks["PDM_ECHOES"])

            def state_callback(new_state):
                if not self._locked:
                    self._received_states.append(new_state)
                    self.makeDirty()

            self._dev.set_callback_state(state_callback)
            self._dev.set_data_mask(self._dev.get_data_mask() | leddar.data_masks["PDM_STATES"])

            self._update_traces_mode()

            self._update_data_thread()

            self._n_received = 0


        if self._received_echoes:
            self._n_received += 1
            self._locked = True
            self._nDroppedPackages = len(self._received_echoes) - 1
            last_received = self._received_echoes[-1]
            last_received['data'] = last_received['data'][np.isin(last_received['data']['flags'], self._rejectedFalgs, invert = True)]

            
            if self._calibrating:
                self._calibration_samples.append(last_received)
            else:
                if (self._dTCorrection) and (self._states is not None):
                    T = self._states['system_temp']
                    last_received = calibration.distance_correction_temperature(last_received, T, self._dTGainFactor, self._dTFix)
                
                if (self._aTCorrection) and (self._states is not None):
                    T = self._states['system_temp']
                    last_received = calibration.amplitude_correction_temperature(last_received, T, self._aTGainFactor, self._aTThreshold)
                

            
            self._received_echoes = []
            self._locked = False
            self.nDroppedPackagesChanged.emit()
            if self._ts_prev is None:
                self._ts_prev = time.time()

            ts = time.time()#last_received['timestamp']
            if self._n_received%10 == 0:
                self._fps = 10 /(ts - self._ts_prev)
                self.fpsChanged.emit()
                self._ts_prev = ts

            if self._emitConnectedChanged: #important for those watching properties. properties seem only valid after the first echo
                self._emitConnectedChanged = False
                self.connectedChanged.emit()

            

            
            self._update_with_last_received(last_received)

        if self._received_states:
            last_received = self._received_states[-1]
            self.set_states(self, last_received)
            self._received_states = []

            if self._calibrating:
                self._calibration_states_samples.append(last_received)
        
        if self._calibrating:
            self.set_calibrationProgress(self,  len(self._calibration_samples)/(self._n_calibration_samples+self._n_drop_calib_samples))

            if self._calibrationProgress >= 1.0:
                self._calibration_samples = self._calibration_samples[-self._n_calibration_samples::]
                self._calibration_states_samples = self._calibration_states_samples[-self._n_calibration_samples::]
                offsets = calibration.calibrate(self._calibration_samples, self._calibration_wall_distance, self._specs, self._interpCal)

                if self._dTCorrection:
                    offsets = calibration.set_offset_to_base_temperature(self._calibration_states_samples, offsets, self._dTGainFactor, self._dTFix)

                self._dev.set_calib_values(leddar.calib_types['ID_TIMEBASE_DELAY'], offsets.tolist())
                self.saveCalibration(offsets = offsets.tolist())
                self.set_calibrating(self, False)

        if self._received_traces_raw:
            self._update_traces_with_last_recieved(self._received_traces_raw[-1])
            self._received_traces_raw = []


    
    def saveCalibration(self, offsets, spath = 'calib_results/' ):

        if not os.path.exists(spath):
            os.makedirs(spath)
    

        dico = { 'v': self._specs['v'],
                 'h': self._specs['h'], 
                 'v_fov': self._specs['v_fov'], 
                 'h_fov': self._specs['h_fov'],
                 'dT_slope': self._dTGainFactor,
                 'dT_ref': self._dTFix,
                 'aT_slope': self._aTGainFactor,
                 'aT_threshold': self._aTThreshold,
                 'offsets': offsets,
                 'data': self._calibration_samples
                }
        
        if 'angles' in self._specs:
            dico['angles'] = self._specs['angles']
            dico['scaling_angles'] = self._scalevangles
        
        fname = spath + self._savingcalibinto
        with open(fname, 'wb') as f:
            pickle.dump(dico, f)
        
        return True