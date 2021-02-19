"""Added for backwards compatibility"""

from new_era.peristaltic_pump import PeristalticPump, NewEraPeristalticPumpInterface
import warnings

warnings.warn(
            'depreciated, instead use: from new_era.peristaltic_pump import PeristalticPump',
            DeprecationWarning,
            stacklevel=2,
        )
