'''_2107.py

ShaftFromCAD
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2091
from mastapy._internal.python_net import python_net_import

_SHAFT_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ShaftFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftFromCAD',)


class ShaftFromCAD(_2091.AbstractShaftFromCAD):
    '''ShaftFromCAD

    This is a mastapy class.
    '''

    TYPE = _SHAFT_FROM_CAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_assembly(self) -> 'bool':
        '''bool: 'CreateAssembly' is the original name of this property.'''

        return self.wrapped.CreateAssembly

    @create_assembly.setter
    def create_assembly(self, value: 'bool'):
        self.wrapped.CreateAssembly = bool(value) if value else False

    @property
    def outer_diameter(self) -> 'float':
        '''float: 'OuterDiameter' is the original name of this property.'''

        return self.wrapped.OuterDiameter

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value else 0.0

    @property
    def inner_diameter(self) -> 'float':
        '''float: 'InnerDiameter' is the original name of this property.'''

        return self.wrapped.InnerDiameter

    @inner_diameter.setter
    def inner_diameter(self, value: 'float'):
        self.wrapped.InnerDiameter = float(value) if value else 0.0
