from django.contrib.auth import get_user_model
from django.db import transaction

from authens.models import CASAccount, OldCASAccount
from authens.signals import post_cas_connect
from authens.utils import get_cas_client, parse_entrance_year

UserModel = get_user_model()


class ENSCASError(Exception):
    pass


class ENSCASBackend:
    """AuthENS CAS authentication backend.

    Implement standard CAS v3 authentication and handles username clashes with non-CAS
    accounts and potential old CAS accounts.

    Every user connecting via CAS is given an `authens.models.CASAccount` instance which
    remembers her CAS login and her entrance year (the year her CAS account was
    created).
    At each connection, we search for a CAS account with the given CAS login and create
    one if none exists. In case the CAS account's entrance year does not match the
    entrance year given by CAS, it means it is a old account and it must be deleted. The
    corresponding user can still connect using regular Django authentication.
    """

    def authenticate(self, request, ticket=None):
        cas_client = get_cas_client(request)
        cas_login, attributes, _ = cas_client.verify_ticket(ticket)

        if cas_login is None:
            # Authentication failed
            return None
        cas_login = self.clean_cas_login(cas_login)

        if request:
            request.session["CASCONNECTED"] = True

        return self._get_or_create(cas_login, attributes)

    def clean_cas_login(self, cas_login):
        return cas_login.strip().lower()

    def get_free_username(self, cas_login, attributes):
        """Find an available username for a new user.

        If you override this method, make sure it returns a username that is not taken
        by any existing user.
        This method will be called from within an atomic database transation (don't
        worry about data races).
        """

        # Ideally we can have username = cas_login.
        if not UserModel.objects.filter(username=cas_login).exists():
            return cas_login

        # Otherwise, add a numerical suffix.

        # If there was a numerical suffix already, remove it:
        # https://git.eleves.ens.fr/klub-dev-ens/authens/issues/5
        i = len(cas_login) - 1
        while i >= 0 and cas_login[i] in "0123456789":
            i -= 1
        radical = cas_login[: i + 1]

        # Find an integer i such that radical + str(i) is not taken.
        taken = UserModel.objects.values_list("username", flat=True)
        taken = taken.filter(username__startswith=radical)
        i = 2
        while radical + str(i) in taken:
            i += 1
        return radical + str(i)

    def create_user(self, username, attributes):
        """Create a CAS user, base method that can be overrided to add more
        information.
        """

        email = attributes.get("email")
        return UserModel.objects.create_user(username=username, email=email)

    def _get_or_create(self, cas_login, attributes):
        """Handles account retrieval, creation and invalidation as described above.

        - If no CAS account exists, create one;
        - If a CAS account exists, but with the wrong entrance year, convert it to
        an OldCASAccount instance, and create a fresh CAS Account with the correct year.
        - If a matching CAS account exists, retrieve it.
        """

        entrance_year = parse_entrance_year(attributes.get("homeDirectory"))
        if entrance_year is None:
            raise ENSCASError("Entrance year not available")

        account_created = False
        with transaction.atomic():
            try:
                user = UserModel.objects.get(cas_account__cas_login=cas_login)
                if user.cas_account.entrance_year != entrance_year:
                    OldCASAccount.objects.create(
                        user=user,
                        entrance_year=user.cas_account.entrance_year,
                        cas_login=cas_login,
                    )
                    user.cas_account.delete()
                    user = None
            except UserModel.DoesNotExist:
                user = None

            if user is None:
                username = self.get_free_username(cas_login, attributes)
                user = self.create_user(username, attributes)
                CASAccount.objects.create(
                    user=user, entrance_year=entrance_year, cas_login=cas_login
                )
                account_created = True

        post_cas_connect.send(
            UserModel,
            instance=user,
            created=account_created,
            cas_login=cas_login,
            attributes=attributes,
        )
        return user

    # Django boilerplate.
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class OldCASBackend:
    """Authentication backend for old CAS accounts.

    Given a CAS login, an entrance year and a password, first finds the matching
    OldCASAccount instance (if it exists), then checks the given password with
    the user associated to this account.
    """

    def authenticate(self, request, cas_login=None, password=None, entrance_year=None):
        if cas_login is None or password is None or entrance_year is None:
            return

        try:
            try:
                cas_acc = CASAccount.objects.get(
                    cas_login=cas_login, entrance_year=entrance_year
                )
                user = cas_acc.user
            except CASAccount.DoesNotExist:
                old_cas_acc = OldCASAccount.objects.get(
                    cas_login=cas_login, entrance_year=entrance_year
                )
                user = old_cas_acc.user
        except OldCASAccount.DoesNotExist:
            # As in Django's ModelBackend, we run the password hasher once
            # to mitigate timing attacks
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        # Taken from Django's ModelBackend
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    # Django boilerplate.
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
