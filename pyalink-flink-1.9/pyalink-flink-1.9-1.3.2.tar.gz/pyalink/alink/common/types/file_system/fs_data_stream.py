from ..bases.j_obj_wrapper import JavaObjectWrapperWithFunc
from ..conversion.java_method_call import auto_convert_java_type
from ....py4j_util import get_java_class


class InputStreamWrapper(JavaObjectWrapperWithFunc):
    def read(self, length=1, offset=0):
        DataStreamReadUtil = get_java_class("com.alibaba.alink.python.util.DataStreamReadUtil")
        (numBytesRead, b) = auto_convert_java_type(DataStreamReadUtil.read)(self.get_j_obj(), length, offset)
        return numBytesRead, b
