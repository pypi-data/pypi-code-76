import sys

# This is the ovito.plugins Python package. It hosts the C++ extension modules of OVITO.

# The C++ extension modules are, however, located in a different directory when OVITO is installed
# as a conda package. For the time being, we use hardcoded, relative paths to find them.
#
# Platform-dependent paths where this Python module is located:
#   Linux:   ${PREFIX}/lib/pythonX.Y/site-packages/ovito/plugins/
#   Windows: ${PREFIX}/Lib/site-packages/ovito/plugins/
#   macOS:   ${PREFIX}/lib/pythonX.Y/site-packages/ovito/plugins/
#
# Platform-dependent paths where the native C++ shared libraries are located:
#   Linux:   ${PREFIX}/lib/ovito/plugins/
#   Windows: ${PREFIX}/Library/bin/
#   macOS:   ${PREFIX}/lib/ovito/plugins/
#

# The OVITO plugins are shared libraries, and we need to specify the path where they are found:
if sys.platform.startswith('darwin'):
    # macOS
    __path__[0] += "/../../../../ovito/plugins"
elif sys.platform.startswith('win32'):
    # Windows
    __path__[0] += "\\..\\..\\..\\..\\Library\\bin"
else:
    # Linux
    __path__[0] += "/../../../../ovito/plugins"

# On Windows, extension modules for the Python interpreter have a .pyd file extension.
# Our OVITO plugins, however, have the standard .ovito.dll extension. We therefore need to implement
# a custom file entry finder and hook it into the import machinery of Python.
# It specifically handles the OVITO plugin path and allows to load extension modules with .ovito.dll
# extension instead of .pyd.
if sys.platform.startswith('win32'):
    import importlib.machinery
    def OVITOPluginFinderHook(path):
        if path == __path__[0]:
            return importlib.machinery.FileFinder(path, (importlib.machinery.ExtensionFileLoader, ['.ovito.dll']))
        raise ImportError()
    sys.path_hooks.insert(0, OVITOPluginFinderHook)
