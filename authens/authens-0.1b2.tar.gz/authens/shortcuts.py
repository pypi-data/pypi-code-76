"""Helper functions to get CAS metadata and create CAS accounts."""

# TODO: make the python-ldap dependency optional
import ldap
from django.conf import settings
from django.contrib.auth import get_user_model

from authens import conf as default_conf
from authens.models import CASAccount, OldCASAccount
from authens.utils import parse_entrance_year

User = get_user_model()


def _extract_ldap_info(entry, field):
    dn, attrs = entry
    return attrs[field][0].decode("utf-8")


def fetch_cas_account(cas_login):
    """Issue an LDAP connection to retrieve metadata associated to a CAS account."""

    # Don't trust the user! Only accept alphanumeric account names.
    if not cas_login.isalnum():
        raise ValueError("Illegal CAS login: {}".format(cas_login))

    ldap_url = getattr(settings, "LDAP_SERVER_URL", default_conf.LDAP_SERVER_URL)
    ldap_obj = ldap.initialize(ldap_url)
    res = ldap_obj.search_s(
        "dc=spi,dc=ens,dc=fr",
        ldap.SCOPE_SUBTREE,
        "(uid={})".format(cas_login),
        ["uid", "cn", "homeDirectory"],
    )
    if not res:
        return None

    if len(res) != 1:
        raise RuntimeError("LDAP returned too many results: {}".format(res))
    (res,) = res

    assert _extract_ldap_info(res, "uid") == cas_login
    return {
        "cn": _extract_ldap_info(res, "cn"),
        "entrance_year": parse_entrance_year(_extract_ldap_info(res, "homeDirectory")),
    }


def register_cas_account(user: User, cas_login: str) -> CASAccount:
    """Register a user as a CAS user and return the newly created CASAccount."""

    if not cas_login:
        raise ValueError("cas_login must be non-empty")
    if CASAccount.objects.filter(cas_login=cas_login).exists():
        raise ValueError("A CAS account named '{}' exists already".format(cas_login))
    if CASAccount.objects.filter(user=user).exists():
        raise ValueError("User '{}' already has a CAS account".format(user))
    if OldCASAccount.objects.filter(user=user).exists():
        raise ValueError("User '{}' has an old CAS account".format(user))

    ldap_info = fetch_cas_account(cas_login)
    if ldap_info is None:
        raise ValueError("There is no LDAP user for id '{}'".format(cas_login))

    entrance_year = ldap_info["entrance_year"]
    return CASAccount.objects.create(
        user=user, cas_login=cas_login, entrance_year=entrance_year
    )
