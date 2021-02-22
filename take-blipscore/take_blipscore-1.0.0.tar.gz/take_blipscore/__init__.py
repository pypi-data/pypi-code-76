"""This project calculates the BlipScore for BLiP smart contacts.

The Blip Score propose a unique metric to indicate the quality of smart contact perceived by users.
In order to gather the user perception, the Blip Score use:
 * Satisfaction rate: metric that collect the user evaluation on the smart contact
 * Resolution rate: analyse if the user is having resolution while interacting on the smart contact

Methods:
_________
    * run: Run BlipScore for given metrics.
"""

from __future__ import annotations

__author__ = "squad XD"
__version__ = "1.0.0"

from .run import run
