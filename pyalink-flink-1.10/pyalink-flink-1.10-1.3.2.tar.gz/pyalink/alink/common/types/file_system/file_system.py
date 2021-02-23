from py4j.java_gateway import JavaObject

from .fs_data_stream import InputStreamWrapper
from ..bases.j_obj_wrapper import JavaObjectWrapperWithAutoTypeConversion
from ..conversion.java_method_call import auto_convert_java_type
from ....py4j_util import get_java_class

__all__ = ['FilePath', 'Path', 'LocalFileSystem', 'HadoopFileSystem', 'OssFileSystem', 'S3HadoopFileSystem', 'S3PrestoFileSystem']


class URI(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'java.net.URI'

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], JavaObject):
            j_obj = args[0]
        else:
            j_obj = get_java_class(self.j_cls_name)(*args)
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def parseServerAuthority(self):
        return self.parseServerAuthority()

    def getRawSchemeSpecificPart(self):
        return self.getRawSchemeSpecificPart()

    def getSchemeSpecificPart(self):
        return self.getSchemeSpecificPart()

    def getRawAuthority(self):
        return self.getRawAuthority()

    def getRawUserInfo(self):
        return self.getRawUserInfo()

    def getRawPath(self):
        return self.getRawPath()

    def getRawQuery(self):
        return self.getRawQuery()

    def getRawFragment(self):
        return self.getRawFragment()

    def toASCIIString(self):
        return self.toASCIIString()

    def compareTo(self, arg0):
        return self.compareTo(arg0)

    def isAbsolute(self):
        return self.isAbsolute()

    def resolve(self, arg0):
        return self.resolve(arg0)

    @classmethod
    def create(cls, arg0):
        return get_java_class(cls.j_cls_name).create(arg0)

    def normalize(self):
        return self.normalize()

    def getPath(self):
        return self.getPath()

    def toURL(self):
        return self.toURL()

    def isOpaque(self):
        return self.isOpaque()

    def getScheme(self):
        return self.getScheme()

    def getAuthority(self):
        return self.getAuthority()

    def getFragment(self):
        return self.getFragment()

    def getQuery(self):
        return self.getQuery()

    def getHost(self):
        return self.getHost()

    def getUserInfo(self):
        return self.getUserInfo()

    def getPort(self):
        return self.getPort()

    def relativize(self, arg0):
        return self.relativize(arg0)


class FileStatus(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'org.apache.flink.core.fs.FileStatus'

    def __init__(self, j_obj):
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def getPath(self):
        return self.getPath()

    def getLen(self):
        return self.getLen()

    def getAccessTime(self):
        return self.getAccessTime()

    def isDir(self):
        return self.isDir()

    def getModificationTime(self):
        return self.getModificationTime()

    def getBlockSize(self):
        return self.getBlockSize()

    def getReplication(self):
        return self.getReplication()


class Path(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'org.apache.flink.core.fs.Path'

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], JavaObject):
            j_obj = args[0]
        else:
            j_obj = auto_convert_java_type(get_java_class(self.j_cls_name))(*args).get_j_obj()
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def suffix(self, arg0):
        return self.suffix(arg0)

    def depth(self):
        return self.depth()

    def makeQualified(self, arg0):
        return self.makeQualified(arg0)

    def hasWindowsDrive(self):
        return self.hasWindowsDrive()

    @classmethod
    def fromLocalFile(cls, arg0):
        return get_java_class(cls.j_cls_name).fromLocalFile(arg0)

    def compareTo(self, arg0):
        return self.compareTo(arg0)

    def getName(self):
        return self.getName()

    def getParent(self):
        return self.getParent()

    def isAbsolute(self):
        return self.isAbsolute()

    def getPath(self):
        return self.getPath()

    def getFileSystem(self):
        return self.getFileSystem()

    def toUri(self):
        return self.toUri()


class FileSystem(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'org.apache.flink.core.fs.FileSystem'

    def __init__(self, j_obj):
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    @classmethod
    def getLocalFileSystem(cls):
        return get_java_class(cls.j_cls_name).getLocalFileSystem()

    @classmethod
    def getUnguardedFileSystem(cls, fsUri):
        return get_java_class(cls.j_cls_name).getUnguardedFileSystem(fsUri)

    def getUri(self):
        return self.getUri()

    @classmethod
    def getDefaultFsUri(cls):
        return get_java_class(cls.j_cls_name).getDefaultFsUri()

    def getWorkingDirectory(self):
        return self.getWorkingDirectory()

    def getHomeDirectory(self):
        return self.getHomeDirectory()

    def getFileStatus(self, f):
        return self.getFileStatus(f)

    def getFileBlockLocations(self, file, start, len):
        return self.getFileBlockLocations(file, start, len)

    def createRecoverableWriter(self):
        return self.createRecoverableWriter()

    def getDefaultBlockSize(self):
        return self.getDefaultBlockSize()

    def listStatus(self, arg0):
        return self.listStatus(arg0)

    def getKind(self):
        return self.getKind()

    def isDistributedFS(self):
        return self.isDistributedFS()

    def initOutPathLocalFS(self, outPath, writeMode, createDirectory):
        return self.initOutPathLocalFS(outPath, writeMode, createDirectory)

    def initOutPathDistFS(self, outPath, writeMode, createDirectory):
        return self.initOutPathDistFS(outPath, writeMode, createDirectory)

    @classmethod
    def get(cls, uri):
        return get_java_class(cls.j_cls_name).get(uri)

    def delete(self, f, recursive):
        return self.delete(f, recursive)

    def create(self, f, overwrite):
        return self.create(f, overwrite)

    def exists(self, arg0):
        return self.exists(arg0)

    def mkdirs(self, f):
        return self.mkdirs(f)

    def rename(self, src, dst):
        return self.rename(src, dst)

    @classmethod
    def initialize(cls, arg0, arg1):
        if arg1 is None:
            return get_java_class(cls.j_cls_name).initialize(arg0)
        else:
            return get_java_class(cls.j_cls_name).initialize(arg0, arg1)

    def open(self, f, bufferSize=None):
        if bufferSize is None:
            return self.open(f)
        else:
            return self.open(f, bufferSize)


class FilePath(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.FilePath'

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], JavaObject):
            j_obj = args[0]
        else:
            j_obj = auto_convert_java_type(get_java_class(self.j_cls_name))(*args).get_j_obj()
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def getPath(self):
        return self.getPath()

    def getFileSystem(self):
        return self.getFileSystem()

    def getPathStr(self):
        return self.getPathStr()

    def serialize(self):
        return self.serialize()

    @classmethod
    def deserialize(cls, str):
        return get_java_class(cls.j_cls_name).deserialize(str)


class BaseFileSystem(FileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.BaseFileSystem'

    def __init__(self, j_obj):
        super(BaseFileSystem, self).__init__(j_obj)

    def get_j_obj(self):
        return self._j_obj

    @classmethod
    def isFileSystem(cls, params):
        return auto_convert_java_type(get_java_class(cls.j_cls_name).isFileSystem)(params)

    @classmethod
    def of(cls, params):
        return auto_convert_java_type(get_java_class(cls.j_cls_name).of)(params)

    def listDirectories(self, f):
        return self.listDirectories(f)

    def getFileStatus(self, f):
        return self.getFileStatus(f)

    def listStatus(self, f):
        return self.listStatus(f)

    def initOutPathLocalFS(self, outPath, writeMode, createDirectory):
        return self.initOutPathLocalFS(outPath, writeMode, createDirectory)

    def initOutPathDistFS(self, outPath, writeMode, createDirectory):
        return self.initOutPathDistFS(outPath, writeMode, createDirectory)

    def delete(self, f, recursive):
        return self.delete(f, recursive)

    def create(self, f, overwriteMode):
        return self.create(f, overwriteMode)

    def exists(self, f):
        return self.exists(f)

    def listFiles(self, f):
        return self.listFiles(f)

    def mkdirs(self, f):
        return self.mkdirs(f)

    def rename(self, src, dst):
        return self.rename(src, dst)

    def open(self, f, bufferSize=None):
        if bufferSize is None:
            return InputStreamWrapper(self.open(f))
        else:
            return InputStreamWrapper(self.open(f, bufferSize))

    def getSchema(self):
        return self.getSchema()


class LocalFileSystem(BaseFileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.LocalFileSystem'

    def __init__(self):
        j_obj = get_java_class(self.j_cls_name)()
        super(LocalFileSystem, self).__init__(j_obj)


class OssFileSystem(BaseFileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.OssFileSystem'

    """
    Construct `OssFileSystem` from arguments with a wrapped Java instance.
    Different combinations of arguments are supported:
    1. j_obj: JavaObject -> directly wrap the instance;
    2. ossVersion: str, endPoint: str, bucketName: str, accessId: str, accessKey: str -> 
    call `OssFileSystem(String ossVersion, String endPoint, String bucketName, String accessId, String accessKey)` of Java side;
    3. ossVersion: str, endPoint: str, bucketName: str, accessId: str, accessKey: str, securityToken: str -> 
    call `OssFileSystem(String ossVersion, String endPoint, String bucketName, String accessId, String accessKey, String securityToken)` of Java side;
    :param args: arguments, see function description.
    """

    def __init__(self, *args):
        j_obj = None
        if len(args) == 1:
            j_obj = args[0]
        elif len(args) == 5:
            ossVersion, endPoint, bucketName, accessId, accessKey = args
            j_obj = get_java_class(self.j_cls_name)(ossVersion, endPoint, bucketName, accessId, accessKey)
        elif len(args) == 6:
            ossVersion, endPoint, bucketName, accessId, accessKey, securityToken = args
            j_obj = get_java_class(self.j_cls_name)(ossVersion, endPoint, bucketName, accessId, accessKey,
                                                    securityToken)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(OssFileSystem, self).__init__(j_obj)


class HadoopFileSystem(BaseFileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.HadoopFileSystem'

    """
    Construct `HadoopFileSystem` from arguments with a wrapped Java instance.
    Different combinations of arguments are supported:
    1. j_obj: JavaObject -> directly wrap the instance;
    2. hadoopVersion: str, fsUri: str -> call `HadoopFileSystem(String hadoopVersion, String fsUri)` of Java side;
    3. hadoopVersion: str, fsUri: str, configuration: FilePath -> call `HadoopFileSystem(String hadoopVersion, String fsUri, FilePath configuration)` of Java side;
    :param args: arguments, see function description.
    """

    def __init__(self, *args):
        j_obj = None
        if len(args) == 1:
            j_obj = args[0]
        elif len(args) == 2:
            hadoopVersion, fsUri = args
            j_obj = get_java_class(self.j_cls_name)(hadoopVersion, fsUri)
        elif len(args) == 3:
            hadoopVersion, fsUri, configuration = args
            j_obj = get_java_class(self.j_cls_name)(hadoopVersion, fsUri, configuration.get_j_obj())
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(HadoopFileSystem, self).__init__(j_obj)


class S3FileSystem(BaseFileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.S3FileSystem'

    def __init__(self, *args):
        j_obj = None
        if len(args) == 1:
            j_obj = args[0]
        elif len(args) == 2:
            s3Version, endPoint, bucketName, accessKey, secretKey, pathStyleAccess = args
            j_obj = get_java_class(self.j_cls_name)(s3Version, endPoint, bucketName, accessKey, secretKey, pathStyleAccess)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(S3FileSystem, self).__init__(j_obj)


class S3HadoopFileSystem(S3FileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.S3HadoopFileSystem'

    def __init__(self, *args):
        j_obj = None
        if len(args) == 1:
            j_obj = args[0]
        elif len(args) == 6:
            s3HadoopVersion, endPoint, bucketName, accessKey, secretKey, pathStyleAccess = args
            j_obj = get_java_class(self.j_cls_name)(s3HadoopVersion, endPoint, bucketName, accessKey, secretKey, pathStyleAccess)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(S3HadoopFileSystem, self).__init__(j_obj)


class S3PrestoFileSystem(S3FileSystem):
    j_cls_name = 'com.alibaba.alink.common.io.filesystem.S3PrestoFileSystem'

    def __init__(self, *args):
        j_obj = None
        if len(args) == 1:
            j_obj = args[0]
        elif len(args) == 6:
            s3PrestoVersion, endPoint, bucketName, accessKey, secretKey, pathStyleAccess = args
            j_obj = get_java_class(self.j_cls_name)(s3PrestoVersion, endPoint, bucketName, accessKey, secretKey, pathStyleAccess)
        if j_obj is None:
            raise Exception("Cannot initialize class with args: ", args)
        super(S3PrestoFileSystem, self).__init__(j_obj)
