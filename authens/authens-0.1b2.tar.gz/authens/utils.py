"""Internal utility functions used by authens."""
from urllib.parse import urlunparse

from cas import CASClient


def get_cas_client(request):
    """Return a CAS client configured for SPI's CAS."""
    return CASClient(
        version=3,
        service_url=urlunparse(
            (request.scheme, request.get_host(), request.path, "", "", "")
        ),
        server_url="https://cas.eleves.ens.fr/",
    )


def parse_entrance_year(home_dir):
    """Infer the entrance year of a CAS account from their home directory."""

    # The home directory of a user is of the form /users/YEAR/DEPARTMENT/CAS_LOGIN where
    # YEAR is a 2-digit number representing the entrance year of the student. We get the
    # entrance year from there.

    if home_dir is None:
        return None

    dirs = home_dir.split("/")
    if len(dirs) < 3 or not dirs[2].isdecimal() or dirs[1] != "users":
        raise ValueError("Invalid home directory: {}".format(home_dir))

    # Expand the 2-digit entrance year into 4 digits.
    # This will break in 2080.
    year = int(dirs[2])
    if year >= 80:
        return 1900 + year
    else:
        return 2000 + year
