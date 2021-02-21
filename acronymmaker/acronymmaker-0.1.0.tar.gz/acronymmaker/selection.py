##############################################################################
#                                                                            #
#   AcronymMaker - Create awesome acronyms for your projects!                #
#   Copyright (c) 2020-2021 - Romain Wallon (romain.gael.wallon@gmail.com)   #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU General Public License as published by     #
#   the Free Software Foundation, either version 3 of the License, or        #
#   (at your option) any later version.                                      #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                     #
#   See the GNU General Public License for more details.                     #
#                                                                            #
#   You should have received a copy of the GNU General Public License        #
#   along with this program.                                                 #
#   If not, see <https://www.gnu.org/licenses/>.                             #
#                                                                            #
##############################################################################


"""
This module provides different strategies for selecting letters from the words
to create acronyms for.

Selection strategies are functions taking a non-empty word (string) as
argument, and returning a set containing the letters selected from this word.

Selection strategies may also be implemented with custom callable objects
respecting the contract described above.
"""


from typing import Set


def _check_not_empty(word: str) -> str:
    """
    Checks whether a word is not empty, and raises a ValueError when this
    is not the case.

    :param word: The word to check.

    :return: The given word, if and only if it is not empty.

    :raises ValueError: If the given word is empty.
    """
    if word != '':
        return word
    raise ValueError('Cannot select letters from an empty word')


def select_first_letter(word: str) -> Set[str]:
    """
    Implements the letter selection strategy consisting in selecting only the
    first letter of a word.

    :param word: The word to select letters from.

    :return: The set containing the first letter of the word.

    :raises ValueError: If the given word is empty.
    """
    return set(_check_not_empty(word)[0])


def select_all_letters(word: str) -> Set[str]:
    """
    Implements the letter selection strategy consisting in selecting all the
    letters of a word.

    :param word: The word to select letters from.

    :return: The set containing all the letters of the word.

    :raises ValueError: If the given word is empty.
    """
    return set(_check_not_empty(word))
