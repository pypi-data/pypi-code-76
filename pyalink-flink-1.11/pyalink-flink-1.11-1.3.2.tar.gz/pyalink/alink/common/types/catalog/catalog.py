from py4j.java_gateway import JavaObject
from pyflink.table.catalog import *

from ..bases.j_obj_wrapper import JavaObjectWrapper
from ..bases.params import Params
from ..conversion.java_method_call import auto_convert_java_type
from ..conversion.type_converters import py_list_to_j_array
from ....py4j_util import get_java_class


class BaseCatalog(Catalog, JavaObjectWrapper):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.BaseCatalog'

    def __init__(self, j_catalog):
        super(BaseCatalog, self).__init__(j_catalog)

    def get_j_obj(self):
        return self._j_catalog

    @auto_convert_java_type
    def open(self):
        self.open()

    @auto_convert_java_type
    def close(self):
        self.close()

    @classmethod
    def of(cls, params):
        return BaseCatalog(get_java_class(cls.j_cls_name).of(params))

    @auto_convert_java_type
    def getParams(self):
        return self.getParams()


class JdbcCatalog(BaseCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.JdbcCatalog'

    def __init__(self, *args):
        """
        Construct `JdbcCatalog` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. params: Params -> call `JdbcCatalog(Params params)` of Java side;
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            elif isinstance(args[0], Params):
                params = args[0]
                j_obj = j_constructor(params)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(JdbcCatalog, self).__init__(j_obj)


class HiveCatalog(BaseCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.HiveCatalog'

    def __init__(self, *args):
        """
        Construct `HiveCatalog` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. params: Params -> call `HiveCatalog(Params params)` of Java side;
        3. catalogName: str, defaultDatabase: str, hiveVersion: str hiveConfDir: str ->
        call `HiveCatalog(String catalogName, String defaultDatabase, String hiveVersion, String hiveConfDir)` of Java side.
        4. catalogName: str, defaultDatabase: str, hiveVersion: str, hiveConfDir: FilePath ->
        call `HiveCatalog(String catalogName, String defaultDatabase, String hiveVersion, FilePath hiveConfDir)` of Java side.
        5. catalogName: str, defaultDatabase: str, hiveVersion: str, hiveConfDir: str, kerberosPrincipal: str, kerberosKeytab: str ->
        call `HiveCatalog(String catalogName, String defaultDatabase, String hiveVersion, String hiveConfDir, String kerberosPrincipal, String kerberosKeytab)` of Java side.
        6. catalogName: str, defaultDatabase: str, hiveVersion: str, hiveConfDir: FilePath, kerberosPrincipal: str, kerberosKeytab: str ->
        call `HiveCatalog(String catalogName, String defaultDatabase, String hiveVersion, FilePath hiveConfDir, String kerberosPrincipal, String kerberosKeytab)` of Java side.
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
        elif len(args) == 4:
            catalogName, defaultDatabase, hiveVersion, hiveConfDir = args
            from ..file_system.file_system import FilePath
            if isinstance(hiveConfDir, FilePath):
                hiveConfDir = hiveConfDir.get_j_obj()
            j_obj = j_constructor(catalogName, defaultDatabase, hiveVersion, hiveConfDir)
        elif len(args) == 6:
            catalogName, defaultDatabase, hiveVersion, hiveConfDir, kerberosPrincipal, kerberosKeytab = args
            from ..file_system.file_system import FilePath
            if isinstance(hiveConfDir, FilePath):
                hiveConfDir = hiveConfDir.get_j_obj()
            j_obj = j_constructor(catalogName, defaultDatabase, hiveVersion, hiveConfDir, kerberosPrincipal, kerberosKeytab)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(HiveCatalog, self).__init__(j_obj)


class DerbyCatalog(JdbcCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.DerbyCatalog'

    def __init__(self, *args):
        """
        Construct `DerbyCatalog` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. params: Params -> call `DerbyCatalog(Params params)` of Java side;
        3. catalogName: str, defaultDatabase: str, derbyVersion: str, derbyPath: str -> call `DerbyCatalog(String catalogName, String defaultDatabase, String derbyVersion, String derbyPath)` of Java side.
        4. catalogName: str, defaultDatabase: str, derbyVersion: str, derbyPath: str, userName: str, password: str -> call `DerbyCatalog(String catalogName, String defaultDatabase, String derbyVersion, String derbyPath, String userName, String password)` of Java side.
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            elif isinstance(args[0], Params):
                params = args[0]
                j_obj = j_constructor(params)
        elif len(args) == 4:
            catalogName, defaultDatabase, derbyVersion, derbyPath = args
            j_obj = j_constructor(catalogName, defaultDatabase, derbyVersion, derbyPath)
        elif len(args) == 6:
            catalogName, defaultDatabase, derbyVersion, derbyPath, userName, password = args
            j_obj = j_constructor(catalogName, defaultDatabase, derbyVersion, derbyPath, userName, password)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(DerbyCatalog, self).__init__(j_obj)


class MySqlCatalog(JdbcCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.MySqlCatalog'

    def __init__(self, *args):
        """
        Construct `MySqlCatalog` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. params: Params -> call `MySqlCatalog(Params params)` of Java side;
        3. catalogName: str, defaultDatabase: str, mysqlVersion: str, mysqlUrl: str, port: str ->
        call `MySqlCatalog(String catalogName, String defaultDatabase, String mysqlVersion, String mysqlUrl, String port)` of Java side.
        4. catalogName: str, defaultDatabase: str, mysqlVersion: str, mysqlUrl: str, port: str, username: str, password: str ->
        call `MySqlCatalog(String catalogName, String defaultDatabase, String mysqlVersion, String mysqlUrl, String port, String userName, String password)` of Java side.
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            elif isinstance(args[0], Params):
                params = args[0]
                j_obj = j_constructor(params)
        elif len(args) == 5:
            catalogName, defaultDatabase, mysqlVersion, mysqlUrl, port = args
            j_obj = j_constructor(catalogName, defaultDatabase, mysqlVersion, mysqlUrl, port)
        elif len(args) == 7:
            catalogName, defaultDatabase, mysqlVersion, mysqlUrl, port, userName, password = args
            j_obj = j_constructor(catalogName, defaultDatabase, mysqlVersion, mysqlUrl, port, userName, password)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(MySqlCatalog, self).__init__(j_obj)


class SqliteCatalog(JdbcCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.SqliteCatalog'

    def __init__(self, *args):
        """
        Construct `SqliteCatalog` from arguments with a wrapped Java instance.
        Different combinations of arguments are supported:
        1. j_obj: JavaObject -> directly wrap the instance;
        2. params: Params -> call `SqliteCatalog(Params params)` of Java side;
        3. catalogName: str, defaultDatabase: str, sqliteVersion: str, dbUrls: List[str] ->
        call `SqliteCatalog(String catalogName, String defaultDatabase, String sqliteVersion, String[] dbUrls)` of Java side.
        4. catalogName: str, defaultDatabase: str, sqliteVersion: str, dbUrls: List[str], username: str, password: str ->
        call `SqliteCatalog(String catalogName, String defaultDatabase, String sqliteVersion, String[] dbUrls, String username, String password)` of Java side.
        :param args: arguments, see function description.
        """
        j_constructor = get_java_class(self.j_cls_name)
        j_string_cls = get_java_class("String")
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            elif isinstance(args[0], Params):
                params = args[0]
                j_obj = j_constructor(params)
        elif len(args) == 4:
            if isinstance(args[3], str):
                catalogName, defaultDatabase, sqliteVersion, dbUrl = args
                dbUrls = [dbUrl]
            else:
                catalogName, defaultDatabase, sqliteVersion, dbUrls = args
            j_obj = j_constructor(catalogName, defaultDatabase, sqliteVersion, py_list_to_j_array(j_string_cls, len(dbUrls), dbUrls))
        elif len(args) == 6:
            catalogName, defaultDatabase, sqliteVersion, dbUrls, userName, password = args
            j_obj = j_constructor(catalogName, defaultDatabase, sqliteVersion, py_list_to_j_array(j_string_cls, len(dbUrls), dbUrls), userName, password)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(SqliteCatalog, self).__init__(j_obj)


class InputOutputFormatCatalog(BaseCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.InputOutputFormatCatalog'


class OdpsCatalog(InputOutputFormatCatalog):
    j_cls_name = 'com.alibaba.alink.common.io.catalog.OdpsCatalog'

    def __init__(self, *args):
        j_constructor = get_java_class(self.j_cls_name)
        j_obj = None
        if len(args) == 1:
            if isinstance(args[0], JavaObject):
                j_obj = args[0]
            elif isinstance(args[0], Params):
                params = args[0]
                j_obj = j_constructor(params)
        elif len(args) == 8:
            catalogName, defaultDatabase, odpsVersion, accessId, accessKey, project, endPoint, runningProject = args
            j_obj = j_constructor(catalogName, defaultDatabase, odpsVersion, accessId, accessKey, project, endPoint, runningProject)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(OdpsCatalog, self).__init__(j_obj)
