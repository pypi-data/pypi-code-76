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
This module provides data structures used to represent disjunctions of words
(a.k.a. tokens) for which a letter has to appear in the acronyms being created.
"""


from collections import defaultdict
from typing import Callable, Dict, Iterator, List, Set
from unicodedata import normalize


class Token:
    """
    A Token represents a disjunction of words for which a letter has to appear
    in the acronyms being created.
    """

    def __init__(self, words: List[str], matches: Dict[str, Set[str]],
                 optional: bool = False) -> None:
        """
        Creates a new Token.

        :param words: The words of the disjunction represented by the Token.
        :param matches: The dictionary associating each letter appearing in the
                        Token to the word(s) in which it appears.
        :param optional: Whether the Token is optional.
        """
        self._words = words
        self._matches = matches
        self._optional = optional

    def __contains__(self, letter: str) -> bool:
        """
        Checks whether a letter can be used to represent this Token.

        :param letter: The letter to check.

        :return: Whether the letter appears in this Token.
        """
        return letter in self._matches

    def __iter__(self) -> Iterator[str]:
        """
        Gives an iterator over the letters appearing in this Token.

        :return: An iterator over the letters of this Token.
        """
        return iter(self._matches)

    def words_with(self, letter: str) -> Set[str]:
        """
        Gives the set of words from this Token that contain the given letter.

        :param letter: The letter to find words for.

        :return: The words in which the given letter appears.

        :raises ValueError: If the letter does not appear in this Token.
        """
        if letter in self:
            return self._matches[letter]
        raise ValueError(f'"{letter}" does not appear in {self}')

    def is_optional(self) -> bool:
        """
        Checks whether this Token is optional.

        :return: If this Token is optional.
        """
        return self._optional

    def __str__(self) -> str:
        """
        Gives a string representing the disjunction of the words contained in
        this Token.

        :return: A string representing this Token.
        """
        string = ' or '.join(self._words)
        if self.is_optional():
            return f'({string})?'
        return f'({string})'


class TokenBuilder:
    """
    A TokenBuilder makes easier the creation of a new instance of Token.
    """

    def __init__(self, selection_strategy: Callable[[str], Set[str]]) -> None:
        """
        Creates a new TokenBuilder.

        :param selection_strategy: The letter selection strategy to use to
                                   select letters from the words of the built
                                   Token.
        """
        self._selection_strategy = selection_strategy
        self._words = []
        self._matches = defaultdict(set)
        self._optional = False

    def add_word(self, word: str) -> None:
        """
        Adds a word to the built Token.

        :param word: The word to add.
        """
        normalized_word = str(normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8'))
        normalized_word = normalized_word.lower()
        self._words.append(normalized_word)
        for letter in self._selection_strategy(normalized_word):
            self._matches[letter].add(normalized_word)

    def set_optional(self, optional: bool = True) -> None:
        """
        Sets the optionality of the built Token.

        :param optional: Whether the built Token is optional.
        """
        self._optional = optional

    def build(self) -> Token:
        """
        Creates the built Token.

        :return: The created Token.
        """
        return Token(self._words, self._matches, self._optional)


class MatchingToken:
    """
    A MatchingToken represents a Token for which a matching letter exists in an
    acronym.
    """

    def __init__(self, token: Token, letter: str) -> None:
        """
        Creates a new MatchingToken.

        :param token: The Token for which a matching letter exists.
        :param letter: The matching letter, which has to appear in the Token.

        :raises ValueError: If the letter does not appear in the Token.
        """
        if letter not in token:
            raise ValueError(f'"{letter}" does not appear in {token}')
        self._token = token
        self._letter = letter

    def get_explanations(self) -> List[str]:
        """
        Gives the explanations of the matching words appearing in the Token.
        An explanation for a word is the string representation of this word,
        in which all letters are lower-case characters, except the matching
        letter which is upper-case.

        :return: The list of explanations.
        """
        matching_words = self._token.words_with(self._letter)
        return [self._get_one_explanation(word) for word in matching_words]

    def _get_one_explanation(self, word: str) -> str:
        """
        Gives the explanation of the given word.

        :param word: The word to get the explanation of.

        :return: The explanation of the word.
        """
        index = word.find(self._letter)
        length = len(self._letter)
        return word[:index] + self._letter.upper() + word[index + length:]
