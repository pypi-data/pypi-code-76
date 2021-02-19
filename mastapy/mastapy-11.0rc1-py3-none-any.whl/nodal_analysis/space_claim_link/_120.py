'''_120.py

SpaceClaimSettings
'''


from mastapy._internal import constructor
from mastapy.utility import _1348
from mastapy._internal.python_net import python_net_import

_SPACE_CLAIM_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis.SpaceClaimLink', 'SpaceClaimSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('SpaceClaimSettings',)


class SpaceClaimSettings(_1348.PerMachineSettings):
    '''SpaceClaimSettings

    This is a mastapy class.
    '''

    TYPE = _SPACE_CLAIM_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpaceClaimSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_space_claim_calls_before_restart(self) -> 'int':
        '''int: 'NumberOfSpaceClaimCallsBeforeRestart' is the original name of this property.'''

        return self.wrapped.NumberOfSpaceClaimCallsBeforeRestart

    @number_of_space_claim_calls_before_restart.setter
    def number_of_space_claim_calls_before_restart(self, value: 'int'):
        self.wrapped.NumberOfSpaceClaimCallsBeforeRestart = int(value) if value else 0

    @property
    def folder_path(self) -> 'str':
        '''str: 'FolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderPath

    @property
    def licence(self) -> 'str':
        '''str: 'Licence' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Licence

    def edit_folder_path(self):
        ''' 'EditFolderPath' is the original name of this method.'''

        self.wrapped.EditFolderPath()
