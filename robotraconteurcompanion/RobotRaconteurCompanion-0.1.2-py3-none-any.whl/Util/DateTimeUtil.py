import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import datetime
import numpy as np
import math

class DateTimeUtil(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj

        self._datetimeutc_dt = node.GetPodDType("com.robotraconteur.datetime.DateTimeUTC", self._client_obj)
        self._datetimelocal = node.GetStructureType("com.robotraconteur.datetime.DateTimeLocal", self._client_obj)
        self._timespec2_dt = node.GetPodDType("com.robotraconteur.datetime.TimeSpec2", self._client_obj)
        self._timespec3_dt = node.GetNamedArrayDType("com.robotraconteur.datetime.TimeSpec3", self._client_obj)
        self._devicetime_dt = node.GetPodDType("com.robotraconteur.device.clock.DeviceTime", self._client_obj)

        self._datetime_const = node.GetConstants("com.robotraconteur.datetime")
        self._clock_codes = self._datetime_const["ClockTypeCode"]

    def UtcNow(self, device_info = None):        
        now_dt = self._node.NowUTC()
        now = (now_dt - datetime.datetime(1970,1,1,0,0,0,0)).total_seconds()
        ret = np.zeros((1,),dtype=self._datetimeutc_dt)
        ret[0]["seconds"] = int(math.floor(now))
        ret[0]["nanoseconds"] = int((now % 1.0)*1e9)
        ret[0]["clock_info"]["clock_type"] = self._clock_codes["default"]
        if device_info is not None and device_info.device is not None:
            ret[0]["clock_info"]["clock_uuid"] = device_info.device.uuid
        return ret

    def TimeSpec2Now(self, device_info = None):
        now_ts = self._node.NowTimeSpec()
        ret = np.zeros((1,),dtype=self._timespec2_dt)
        ret[0]["seconds"] = now_ts.seconds
        ret[0]["nanoseconds"] = now_ts.nanoseconds
        ret[0]["clock_info"]["clock_type"] = self._clock_codes["default"]
        if device_info is not None and device_info.device is not None:
            ret[0]["clock_info"]["clock_uuid"] = device_info.device.uuid
        return ret

    def TimeSpec3Now(self):
        now_ts = self._node.NowTimeSpec()
        ret = np.zeros((1,),dtype=self._timespec3_dt)
        ret[0]["microseconds"] = now_ts.seconds*1e6 + now_ts.nanoseconds*1e-3
        return ret

    def FillDeviceTime(self, device_info, seqno):
        ret = np.zeros((1,),self._devicetime_dt)
        ret[0]["device_seqno"] = seqno
        ret[0]["device_ts"] = self.TimeSpec2Now(device_info)
        ret[0]["device_utc"] = self.UtcNow(device_info)
        return ret