"""Core of the satisfaction rate metric.

This part of the process use a numeric scale.
Therefore, if the original input was a textual scale, it is necessary to use this metric to transform to numeric scale.

Methods:
____________
    * calculate_satisfaction_rate - Calculates the satisfaction rate based on the bot scale.
"""

__all__ = [
    "calculate_satisfaction_rate"
]

from .calculate_satisfaction_rate import calculate_satisfaction_rate
