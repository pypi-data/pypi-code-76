from distutils.core import setup, Extension, DEBUG

sfc_module = Extension('binstore', sources = ['module_bins.c'])
setup(name = 'binstore',
      version = '1.7',
      description = 'Python Package with Count C extension',
      ext_modules = [sfc_module],

      )
