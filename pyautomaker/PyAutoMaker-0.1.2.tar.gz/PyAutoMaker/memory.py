import ctypes
import win32api
import win32con
from ctypes import windll, wintypes


class processUtil:
    def __init__(self, target):
        self.__GetLastError = windll.kernel32["GetLastError"]
        self.__GetLastError.argtypes = ()
        self.__GetLastError.restype = (wintypes.DWORD)

        self.__OpenProcess = windll.kernel32["OpenProcess"]
        self.__OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        self.__OpenProcess.restype = (wintypes.HANDLE)

        self.__ReadProcessMemory = windll.kernel32["ReadProcessMemory"]
        self.__ReadProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPCVOID
                                             , wintypes.LPVOID, ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ulonglong))
        self.__ReadProcessMemory.restype = (wintypes.BOOL)


        self.__handle = self.__OpenProcess(win32con.MAXIMUM_ALLOWED, win32con.FALSE, target)


    def __del__(self):
        if self.__handle == None:
            return

        CloseHandle = windll.kernel32["CloseHandle"]
        CloseHandle.argtypes = (wintypes.HANDLE, )
        CloseHandle.restype = (wintypes.BOOL)

        CloseHandle(self.__handle)

    def read(self, addr, readSize):
        if self.__handle == None:
            return None

        buffer = (wintypes.BYTE * readSize)()
        baseAddr = wintypes.LPVOID(addr)
        numberOfBytesRead = ctypes.c_ulonglong()

        ret = self.__ReadProcessMemory(self.__handle, ctypes.cast(baseAddr, wintypes.LPCVOID), ctypes.cast(buffer, wintypes.LPVOID)
                                       , readSize, ctypes.byref(numberOfBytesRead))

        if ret == win32con.FALSE:
            #print("Read Error Code : {}".format(self.__GetLastError()))
            return None

        return bytearray(buffer)


if __name__ == "__main__":
    pass
