"""
AMIE packets relating to projects
"""

from .base import Packet


class DataProjectCreate(Packet):
    _packet_type = 'data_project_create'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID']
    _data_keys_not_required_in_reply = ['GlobalID', 'PersonID']
    _data_keys_allowed = ['DnList']


class NotifyProjectCreate(Packet):
    _packet_type = 'notify_project_create'
    _expected_reply = [{'type': 'data_project_create', 'timeout': 30240}]
    _data_keys_required = [
        'GrantNumber',
        'PfosNumber',
        'PiOrgCode',
        'PiPersonID',
        'PiRemoteSiteLogin',
        'ProjectID',
        'ProjectTitle',
        'ResourceList',
        'ServiceUnitsAllocated',
        'StartDate'
    ]
    _data_keys_not_required_in_reply = [
        'GrantNumber',
        'PfosNumber',
        'PiOrgCode',
        'ProjectTitle',
        'ResourceList',
        'ServiceUnitsAllocated',
        'StartDate'
    ]
    _data_keys_allowed = [
        'Abstract',
        'AcademicDegree',
        'AllocationType',
        'EndDate',
        'NsfStatusCode',
        'PiBusinessPhoneComment',
        'PiBusinessPhoneExtension',
        'PiBusinessPhoneNumber',
        'PiCity',
        'PiCountry',
        'PiDepartment',
        'PiDnList',
        'PiEmail',
        'PiFax',
        'PiFirstName',
        'PiGlobalID',
        'PiHomePhoneComment',
        'PiHomePhoneExtension',
        'PiHomePhoneNumber',
        'PiLastName',
        'PiMiddleName',
        'PiOrganization',
        'PiPosition',
        'PiRequestedLoginList',
        'PiState',
        'PiStreetAddress',
        'PiStreetAddress2',
        'PiTitle',
        'PiUID',
        'PiZip',
        'ProjectGID',
        'ResourceLogin',
        'RoleList',
        'Sfos',
    ]


class NotifyProjectInactivate(Packet):
    _packet_type = 'notify_project_inactivate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = [
        'Comment', 'PersonID', 'ProjectID', 'ResourceList'
    ]
    _data_keys_allowed = []


class NotifyProjectReactivate(Packet):
    _packet_type = 'notify_project_reactivate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = [
        'Comment', 'PersonID', 'ProjectID', 'ResourceList'
    ]
    _data_keys_allowed = []


class RequestProjectCreate(Packet):
    _packet_type = 'request_project_create'
    _expected_reply = [{'type': 'notify_project_create', 'timeout': 30240}]
    _data_keys_required = [
        'AllocationType',
        'EndDate',
        'GrantNumber',
        'PfosNumber',
        'PiFirstName',
        'PiLastName',
        'PiOrganization',
        'PiOrgCode',
        'StartDate',
        'ResourceList',
        'RecordID',
        'ServiceUnitsAllocated',
    ]
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = [
        'Abstract',
        'AcademicDegree',
        'AllocatedResource',
        'BoardType',
        'ChargeNumber',
        'CitizenshipList',
        'CitizenshipList',
        'GrantType',
        'NsfStatusCode',
        'PiBusinessPhoneComment',
        'PiBusinessPhoneExtension',
        'PiBusinessPhoneNumber',
        'PiCity',
        'PiCountry',
        'PiDepartment',
        'PiDnList',
        'PiEmail',
        'PiFax',
        'PiGlobalID',
        'PiHomePhoneComment',
        'PiHomePhoneExtension',
        'PiHomePhoneNumber',
        'PiMiddleName',
        'PiPersonID',
        'PiRequestedLoginList',
        'PiState',
        'PiStreetAddress',
        'PiStreetAddress2',
        'PiTitle',
        'PiZip',
        'ProjectID',
        'ProjectTitle',
        'RequestType',
        'RoleList',
        'Sfos',
        'SitePersonId',
    ]


class RequestProjectInactivate(Packet):
    _packet_type = 'request_project_inactivate'
    _expected_reply = [{'type': 'notify_project_inactivate', 'timeout': 30240}]
    _data_keys_required = ['ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['Comment',
                          'AllocatedResource',
                          'GrantNumber',
                          'StartDate',
                          'EndDate',
                          'ServiceUnitsAllocated',
                          'ServiceUnitsRemaining',
                          ]


class RequestProjectReactivate(Packet):
    _packet_type = 'request_project_reactivate'
    _expected_reply = [{'type': 'notify_project_reactivate', 'timeout': 30240}]
    _data_keys_required = ['ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['PersonID',
                          'Comment',
                          'AllocatedResource',
                          'GrantNumber',
                          'StartDate',
                          'EndDate',
                          'ServiceUnitsAllocated',
                          'ServiceUnitsRemaining'
                          ]
