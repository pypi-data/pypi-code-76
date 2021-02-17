import json
import pytest

# This one includes UserFavoriteColor: blue
# to make sure that we handle unexpected data properly
DEMO_JSON_PKT_1 = {
    'DATA_TYPE': 'Packet',
    'type_id': 16,
    'type': 'request_account_create',
    'header': {
        'expected_reply_list': [
            {'type': 'notify_account_create', 'timeout': 30240}
        ],
        'packet_id': 1,
        'trans_rec_id': 87139097,
        'transaction_id': 244206,
        'packet_rec_id': 174709745,
        'local_site_name': 'PSC',
        'remote_site_name': 'SDSC',
        'originating_site_name': 'SDSC',
        'outgoing_flag': False,
        'transaction_state': 'in-progress',
        'packet_state': None,
    },
    'body': {
        'AcademicDegree': [
            {'Field': 'Computer and Computation Research', 'Degree': 'MS'}
        ],
        'SitePersonId': [
            {'PersonID': 'vraunak', 'Site': 'X-PORTAL'},
            {'PersonID': 'vraunak', 'Site': 'XD-ALLOCATIONS'},
            {'PersonID': 'RAUNAK12P', 'Site': 'PSC'},
            {'PersonID': '112157', 'Site': 'SDSC'}
        ],
        'RoleList': ['allocation_manager'],
        'UserDnList': [
            '/C=US/O=Pittsburgh Supercomputing Center/CN=Vikas Raunak',
            '/C=US/O=National Center for Supercomputing Applications/CN=Vikas Raunak'
        ],
        'UserPersonID': '112157',
        'NsfStatusCode': 'GS',
        'UserOrgCode': '0032425',
        'UserOrganization': 'Carnegie Mellon University',
        'UserTitle': '',
        'UserDepartment': 'SCS',
        'UserLastName': 'Raunak',
        'UserMiddleName': '',
        'UserFirstName': 'Vikas',
        'UserCountry': '9US',
        'UserState': 'PA',
        'UserZip': '15213',
        'UserStreetAddress': 'Craig Street, Carnegie Mellon University, Pittsburgh 15213',
        'UserCity': 'Pittsburgh',
        'UserEmail': 'vraunak@andrew.cmu.edu',
        'UserBusinessPhoneNumber': '4124781149',
        'UserGlobalID': '71691',
        'UserFavoriteColor': 'blue',
        'AllocatedResource': 'comet-gpu.sdsc.xsede',
        'UserRequestedLoginList': [''],
        'ResourceList': ['comet-gpu.sdsc.xsede'],
        'UserPasswordAccessEnable': '1',
        'GrantNumber': 'IRI120015',
        'ProjectID': 'CMU139'
    }  # End body
}  # End packet 1

DEMO_JSON_PKT_2 = {
  "DATA_TYPE": "Packet",
  "type_id": 16,
  "type": "request_account_create",
  "header": {
    "expected_reply_list": [
      {
        "type": "notify_account_create",
        "timeout": 30240
      }
    ],
    "packet_id": 1,
    "trans_rec_id": 86860578,
    "transaction_id": 243873,
    "packet_rec_id": 174151086,
    'local_site_name': 'PSC',
    'remote_site_name': 'SDSC',
    'originating_site_name': 'SDSC',
    'outgoing_flag': False,
    'transaction_state': 'in-progress',
    'packet_state': None,
  },
  "body": {
    "AcademicDegree": [
      {
        "Field": "Biophysics",
        "Degree": "PhD"
      }
    ],
    "SitePersonId": [
      {
        "PersonID": "xizhang",
        "Site": "X-PORTAL"
      },
      {
        "PersonID": "xizhang",
        "Site": "XD-ALLOCATIONS"
      },
      {
        "PersonID": "114121",
        "Site": "SDSC"
      }
    ],
    "UserDnList": [
      "/C=US/O=Pittsburgh Supercomputing Center/CN=Xi Zhang 2",
      "/C=US/O=National Center for Supercomputing Applications/CN=Xi Zhang 2"
    ],
    "UserPersonID": "114121",
    "NsfStatusCode": "PD",
    "UserOrgCode": "0090910",
    "UserOrganization": "University of Michigan",
    "UserTitle": "",
    "UserDepartment": "Department of Computational Medicine and Bioinformatics",
    "UserLastName": "Zhang",
    "UserMiddleName": "",
    "UserFirstName": "Xi",
    "UserCountry": "9US",
    "UserState": "MI",
    "UserZip": "48197",
    "UserStreetAddress": "2353 TWIN LAKES DR APT TB",
    "UserCity": "Ypsilanti",
    "UserEmail": "xizha@umich.edu",
    "UserBusinessPhoneNumber": "734-773-2530",
    "UserGlobalID": "76716",
    "AllocatedResource": "comet.sdsc.xsede",
    "UserRequestedLoginList": [
      ""
    ],
    "ResourceList": [
      "comet.sdsc.xsede"
    ],
    "UserPasswordAccessEnable": "1",
    "GrantNumber": "MCB200078",
    "ProjectID": "MIA322"
  }  # End body
}  # End packet 2

DEMO_JSON_TXN = {
  "DATA_TYPE": "transaction",
  "transaction_id": "12",
  "originating_site_name": "PSC",
  "local_site_name": "PSC",
  "remote_site_name": "XSEDE",
  "state": "in_progress",
  "timestamp": "2020-06-05T09:25:37",
  "DATA": [
      DEMO_JSON_PKT_1,
      DEMO_JSON_PKT_2
  ]
}

DEMO_JSON_PKT_LIST = {
  "message": '',
  "result": [
      DEMO_JSON_PKT_1,
      DEMO_JSON_PKT_2
  ]
}
