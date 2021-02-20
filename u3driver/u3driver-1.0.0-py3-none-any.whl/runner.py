import json
import re
import socket
import subprocess
import time
import multiprocessing

from u3driver.altUnityExceptions import *
from deprecated import deprecated
from u3driver.commands import *
from u3driver.altElement import AltElement
BUFFER_SIZE = 1024

class AltrunUnityDriver(object):

    def __init__(self, appium_driver,  platform, TCP_IP='127.0.0.1',TCP_PORT=13000, timeout=60,request_separator=';',request_end='&',device_id="",log_flag=False):
        self.TCP_PORT = TCP_PORT
        self.request_separator=request_separator
        self.request_end=request_end
        self.log_flag=log_flag
        self.appium_driver=None
        self.connect = False
        self.pause = False
        if (appium_driver != None):
            self.appium_driver = appium_driver

        while timeout > 0:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((TCP_IP, TCP_PORT))
                self.socket.settimeout(300)
                # print("Get server Version")
                GetServerVersion(self.socket, self.request_separator, self.request_end).execute()
                self.connect = True
                break
            except Exception as e:
                print(e)
                print('AltUnityServer not running on port ' + str(self.TCP_PORT) +
                      ', retrying (timing out in ' + str(timeout) + ' secs)...')
                timeout -= 5
                time.sleep(5)

        if timeout <= 0:
            raise Exception('Could not connect to AltUnityServer on: '+ TCP_IP +':'+ str(self.TCP_PORT))

    def NeedPause(self):
        while self.pause:
            time.sleep(1)
            print("[Info]udriver is pausing!")
    
    def Pause(self,pause):
        self.pause = pause

    def stop(self):
        self.pause = False
        CloseConnection(self.socket,self.request_separator,self.request_end).execute()

    def find_object(self,by,value,image_url = None):
        self.NeedPause()
        return FindObject(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,image_url).execute()

    def tap_at_coordinates(self,x,y):
        self.NeedPause()
        return TapAtCoordinates(self.socket,self.request_separator,self.request_end,self.appium_driver,x,y).execute()

    def find_object_and_tap(self,by,value,camera_name='',enabled=True):
        self.NeedPause()
        return FindObjectAndTap(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()

    def find_object_in_range_where_name_contains(self, name,range_path,camera_name='',enabled=True):
        self.NeedPause()
        return FindObjectInRangeWhereNameContains(self.socket,self.request_separator,self.request_end,self.appium_driver,name,range_path,camera_name,enabled).execute()

    def object_exist(self, by,value):
        self.NeedPause()
        return ObjectExist(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value).execute()

    def find_all_object_where_text_contains(self,text):
        self.NeedPause()
        return FindAllObjectWhereTextContains(self.socket,self.request_separator,self.request_end,self.appium_driver,text).execute()

    def get_screen(self):
        self.NeedPause()
        return GetScreen(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

    def find_child(self,value):
        self.NeedPause()
        return FindChild(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()
    
    def get_object_rect(self,value):
        self.NeedPause()
        return GetObjectRect(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()
    
    def find_all_objects(self,value):
        self.NeedPause()
        return FindAllObjects(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()

    def find_all_objects_in_range_where_text_contains(self,value,text):
        self.NeedPause()
        return FindAllObjectInRangeWhereTextContains(self.socket,self.request_separator,self.request_end,self.appium_driver,value,text).execute()
    
    #调用格式如下：组件名必须是完整的，而且要带上模块名称
    #udriver.get_value_on_component("//Canvas","Test,Assembly-CSharp","test1")
    #udriver.get_value_on_component("//Canvas","UnityEngine.UI.Text,UnityEngine.UI","text")
    def get_value_on_component(self,path,component_name,value_name):
        self.NeedPause()
        return GetValueOnComponent(self.socket,self.request_separator,self.request_end,self.appium_driver,path,component_name,value_name).execute()

    def debug_mode(self,file_path = None):
        return DebugMode(self.socket,self.request_separator,self.request_end,file_path).execute()

    def drag_object(self,path,x1,y1,x2 = None,y2 = None):
        self.NeedPause()
        return Drag(self.socket,self.request_separator,self.request_end,path,x1,y1,x2,y2).execute()

    
    '''
    用法:
    id = udriver.find_all_objects_where_text_contains("//UICanvas","xxx")[0]["id"]
    udriver.tap_by_id(id)
    '''
    def tap_by_id(self,id):
        # json.dumps({"id",id})
        self.NeedPause()
        return AltElement(CommandReturningAltElements(self.socket,self.request_separator,self.request_end,self.appium_driver),self.appium_driver,'{"name":"","id":"'+ id +'"}').tap()

    def find_all_text(self):
        self.NeedPause()
        return FindAllText(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

    def get_hierarchy(self):
        self.NeedPause()
        return GetHierarchy(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

        
    def get_inspector(self, id):
        self.NeedPause()
        return GetInspector(self.socket,self.request_separator,self.request_end,self.appium_driver, id).execute()

    def get_server_version(self):
        return GetServerVersion(self.socket, self.request_separator, self.request_end).execute()