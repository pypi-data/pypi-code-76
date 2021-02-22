from requests.models import default_hooks
from graviteeio_cli.http_client.apim.api import Api_Action
import json
import logging

from graviteeio_cli.http_client.http_client import HttpClient
from graviteeio_cli.core.config import GraviteeioConfig_apim

logger = logging.getLogger("client.config_client")


class ConfigClient:

    def __init__(self, config: GraviteeioConfig_apim, debug=False):
        self.httpClient = HttpClient("/management/{}configuration/", config)


Analytics
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/dashboards/?reference_type=PLATFORM
Type API
Type Application


API Portal Informations
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/apiheaders/

API Quality
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/quality-rules/

Authentication
https://nightly.gravitee.io/api/management/organizations/DEFAULT/configuration/identities/

https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/identities

https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/settings/


Categories
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/categories/

Client Registration
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/applications/registration/providers/


Meta
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/metadata/

settings
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/tags/
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/settings/

Theme
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/themes/default_hooks

Top-Api
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/top-apis/


GATEWAY
API Loggin
https://nightly.gravitee.io/api/management/organizations/DEFAULT/settings/

dictionaries
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/dictionaries

Sharding Tags
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/tags/

https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/entrypoints/

https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/groups

https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/settings/

Tenants
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/tenants/

User Management

user field
https://nightly.gravitee.io/api/management/organizations/DEFAULT/configuration/custom-user-fields

Groups
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/groups

Notification
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/default_hooks
[ {
  "id" : "USER_REGISTRATION_REQUEST",
  "label" : "User Registration Request",
  "description" : "Triggered when a new user is created and automatic validation is disabled",
  "scope" : "PORTAL",
  "category" : "USER"
}, {
  "id" : "USER_REGISTERED",
  "label" : "User Registered",
  "description" : "Triggered when an user is registered",
  "scope" : "PORTAL",
  "category" : "USER"
}, {
  "id" : "USER_CREATED",
  "label" : "User Created",
  "description" : "Triggered when an user is created",
  "scope" : "PORTAL",
  "category" : "USER"
}, {
  "id" : "USER_FIRST_LOGIN",
  "label" : "First Login",
  "description" : "Triggered when an user log in for the first time",
  "scope" : "PORTAL",
  "category" : "USER"
}, {
  "id" : "PASSWORD_RESET",
  "label" : "Password Reset",
  "description" : "Triggered when a password is reset",
  "scope" : "PORTAL",
  "category" : "USER"
}, {
  "id" : "NEW_SUPPORT_TICKET",
  "label" : "New Support Ticket",
  "description" : "Triggered when a new support ticket is created",
  "scope" : "PORTAL",
  "category" : "SUPPORT"
}, {
  "id" : "GROUP_INVITATION",
  "label" : "Group invitation",
  "description" : "Triggered when an user is invited in a group",
  "scope" : "PORTAL",
  "category" : "GROUP"
} ]
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/notifiers
[ {
  "id" : "default-email",
  "type" : "EMAIL",
  "name" : "Default Email Notifier"
}, {
  "id" : "default-webhook",
  "type" : "WEBHOOK",
  "name" : "Default Webhook Notifier"
} ]
https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/configuration/notificationsettings
[ {
  "referenceType" : "PORTAL",
  "referenceId" : "DEFAULT",
  "user" : "e689d719-789f-4967-89d7-19789f3967fa",
  "hooks" : [ ],
  "config_type" : "portal",
  "name" : "Portal Notification"
} ]
https://nightly.gravitee.io/api/management/organizations/DEFAULT/user/notifications
{
  "data" : [ ],
  "page" : {
    "current" : 1,
    "size" : 0,
    "per_page" : 0,
    "total_pages" : 0,
    "total_elements" : 0
  }
}

