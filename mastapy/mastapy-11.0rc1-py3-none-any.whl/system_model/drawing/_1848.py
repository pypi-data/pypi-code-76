'''_1848.py

ShaftDeflectionDrawingNodeItem
'''


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1118
from mastapy.system_model.analyses_and_results.system_deflections import _2331
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_DEFLECTION_DRAWING_NODE_ITEM = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ShaftDeflectionDrawingNodeItem')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftDeflectionDrawingNodeItem',)


class ShaftDeflectionDrawingNodeItem(_0.APIBase):
    '''ShaftDeflectionDrawingNodeItem

    This is a mastapy class.
    '''

    TYPE = _SHAFT_DEFLECTION_DRAWING_NODE_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftDeflectionDrawingNodeItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.'''

        return self.wrapped.Offset

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0

    @property
    def radial_deflection(self) -> 'float':
        '''float: 'RadialDeflection' is the original name of this property.'''

        return self.wrapped.RadialDeflection

    @radial_deflection.setter
    def radial_deflection(self, value: 'float'):
        self.wrapped.RadialDeflection = float(value) if value else 0.0

    @property
    def axial_deflection(self) -> 'float':
        '''float: 'AxialDeflection' is the original name of this property.'''

        return self.wrapped.AxialDeflection

    @axial_deflection.setter
    def axial_deflection(self, value: 'float'):
        self.wrapped.AxialDeflection = float(value) if value else 0.0

    @property
    def node_detail(self) -> '_1118.ForceAndDisplacementResults':
        '''ForceAndDisplacementResults: 'NodeDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1118.ForceAndDisplacementResults)(self.wrapped.NodeDetail) if self.wrapped.NodeDetail else None

    @property
    def section_to_the_left_side(self) -> '_2331.ShaftSectionSystemDeflection':
        '''ShaftSectionSystemDeflection: 'SectionToTheLeftSide' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2331.ShaftSectionSystemDeflection)(self.wrapped.SectionToTheLeftSide) if self.wrapped.SectionToTheLeftSide else None

    @property
    def section_to_the_right_side(self) -> '_2331.ShaftSectionSystemDeflection':
        '''ShaftSectionSystemDeflection: 'SectionToTheRightSide' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2331.ShaftSectionSystemDeflection)(self.wrapped.SectionToTheRightSide) if self.wrapped.SectionToTheRightSide else None
