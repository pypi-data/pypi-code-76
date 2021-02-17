
import os
import ctypes
from pathlib import Path
import re
import sys
import RobotRaconteur as RR
import uuid
import numpy as np
import stat
import errno

if sys.platform == 'win32':
    import msvcrt
else:
    import fcntl

def _get_user_data_path():
    if sys.platform == 'win32':
        buf = ctypes.create_unicode_buffer(1024)
        assert ctypes.windll.shell32.SHGetFolderPathW(None,0x001c | 0x8000, None, 0, buf) == 0
        p = Path(buf.value).joinpath("RobotRaconteur")
        p.mkdir(parents = True, exist_ok = True)
        return p
    else:
        path1 = os.environ["HOME"]
        assert path1 is not None, "Home directory not set"
        p = Path(path1).joinpath(".config").joinpath("RobotRaconteur")
        p.mkdir(parents = True, exist_ok = True)
        return p

def _get_user_run_path():
    if sys.platform == 'win32':
        buf = ctypes.create_unicode_buffer(1024)
        assert ctypes.windll.shell32.SHGetFolderPathW(None,0x001c | 0x8000, None, 0, buf) == 0
        p = Path(buf.value).joinpath("RobotRaconteur").joinpath("run")
        p.mkdir(parents = True, exist_ok = True)
        return p
    elif sys.platform == 'darwin':
        u = os.getuid()
        if u == 0:
            path = Path("/var/run/robotraconteur/root")
            path.mkdir(parents = True, exist_ok = True)
            path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        else:
            path1 = os.environ["TMPDIR"]
            assert path1 is not None, "Could not activate system for local identifier manager"
            path = Path(path1).parent.joinpath("C")
            assert path.is_dir(), "Could not activate system for local identifier manager"
            path = path.joinpath("robotraconteur")
        path.mkdir(parents = True, exist_ok = True)
        return path
    else:
        u = os.getuid()
        if u == 0:
            path = Path("/var/run/robotraconteur/root")
            path.mkdir(parents = True, exist_ok = True)
            path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        else:
            path1 = os.environ["XDG_RUNTIME_DIR"]
            assert path1 is not None, "Could not activate system for local identifier manager"
            path = Path(path1)
            assert path.is_dir(), "Could not activate system for local identifier manager"
            path = path.joinpath("robotraconteur")
        path.mkdir(parents = True, exist_ok = True)
        return path

def _get_user_identifier_path():
    p = _get_user_data_path().joinpath("identifiers")
    p.mkdir(parents = True, exist_ok = True)
    return p

def _open_lock_write(file_path):    
    if sys.platform == "win32":
        fname_buf = ctypes.create_unicode_buffer(str(file_path))
        h = ctypes.windll.kernel32.CreateFileW(fname_buf, 0x80000000 | 0x40000000, 0x00000001, None, 4, 0x00000080)
        if h == -1:
            win_err = ctypes.windll.kernel32.GetLastError()
            if win_err ==  32:
                raise RR.InvalidOperationException("Identifier name in use")
            else:
                assert False, "Could not activate system for local identifier manager"
        fd = msvcrt.open_osfhandle(h,os.O_APPEND | os.O_TEXT)
        f = os.fdopen(fd, "r+",encoding="ascii")
        return f
    else:
        fd1 = os.open(str(file_path),os.O_CLOEXEC | os.O_RDWR | os.O_APPEND | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)        
        f = os.fdopen(fd1, "r+",encoding="ascii")
        fcntl.lockf(f,fcntl.LOCK_EX)
        return f
        

class LocalIdentifiersManager(object):

    def __init__(self,node,client_object = None):
        self._node = node
        self._client_object = client_object

    def GetIdentifierForNameAndLock(self, category, name):
        
        assert re.match("^[a-zA-Z][a-zA-Z0-9_\\.\\-]*$",name) is not None, "Invalid identifier name"
        category2=category.lower()

        p1 = _get_user_identifier_path().joinpath(category)
        p1.mkdir(parents = True, exist_ok = True)
        p = p1.joinpath(name)

        if sys.platform == "win32":
            f = _open_lock_write(p)
        else:
            p_lock1 = _get_user_run_path().joinpath("identifiers").joinpath(category)
            p_lock1.mkdir(parents = True, exist_ok = True)
            p_lock = p_lock1.joinpath(name + ".pid")
            f_run = _open_lock_write(p_lock)
            f_run.seek(0,0)
            f_run.truncate()
            f_run.write(str(os.getpid()))

            try:
                f = _open_lock_write(p)
            except OSError as x:
                if x.errno == errno.EROFS:
                    f = open(p,'r',encoding="ascii")
                else:
                    raise

        f.seek(0,0)
        f_text = f.read()
        if len(f_text) == 0:
            ident_uuid = uuid.uuid4()
            f.write("{" + str(ident_uuid) + "}")
        else:
            ident_uuid = uuid.UUID(str(f_text))

        ident_type = self._node.GetStructureType("com.robotraconteur.identifier.Identifier",self._client_object)
        uuid_dtype = self._node.GetNamedArrayDType("com.robotraconteur.uuid.UUID",self._client_object)
        ret = ident_type()
        ret.name = name
        ret.uuid = np.zeros((1,),dtype=uuid_dtype)
        ret.uuid["uuid_bytes"] = np.frombuffer(ident_uuid.bytes,dtype=np.uint8)
        if sys.platform == "win32":
            return ret,f
        else:
            f.close()
            return ret,f_run
