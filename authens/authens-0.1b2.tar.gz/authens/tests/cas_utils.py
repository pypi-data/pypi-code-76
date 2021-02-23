class FakeCASClient:
    """Fake CAS Client that mimics CAS interactions.

    By default, always log in the same user 'johndoe' without checking the ticket.
    """

    def __init__(self, cas_login="johndoe", entrance_year=2019):
        self.cas_login = cas_login
        self.entrance_year = entrance_year

    def verify_ticket(self, ticket):
        """Dummy client that always log in the same user."""

        attributes = {
            "homeDirectory": "/users/{}/info/{}".format(
                self.entrance_year % 100, self.cas_login
            )
        }
        return self.cas_login, attributes, None


class FakeLDAPObject:
    """Fake object to be used in place of the result of `ldap.initialize`.

    Always return the same user information (configured at class initialization).
    """

    def __init__(self, cas_login: str, entrance_year: int):
        self.cas_login = cas_login
        self.entrance_year = entrance_year

    def search_s(self, base, scope, request, *args):
        if request != "(uid={})".format(self.cas_login):
            raise ValueError("I don't know how to answer this request!")

        home_dir = "/users/{}/info/{}".format(self.entrance_year % 100, self.cas_login)
        dn = "whatever"
        attrs = {
            "uid": [self.cas_login.encode("utf-8")],
            "cn": ["{}'s long name".format(self.cas_login).encode("utf-8")],
            "homeDirectory": [home_dir.encode("utf-8")],
        }
        return [(dn, attrs)]
