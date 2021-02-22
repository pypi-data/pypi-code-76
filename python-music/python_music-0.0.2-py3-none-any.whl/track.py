#
#  Python-music
#  Python music module.
#  Copyright Medilocus 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from typing import Any, List, Tuple
from .constants import *
from .elements import Note


class Track:
    """
    Single track class.
    Contains notes, tempo changes, time signatures, ...
    """

    elements: List[Any]

    default_tsig: Tuple[int] = (4, 4)
    default_tempo: float = 120

    def __init__(self) -> None:
        """
        Initializes track.
        """
        self.elements = []

    def __repr__(self) -> str:
        return f"<Track object, {len(self.elements)} elements>"

    @classmethod
    def from_elements(cls, elements: Tuple[Any]):
        """
        Initializes track with elements.
        :param elements: Tuple of elements.
        """
        track = cls()
        for e in elements:
            track.add_element(e)
        return track

    def add_element(self, element):
        """
        Adds an element.
        :param element: Element to add.
        """
        self.elements.append(element)
