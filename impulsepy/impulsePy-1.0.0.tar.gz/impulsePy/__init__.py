import pyzmq
from threading import Thread, Event
import json
import pandas as pd
import os
from time import sleep

versionNo = "1.0.0"

controlEndpoint = "tcp://127.0.0.1:5557"
dataEndpoint = "tcp://127.0.0.1:5556"

profilesPath = os.path.expanduser('~\\Documents\\Impulse\\Profiles\\')
profilesPath = profilesPath.replace("\\","/")


decimalVals = {
    'temperatureMeasured': 6,
    'temperatureSetpoint': 6,
    'powerMeasured': 3,
    'currentMeasured': 18,
    'voltageMeasured': 15,
    'setpoint': 18,
    'resistance': 11,
    'compliance': 18,
    'gas1FlowMeasured': 9,
    'gas2FlowMeasured': 9,
    'gas3FlowMeasured': 9,
    'gas1ConcentrationMeasured': 2,
    'gas2ConcentrationMeasured': 2,
    'gas3ConcentrationMeasured': 2,
    'gas1FlowSetpoint': 9,
    'gas2FlowSetpoint': 9,
    'gas3FlowSetpoint': 9,
    'gas1ConcentrationSetpoint': 2,
    'gas2ConcentrationSetpoint': 2,
    'inletPressureMeasured': 7,
    'outletPressureMeasured': 7,
    'inletPressureSetpoint': 7,
    'outletPressureSetpoint': 7,
    'reactorPressureMeasured': 7,
    'reactorFlowMeasured': 9,
    'reactorPressureSetpoint': 7,
    'reactorFlowSetpoint': 9,
    'vacuumPressureMeasured': 9,
    'flowCheckSetpoint': 9,
}

def version():
    return versionNo

def createControlMessage(details):
    controlString = json.dumps(details)
    controlStringB = bytes(controlString, 'utf_8')
    return controlStringB

def sendControl(controlDict):  
    controlString = createControlMessage(controlDict)
    context = pyzmq.Context()
    controlSock = context.socket(pyzmq.REQ)
    controlSock.connect(controlEndpoint)
    controlSock.send(controlString)
    returnMessage = controlSock.recv_json()
    controlSock.setsockopt(pyzmq.LINGER, 0)
    controlSock.close()
    context.term()
    if returnMessage["resultCode"] != "ok":
        if returnMessage["resultCode"] == "invalidInput":
            print("[INVALID INPUT]: ", returnMessage["message"], ":")
            for error in returnMessage["data"]["errors"]:
                print("    - ", error["parameter"],
                      error["$type"].split('.')[-1], error["description"])
        elif returnMessage["resultCode"] == "badRequest":
            print("[BAD REQUEST]:",
                  controlString.decode('ascii'))
        elif returnMessage["resultCode"] == "invalidOperation":
            print("[INVALID OPERATION]: ",
                  controlString.decode('ascii'))
    return returnMessage

def disconnect():
    if heat.data.dataSock is not None:
        heat.data.disconnect()
    if bias.data.dataSock is not None:
        bias.data.disconnect()
    if gas.data.dataSock is not None:
        gas.data.disconnect()
    if gas.msdata.dataSock is not None:
        gas.msdata.disconnect()
    if events.eventSock is not None:
        events.disconnect()
    sleep(1)
    print("Disconnected from impulse")

def getStatus():
    controlDict = {
        '$type' : 'control.impulse.getStatus'
        }
    returnMessage = sendControl(controlDict)
    status = returnMessage["data"]["status"]
    return status

def waitForControl():
    status = getStatus()
    print("[IMPULSE STATUS]:", status)
    while status != "control": 
        sleep(0.2)
        newStatus = getStatus()
        if newStatus != status: 
            print("[IMPULSE STATUS]:", newStatus)
        status = newStatus
    sleep(1) # To prevent fatal errors

class profile():
    def load(self, location):
        controlDict = {
            '$type' : 'control.profileController.loadProfile',
            'path' : location  
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]             

    def getStatus(self):
        controlDict = {
            '$type' : 'control.impulse.getStatus'
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]  

    def control(self, action):
        controlDict = {
            '$type' : 'control.profileController.controlProfile',
            'action' : action
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]  

class heat():
    def __init__(self):
        self.data = dataHandler("heat")
        self.busy = False
    
    def startRamp(self, setPoint, timeOrRate, rampTimeRate):
        controlDict = {
            '$type' : 'control.heat.startRamp',
            'temperature' : setPoint,
            timeOrRate : rampTimeRate    
            }
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            self.busy = True
        return returnMessage["resultCode"]        

    def stopRamp(self):
        controlDict = {
            '$type' : 'control.heat.stopRamp' 
            }
        returnMessage = sendControl(controlDict)
        if returnMessage['resultCode']=='ok':
            self.busy = False
        return returnMessage["resultCode"]  


    def set(self, setPoint):
        self.data.setPointChanged()
        self.startRamp(setPoint, "rampTime", 0)

class bias():
    def __init__(self):
        self.data = dataHandler("bias")
        self.busy = False
        
    def getConfiguration(self):
        controlDict = {
            '$type' : 'control.bias.getConfiguration'        
            }
        returnMessage = sendControl(controlDict)
        return returnMessage
    
    def set(self, setPoint, compliance):
        controlDict = {
            '$type' : 'control.bias.applyConstantBias',
            'setpoint' : setPoint,
            'compliance' : compliance
            }
        returnMessage = sendControl(controlDict)
        self.data.setPointChanged()
        return returnMessage["resultCode"]
    
    def startSweepCycle(self, baseline, amplitude, sweepCycleType, rate, cycles, compliance):
        controlDict = {
            '$type' : 'control.bias.startSweepCycle',
            'baseline' : baseline,
            'amplitude' : amplitude,
            'sweepCycleType' : sweepCycleType,
            'rate' : rate,
            'cycles' : cycles,
            'compliance' : compliance            
            }
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            self.busy = True
        return returnMessage["resultCode"]

    def stopSweepCycle(self):
        controlDict = {
            '$type' : 'control.bias.stopSweepCycle'          
            }
        returnMessage = sendControl(controlDict)
        if returnMessage['resultCode']=='ok':
            self.busy = False
        return returnMessage["resultCode"]

class gas():
    def __init__(self):
        self.data = dataHandler("gas")
        self.msdata = dataHandler("massSpec")
        self.busy = False
        self.gasSystemType = None
        self.controlMode = None
        
    def getConfiguration(self):
        controlDict = {
            '$type' : 'control.gas.getConfiguration'        
            }
        returnMessage = sendControl(controlDict)
        self.gasSystemType = returnMessage['data']['$type'].split('.')[-1]
        return returnMessage

    def setBypass(self, toggleState):
        controlDict = {
            '$type' : 'control.gas.setBypass',
            'state' : toggleState
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]       
    
    def setFlowCheck(self, flow, state):
        controlDict = {
            '$type' : 'control.gas.setFlowCheck',
            'state' : state,
            'flow' : flow
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]       

    def flushReactor(self, state):
        controlDict = {
            '$type' : 'control.gas.flushReactor',
            'state' : state
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]       
        
    def stopRamp(self):
        controlDict = {
            '$type' : 'control.gas.stopRamp'
            }
        returnMessage = sendControl(controlDict)
        if returnMessage['resultCode']=='ok':
            self.busy = False
        return returnMessage["resultCode"]       
    
    def evacuateHolder(self):
        controlDict = {
            '$type' : 'control.gas.evacuateHolder'
            }
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]       

    def startIOPRamp(self, inletPressure, outletPressure, rampTime, gas1Flow=None, gas1FlowPath=None, gas2Flow=None, gas2FlowPath=None, gas3Flow=None, gas3FlowPath=None ):
        if self.gasSystemType is None:
            self.getConfiguration()
        controlDict = {
            '$type' : 'control.gas.' + self.gasSystemType + '.inletOutletPressure.startRamp',
            'inletPressure' : inletPressure,
            'outletPressure' : outletPressure,
            'rampTime' : rampTime
            }
        if gas1Flow is not None:
            controlDict['gas1Flow']=gas1Flow
            controlDict['gas1FlowPath']=gas1FlowPath
            controlDict['gas2Flow']=gas2Flow
            controlDict['gas2FlowPath']=gas2FlowPath            
            controlDict['gas3Flow']=gas3Flow
            controlDict['gas3FlowPath']=gas3FlowPath           
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            self.busy = True
        return returnMessage["resultCode"]
    
    def setIOP(self, inletPressure, outletPressure, gas1Flow=None, gas1FlowPath=None, gas2Flow=None, gas2FlowPath=None, gas3Flow=None, gas3FlowPath=None):
        returnMessage = self.startIOPRamp(inletPressure, outletPressure, 0, gas1Flow, gas1FlowPath, gas2Flow, gas2FlowPath, gas3Flow, gas3FlowPath)
        self.data.setPointChanged()
        return returnMessage
    
    def startPFRamp(self, reactorPressure, reactorFlow, rampTime, gasConcentrationType=None, gas1Concentration=None, gas2Concentration=None ):
        if self.gasSystemType is None:
            self.getConfiguration()
        controlDict = {
            '$type' : 'control.gas.' + self.gasSystemType + '.pressureFlow.startRamp',
            'reactorPressure' : reactorPressure,
            'reactorFlow' : reactorFlow,
            'rampTime' : rampTime
            }
        if gasConcentrationType is not None:
            controlDict['gasConcentrationType']=gasConcentrationType
            controlDict['gas1Concentration']=gas1Concentration
            controlDict['gas2Concentration']=gas2Concentration        
        returnMessage = sendControl(controlDict)
        if returnMessage["resultCode"] =="ok":
            self.busy = True
        return returnMessage["resultCode"]    
    
    def setPF(self, reactorPressure, reactorFlow, gasConcentrationType=None, gas1Concentration=None, gas2Concentration=None):
        returnMessage = self.startPFRamp(reactorPressure, reactorFlow, 0, gasConcentrationType, gas1Concentration, gas2Concentration)
        self.data.setPointChanged()
        return returnMessage
    
    def initiateFlow(self, reactorPressure, reactorFlow, gasConcentrationType, gas1Concentration, gas2Concentration):
        controlDict = {
            '$type' : 'control.gas.gplus.pressureFlow.initiateFlow',
            'reactorPressure' : reactorPressure,
            'reactorFlow' : reactorFlow,
            'gasConcentrationType' : gasConcentrationType,
            'gas1Concentration' : gas1Concentration,
            'gas2Concentration' : gas2Concentration
            }        
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]   

    def stopInitiateFlow(self):
        controlDict = {
            '$type' : 'control.gas.gplus.pressureFlow.stopInitializingFlow',
            }        
        returnMessage = sendControl(controlDict)
        return returnMessage["resultCode"]           

class eventHandler():
    def __init__(self):
        self.event = Event()
        self.lastMssg = None
        self.eventSock = None

    def subscribe(self):
        self.context = pyzmq.Context()
        self.eventSock = self.context.socket(pyzmq.SUB)
        self.eventSock.connect(dataEndpoint)
        btopic = bytes('event', 'utf_8')
        self.eventSock.setsockopt(pyzmq.SUBSCRIBE, btopic)
        self.eventCatcherThread = Thread(target=self.eventCatcher)
        self.eventCatcherThread.start()

    def eventCatcher(self):
        print("Subscribed to impulse events. ")
        sleep(0.01)
        while True:
            if self.event.is_set():
                break
            try:
                [address, contents] = self.eventSock.recv_multipart()
            except:
                continue
            else:
                contents = json.loads(contents)
                self.lastMssg = contents
                if contents["$type"]=="data.event.stimulusActionFinished":
                    if contents["stimulusType"]=="heat":
                        heat.busy = False
                    if contents["stimulusType"]=="bias":
                        bias.busy = False
                    if contents["stimulusType"]=="gas":
                        gas.busy = False
                elif contents["$type"] == "data.event.profileController.stateChanged": #deze moet ook anders heten
                    print("[PROFILE CONTROLLER]:",contents['state'])
                elif contents["$type"] == "data.event.popupRaised":
                    print("[IMPULSE POPUP]:",contents['message'])
                elif contents["$type"] == "data.event.notificationRaised":
                    print("[IMPULSE NOTIFICATION]:",contents['message'])
                    sleep(0.1)
                else:
                    print("[IMPULSE EVENT]:",contents)
        self.eventSock.setsockopt(pyzmq.LINGER, 0)
        self.eventSock.close()
        self.context.term()
        self.eventSock = None # For jupyter notebook if a cell is rerun
        self.event.clear()
        
    def disconnect(self):
        self.event.set()


class dataHandler():
    def __init__(self, topic):
        self.topic = topic
        self.lastSentSequence = 0
        self.lastMssg = None
        self.context= None
        self.dataSock = None
        self.data = None
        self.header = None
        self.flags = {}
        self.currentFlag = ""
        self.event = Event()

    def subscribe(self):
        self.context = pyzmq.Context()
        self.dataSock = self.context.socket(pyzmq.SUB)
        self.dataSock.connect(dataEndpoint)
        btopic = bytes(self.topic, 'utf_8')
        self.dataSock.setsockopt(pyzmq.SUBSCRIBE, btopic)
        self.dataThread = Thread(target=self.incomingDataReader)
        self.dataThread.start()
        print(f"Subscribed to {self.topic} data. ")

    def incomingDataReader(self):
        if self.topic != "massSpec":
            while True:
                if self.event.is_set():
                    break
                try:
                    [address, contents] = self.dataSock.recv_multipart()
                except:
                    continue
                else:
                    contents = json.loads(contents)
                    contents["flags"]=self.currentFlag
                    self.lastMssg = contents
                    if self.header is None:
                        self.header = list(contents.keys())
                        self.data = pd.DataFrame(columns=self.header)
                    self.data = self.data.append(contents, ignore_index=True, sort=False)
        else: # Special DataReceiver for MS data
            while True:
                if self.event.is_set():
                    break
                try:
                    [address, contents] = self.dataSock.recv_multipart()
                except:
                    continue
                else:
                    contents = json.loads(contents)
                    for channel in contents["channels"]:
                       contents[channel["name"]]=channel["measuredValue"]
                    del contents["channels"]
                    contents["flags"]=self.currentFlag
                    self.lastMssg = contents
                    if self.header is None:
                        self.header = list(contents.keys())
                        self.data = pd.DataFrame(columns=self.header)
                    self.data = self.data.append(contents, ignore_index=True, sort=False)
        self.dataSock.setsockopt(pyzmq.LINGER, 0)
        self.dataSock.close()
        self.context.term()
        self.event.clear()
        self.dataSock = None #For jupyter notebook, if a cell is rerun

    def disconnect(self):
        self.event.set()

    def setPointChanged(self):
        self.lastSentSequence = self.lastMssg["sequenceNumber"]

    def roundDataFrame(self, dataSet):       
        dataSet = dataSet.round(decimalVals)
        return dataSet
        
    def getLastData(self):
        if self.dataSock is not None:
            self.lastSentSequence = self.lastMssg["sequenceNumber"]
            dataSet = self.lastMssg
            for key, value in dataSet.items():
                if key in decimalVals:
                    dataSet[key]=round(dataSet[key],decimalVals[key])
            return dataSet

        else:
            if self.topic == 'massSpec':
                print("[ALERT] Please subscribe using impulse.gas.msdata.subscribe() first")
            else:
                print(f"[ALERT] Please subscribe using impulse.{self.topic}.data.subscribe() first")
            return []

    def getNewData(self):
        if self.dataSock is not None:
            while self.lastMssg["sequenceNumber"] == self.lastSentSequence:
                sleep(0.001)
            self.lastSentSequence = self.lastMssg["sequenceNumber"]
            dataSet = self.lastMssg
            for key, value in dataSet.items():
                if key in decimalVals:
                    dataSet[key]=round(dataSet[key],decimalVals[key])
            return dataSet
        else:
            print(f"[ALERT] Please subscribe using impulse.{self.topic}.data.subscribe() first")
            return []
        
    def setFlag(self, flagName):
        if self.dataSock is not None:
            self.flags[flagName]=len(self.data)
            self.currentFlag = flagName
        else:
            print(f"[ALERT] Please subscribe using impulse.{self.topic}.data.subscribe() first")
            return []

    def getDataFrame(self, startRowOrFlag=1, endRowOrFlag=None):
        if self.dataSock is not None:    
            if isinstance(startRowOrFlag, str):
                if startRowOrFlag in self.flags:
                    startRowOrFlag= self.flags[startRowOrFlag]
                else:
                    print(f"[ERROR] Flag {startRowOrFlag} does not exist!")
                    return []
            if isinstance(endRowOrFlag, str):
                if endRowOrFlag in self.flags:
                    endRowOrFlag= self.flags[endRowOrFlag]
                else:
                    print(f"[ERROR] Flag {endRowOrFlag} does not exist!")
                    return []
            df = self.data.iloc[startRowOrFlag:endRowOrFlag].copy()
            if len(df)>1:
                df["timeStamp"] = pd.to_datetime(df['timeStamp'])#.dt.tz_convert(None)
            df = self.roundDataFrame(df)
            return df
        else:
            print(f"[ALERT] Please subscribe using impulse.{self.topic}.data.subscribe() first")
            return []

profile = profile()
heat = heat()
bias = bias()
gas = gas()
events = eventHandler()
events.subscribe()