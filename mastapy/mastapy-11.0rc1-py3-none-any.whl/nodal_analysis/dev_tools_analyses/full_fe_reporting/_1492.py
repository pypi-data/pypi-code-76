'''_1492.py

PoissonRatioOrthotropicComponents
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_POISSON_RATIO_ORTHOTROPIC_COMPONENTS = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'PoissonRatioOrthotropicComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('PoissonRatioOrthotropicComponents',)


class PoissonRatioOrthotropicComponents(_0.APIBase):
    '''PoissonRatioOrthotropicComponents

    This is a mastapy class.
    '''

    TYPE = _POISSON_RATIO_ORTHOTROPIC_COMPONENTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PoissonRatioOrthotropicComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def xy(self) -> 'float':
        '''float: 'XY' is the original name of this property.'''

        return self.wrapped.XY

    @xy.setter
    def xy(self, value: 'float'):
        self.wrapped.XY = float(value) if value else 0.0

    @property
    def yz(self) -> 'float':
        '''float: 'YZ' is the original name of this property.'''

        return self.wrapped.YZ

    @yz.setter
    def yz(self, value: 'float'):
        self.wrapped.YZ = float(value) if value else 0.0

    @property
    def xz(self) -> 'float':
        '''float: 'XZ' is the original name of this property.'''

        return self.wrapped.XZ

    @xz.setter
    def xz(self, value: 'float'):
        self.wrapped.XZ = float(value) if value else 0.0
