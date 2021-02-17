import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import numpy as np
import uuid as py_uuid

class UuidUtil(object):

    def __init__(self, node = None, client_obj = None):
        if node is None:
            self._node = RRN
        else:
            self._node = node
        self._client_obj = client_obj
        
        self._uuid_dt = node.GetNamedArrayDType("com.robotraconteur.uuid.UUID", self._client_obj)

    def UuidFromPyUuid(self, py_uuid):
        ret_bytes = np.frombuffer(py_uuid.bytes,dtype=np.uint8)
        ret = np.zeros((1,),dtype=self._uuid_dt)
        ret[0]["uuid_bytes"]=ret_bytes
        return ret

    def UuidToPyUuid(self, uuid):
        uuid_bytes = uuid["uuid_bytes"].tobytes()
        return py_uuid.UUID(bytes=uuid_bytes)

    def NewRandomUuid(self):
        new_uuid = py_uuid.uuid4()
        return self.UuidFromPyUuid(new_uuid)

    def ParseUuid(self,uuid_str):
        return self.UuidFromPyUuid(py_uuid.UUID(uuid_str))

    def UuidToString(self,uuid):
        return str(self.UuidToPyUuid(uuid))
