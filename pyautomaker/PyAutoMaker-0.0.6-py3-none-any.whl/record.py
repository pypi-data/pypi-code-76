import keyboard
import mouse
import ctypes
import time
import copy
import random
import json
from glob import glob
from queue import Queue
from ast import literal_eval

class RecordKeyboardEvent:
    EVENT_NAME = "keyboard"

    VKEY_CODE = "vkeyCode"
    KEY_NAME = "keyName"
    KEY_STATE = "keyState"
    SLEEP = "sleep"

    def __init__(self, vkeyCode, keyName = "", keyState = 0, sleep = 0):
        if isinstance(vkeyCode, dict):
            self.loadJson(vkeyCode)
            return

        self.vkeyCode = vkeyCode
        self.keyName = keyName
        self.keyState = keyState
        self.sleep = sleep

    def __del__(self):
        pass

    def __str__(self):
        return self.toJson()

    def toJson(self):
        jsonString = json.dumps({"eventName" : self.EVENT_NAME, self.VKEY_CODE : self.vkeyCode, self.KEY_NAME : self.keyName
                                 , self.KEY_STATE : self.keyState, self.SLEEP : self.sleep})

        return jsonString

    def loadJson(self, data):
        #data = json.loads(jsonString)

        self.vkeyCode = data[self.VKEY_CODE]
        self.keyName = data[self.KEY_NAME]
        self.keyState = data[self.KEY_STATE]
        self.sleep = data[self.SLEEP]

class RecordMoveEvent:
    EVENT_NAME = "move"
    X = "x"
    Y = "y"
    SLEEP = "sleep"

    def __init__(self, x, y = 0, sleep = 0):
        if isinstance(x, dict):
            self.loadJson(x)
            return

        self.x = x
        self.y = y
        self.sleep = sleep

    def __del__(self):
        pass

    def __str__(self):
        return self.toJson()

    def toJson(self):
        jsonString = json.dumps({"eventName" : self.EVENT_NAME, self.X:self.x, self.Y:self.y, self.SLEEP : self.sleep})

        return jsonString

    def loadJson(self, data):
        #data = json.loads(jsonString)
        
        self.x = data[self.X]
        self.y = data[self.Y]
        self.sleep = data[self.SLEEP]

class RecordButtonEvent:
    EVENT_NAME = "button"
    BUTTON = "button"
    BUTTON_STATE = "buttonState"
    SLEEP = "sleep"

    def __init__(self, button, buttonState = "", sleep = 0):
        if isinstance(button, dict):
            self.loadJson(button)
            return

        self.button = button
        self.buttonState = buttonState
        self.sleep = sleep

    def __del__(self):
        pass

    def __str__(self):
        return self.toJson()

    def toJson(self):
        jsonString = json.dumps({"eventName" : self.EVENT_NAME, self.BUTTON : self.button, self.BUTTON_STATE : self.buttonState, self.SLEEP : self.sleep})

        return jsonString

    def loadJson(self, data):
        #data = json.loads(jsonString)

        self.button = data[self.BUTTON]
        self.buttonState = data[self.BUTTON_STATE]
        self.sleep = data[self.SLEEP]
        
RECORD_KEYBOARD = 1
RECORD_MOUSE = 2
RECORD_ALL = 4

class Record:
    #keyboard모듈이 알려주는 키코드는 스캔코드임
    #그 코드를 변환하기 위해서 사용하는 플래그
    #https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
    MAPVK_VSC_TO_VK = 1 #좌우 구분을 하지 않음, 호출이 실패하면 0을 반환
    MAPVK_VSC_TO_VK_EX = 3 #좌우 구분을 함, 호출이 실패하면 0을 반환
    
    def __init__(self, dd = None):
        self.dd = dd
        if self.dd != None:
            self.btnCode = {"left" : self.dd.MOUSE_LDOWN, "right" : self.dd.MOUSE_RDOWN}

        #스캔코드 -> 가상키코드로 변환을 위해서 함수 객체를 만듬
        #UINT MapVirtualKeyW(UINT uCode, UINT uMapType);
        self.MapVirtualKeyW = ctypes.windll.user32["MapVirtualKeyW"]
        #파라미터를 강제함, UINT, UINT
        self.MapVirtualKeyW.argtypes = (ctypes.c_uint32, ctypes.c_uint32)
        #리턴값을 강제함
        self.MapVirtualKeyW.restype = (ctypes.c_uint32)

    def __del__(self):
        pass

    def mapVirtualKey(self, uCode, uMapType = MAPVK_VSC_TO_VK):
        #스캔코드를 가상키코드로 변환하는 함수
        #keyboard모듈은 스캔코드를 리턴함
        return self.MapVirtualKeyW(uCode, uMapType)

    def makeEventList(self, eventList):
        if len(eventList) <= 1:
            return []

        newEventList = []

        for idx in range(len(eventList) - 1):
            newEvent = None
            if isinstance(eventList[idx], keyboard.KeyboardEvent):
                newEvent = RecordKeyboardEvent(self.mapVirtualKey(eventList[idx].scan_code), eventList[idx].name
                                               , keyboard.KEY_DOWN if eventList[idx].event_type == keyboard.KEY_DOWN else keyboard.KEY_UP
                                               , eventList[idx + 1].time - eventList[idx].time)
            elif isinstance(eventList[idx], mouse.MoveEvent):
                newEvent = RecordMoveEvent(eventList[idx].x, eventList[idx].y, eventList[idx + 1].time - eventList[idx].time)

            elif isinstance(eventList[idx], mouse.ButtonEvent):
                newEvent = RecordButtonEvent(eventList[idx].button, eventList[idx].event_type, eventList[idx + 1].time - eventList[idx].time)

            if newEvent == None:
                continue

            newEventList.append(newEvent)

        newEventList[-1].sleep = 0
        return newEventList

    def save(self, recorded, savePath):
        #녹화된 키보드 마우스 코드를 파일로 저장하는 함수
        #각 이벤트의 타입을 조사하고 input_type에 입력함, 그래야지 다시 불러올 때 타입을 알 수 있음
        #파일을 만듬
        with open(savePath, "wt") as f:

            #녹화데이터를 반복하면서 문자열로 변경
            for data in recorded:
                jsonString = data.toJson()
                #파일에 입력
                f.write(jsonString + "\n")
                
            #성공적으로 파일을 만들었고 저장했을 때
            return True

        #파일을 만들지 못함
        return False
    
    def record(self, until = "esc", record_type = RECORD_ALL, savePath = None):
        #키보드와 마우스 이벤트를 녹화하는 함수
        
        #recorded = keyboard.record(until = until)
        #녹화한 데이터가 들어갈 큐
        #여러 스레드에서 입, 출 하는 경우에는 List말고 Queue와 같이 락을 지원하는 컨테이너를 사용해야함
        recorded = Queue()

        if record_type == RECORD_KEYBOARD or record_type == RECORD_ALL:
            keyboard.start_recording(recorded)#키보드 녹화시작
        
        if record_type == RECORD_MOUSE or record_type == RECORD_ALL:
            mouse.hook(recorded.put)#마우스 녹화 시작

        keyboard.wait(until)#지정한 키가 눌릴 때까지 대기

        if record_type == RECORD_KEYBOARD or record_type == RECORD_ALL:
            keyboard.stop_recording()#키보드 녹화 중지

        if record_type == RECORD_MOUSE or record_type == RECORD_ALL:
            mouse.unhook_all()#마우스 녹화 중지
        

        #녹화된 이벤트를 리스트 형태로 변환함
        recorded = [recorded.get() for idx in range(recorded.qsize())]

        recorded = self.makeEventList(recorded)

        #파일로 저장할 경로가 주어졌다면 저장
        if savePath:
            self.save(recorded, savePath)

        #녹화된 키보드, 마우스 이벤트 리스트를 반환
        return recorded
    

    def load(self, filePath):
        #저장한 파일을 불러오는 함수
        with open(filePath, "rt") as f:
            #한번에 모든 라인을 불러옴
            #큰 파일이 있을 수 있으니 반복문을 돌면서 처리하도록 수정할것
            fileDatas = f.readlines()

            eventList = []
            for line in fileDatas:
                data = json.loads(line)
                if data["eventName"] == RecordKeyboardEvent.EVENT_NAME:
                    eventList.append(RecordKeyboardEvent(data))
                elif data["eventName"] == RecordMoveEvent.EVENT_NAME:
                    eventList.append(RecordMoveEvent(data))
                elif data["eventName"] == RecordButtonEvent.EVENT_NAME:
                    eventList.append(RecordButtonEvent(data))

            return eventList

    def loadEx(self, filePath):
        """
        loadDataList = loadEx("C:\\*.txt")
        """
        #지정한 경로에서 파일 리스트를 긁어옴
        filePathList = glob(filePath)
        eventLists = []

        #파일을 읽고 파싱한 뒤 데이터를 리스트에 저장
        for filePath in filePathList:
            eventLists.append(self.load(filePath))

        return eventLists

    def playDD(self, event, randomTime = (0.00, 0.00)):
        if isinstance(event, RecordKeyboardEvent):
            self.dd.DD_keyEx(event.vkeyCode, self.dd.KEY_DOWN if event.keyState == "down" else self.dd.KEY_UP)
            time.sleep(event.sleep + random.uniform(*randomTime))
        elif isinstance(event, RecordMoveEvent):
            self.dd.DD_mov(event.x, event.y)
            #time.sleep(event.sleep)
        elif isinstance(event, RecordButtonEvent):
            code = self.btnCode.get(event.button, None)
            if code == None:
                return

            code = code << 1 if event.buttonState == "up" else code

            print(code)
            self.dd.DD_btn(code)
            pass
        else:
            return

        time.sleep(event.sleep + random.uniform(*randomTime))


    def play(self, eventList, randomTime = (0.00, 0.00)):
        if self.dd == None:
            return

        for event in eventList:
            print(event)
            self.playDD(event, randomTime)
        
    
if __name__ == "__main__":
    pass
