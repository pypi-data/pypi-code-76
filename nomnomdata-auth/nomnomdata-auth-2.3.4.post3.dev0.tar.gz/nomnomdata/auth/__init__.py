import dunamai as _dunamai

from .auth import NNDAuth, get_profiles
from .vars import DEFAULT_PROFILE

__version__ = _dunamai.get_version(
    "nomnomdata-auth", third_choice=_dunamai.Version.from_any_vcs
).serialize()
