"""Core of the resolution rate metric.

Resolution daily rate is defined as the division between amount of users that have some resolution by total users.

Methods:
____________
    * resolution_metric - Calculates the satisfaction rate based on the bot scale.
    * daily_resolution - Return daily resolution metric for given array.
"""

__all__ = [
    "resolution_metric",
    "daily_resolution"
]
from .metrics import (resolution_metric,
                      daily_resolution)

