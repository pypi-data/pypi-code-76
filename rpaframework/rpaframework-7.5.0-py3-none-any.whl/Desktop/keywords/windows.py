from RPA.Desktop.keywords import LibraryContext, keyword

if utils.is_windows():
    import ctypes
    import win32api
    import win32com.client
    import win32con
    import win32security
    import pywinauto
    import win32gui
    from comtypes import COMError


class WindowsKeywords(LibraryContext):
    pass
