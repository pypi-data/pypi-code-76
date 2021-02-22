'''_1024.py

ShaftHubConnectionRating
'''


from typing import List

from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors import _975
from mastapy.detailed_rigid_connectors.splines import (
    _978, _981, _985, _988,
    _989, _996, _1003, _1008
)
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.keyed_joints import _1025
from mastapy.detailed_rigid_connectors.interference_fits import _1033
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Rating', 'ShaftHubConnectionRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionRating',)


class ShaftHubConnectionRating(_0.APIBase):
    '''ShaftHubConnectionRating

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def additional_rating_information(self) -> 'str':
        '''str: 'AdditionalRatingInformation' is the original name of this property.'''

        return self.wrapped.AdditionalRatingInformation

    @additional_rating_information.setter
    def additional_rating_information(self, value: 'str'):
        self.wrapped.AdditionalRatingInformation = str(value) if value else None

    @property
    def joint_design(self) -> '_975.DetailedRigidConnectorDesign':
        '''DetailedRigidConnectorDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _975.DetailedRigidConnectorDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to DetailedRigidConnectorDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_custom_spline_joint_design(self) -> '_978.CustomSplineJointDesign':
        '''CustomSplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _978.CustomSplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to CustomSplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_din5480_spline_joint_design(self) -> '_981.DIN5480SplineJointDesign':
        '''DIN5480SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _981.DIN5480SplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to DIN5480SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_gbt3478_spline_joint_design(self) -> '_985.GBT3478SplineJointDesign':
        '''GBT3478SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _985.GBT3478SplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to GBT3478SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_iso4156_spline_joint_design(self) -> '_988.ISO4156SplineJointDesign':
        '''ISO4156SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _988.ISO4156SplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to ISO4156SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_jisb1603_spline_joint_design(self) -> '_989.JISB1603SplineJointDesign':
        '''JISB1603SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _989.JISB1603SplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to JISB1603SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_sae_spline_joint_design(self) -> '_996.SAESplineJointDesign':
        '''SAESplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _996.SAESplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to SAESplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_spline_joint_design(self) -> '_1003.SplineJointDesign':
        '''SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1003.SplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_standard_spline_joint_design(self) -> '_1008.StandardSplineJointDesign':
        '''StandardSplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1008.StandardSplineJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to StandardSplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_keyed_joint_design(self) -> '_1025.KeyedJointDesign':
        '''KeyedJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1025.KeyedJointDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to KeyedJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_interference_fit_design(self) -> '_1033.InterferenceFitDesign':
        '''InterferenceFitDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1033.InterferenceFitDesign.TYPE not in self.wrapped.JointDesign.__class__.__mro__:
            raise CastException('Failed to cast joint_design to InterferenceFitDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.JointDesign.__class__)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
