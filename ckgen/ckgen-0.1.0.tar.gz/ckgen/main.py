from fortlab import Fortlab

from ckgen.mpasocn import MPASOcnKernel
from ckgen.atm import AtmKernel

class CESMKGen(Fortlab):

    _name_ = "ckgen"
    _version_ = "0.1.0"
    _description_ = "Microapp CESM Fortran Kernel Generator"
    _long_description_ = "Microapp CESM Fortran Kernel Generator"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/ckgen"
    _builtin_apps_ = [MPASOcnKernel, AtmKernel]

    def __init__(self):
        pass
