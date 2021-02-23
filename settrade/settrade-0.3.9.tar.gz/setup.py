import sys
import platform
import distutils.sysconfig

from setuptools import setup, find_packages

platform_supported = False

dir_path = "src/settrade_open_api_uat/open_api"
lib_path = dir_path + "/lib"
wrapper_path = dir_path + "/wrapper"

py_ver = str(sys.version_info.major) + str(sys.version_info.minor)

if sys.platform == "win32":
    platform_supported = True

    if platform.architecture()[0] == "64bit":
        lib_path += "/windows_x64/python" + py_ver
    else:
        lib_path += "/windows_x86/python" + py_ver
elif sys.platform == "darwin":
    platform_supported = True
    lib_path += "/mac/python" + py_ver
elif sys.platform == "linux":
    platform_supported = True
    lib_path += "/linux/python" + py_ver

if not platform_supported:
    raise NotImplementedError(sys.platform)

setup(
    name="settrade",
    version="0.3.9",
    install_requires=["numpy"],
    packages=[
        "settrade.openapi",
        "settrade.openapi.account.investor",
        "settrade.openapi.account.marketrep",
        "settrade.openapi.user",
        "settrade.openapi.lib",
    ],
    package_dir={
        "settrade.openapi": wrapper_path,
        "settrade.openapi.account.investor": wrapper_path + "/account/investor",
        "settrade.openapi.account.marketrep": wrapper_path + "/account/marketrep",
        "settrade.openapi.user": wrapper_path + "/user",
        "settrade.openapi.lib": lib_path,
    },
    package_data={
        "": ["*.so", "*.pyd", "*.dll"]
    },
    python_requires=">=3.5, <3.9",
)
