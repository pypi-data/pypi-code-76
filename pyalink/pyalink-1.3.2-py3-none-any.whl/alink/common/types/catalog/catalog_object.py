from py4j.java_gateway import JavaObject

from ..bases.j_obj_wrapper import JavaObjectWrapperWithAutoTypeConversion
from ....py4j_util import get_java_class


class CatalogObject(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'com.alibaba.alink.params.io.HasCatalogObject$CatalogObject'

    def __init__(self, *args):
        """
        Construct `CatalogObject` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. catalog: BaseCatalog, objectPath: ObjectPath -> call `CatalogObject(BaseCatalog catalog, ObjectPath objectPath)` of Java side;
        3. catalog: BaseCatalog, objectPath: ObjectPath, params: Params -> call `CatalogObject(BaseCatalog catalog, ObjectPath objectPath, Params params)` of Java side;
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
        elif len(args) == 2:
            catalog, objectPath = args
            j_obj = j_constructor(catalog.get_j_obj(), objectPath._j_object_path)
        elif len(args) == 3:
            catalog, objectPath, params = args
            j_obj = j_constructor(catalog.get_j_obj(), objectPath._j_object_path, params)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def getCatalog(self):
        return self.getCatalog()

    def getObjectPath(self):
        return self.getObjectPath()

    def getParams(self):
        return self.getParams()

    def serialize(self):
        return self.serialize()

    @classmethod
    def deserialize(cls, s: str):
        return get_java_class(cls.j_cls_name).deserialize(s)
