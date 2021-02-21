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
This module provides the data structures used to combine the different
acronym building strategies so as to find acronyms matching a given set of
tokens.
"""


from typing import Any, Callable, Iterable, List, Set, Tuple
from unicodedata import normalize

from acronymmaker.matching import Acronym, MatchingStrategy
from acronymmaker.token import Token, TokenBuilder


class AcronymMaker:
    """
    AcronymMaker is responsible for dispatching the computation of acronyms to
    the appropriate strategies.
    """

    def __init__(self, selection_strategy: Callable[[str], Set[str]],
                 matching_strategy: MatchingStrategy,
                 callback: Callable[[Acronym], Any]) -> None:
        """
        Creates a new AcronymMaker.

        :param selection_strategy: The letter selection strategy to use to
                                   select letters from the words to create
                                   acronyms from.
        :param matching_strategy: The matching strategy to use to check
                                  whether a word matches as an acronym.
        :param callback: The callback function to invoke when an acronym is
                         found.
        """
        self._selection_strategy = selection_strategy
        self._matching_strategy = matching_strategy
        self._callback = callback
        self._known_words = []

    def add_known_word(self, word: str) -> None:
        """
        Adds the given word to the dictionary of words that are known by this
        AcronymMaker.

        :param word: The word to add.
        """
        normalized_word = word.strip()
        normalized_word = str(normalize('NFD', normalized_word).encode('ascii', 'ignore').decode('utf-8'))
        normalized_word = normalized_word.lower()
        self._known_words.append(normalized_word)

    def add_known_words(self, words: Iterable[str]) -> None:
        """
        Adds the given words to the dictionary of words that are known by this
        AcronymMaker.

        :param words: The words to add.
        """
        for word in words:
            self.add_known_word(word)

    def find_acronyms_for_string(self, tokens: str) -> None:
        """
        Searches the known words to find acronyms for the given tokens.

        Tokens must be represented with a string having the following
        format (question marks are used to mark optional tokens):

            'word_1_1/.../word_1_n1[?]  ...  word_m_1/.../word_m_nm[?]'

        :param tokens: The tokens to find acronyms for, as a string in
                       the format described above.
        """
        extracted_tokens = []
        for token in tokens.split():
            optional = False
            if token.endswith('?'):
                token = token[:-1]
                optional = True
            extracted_tokens.append((token.split('/'), optional))
        self.find_acronyms_for_list(extracted_tokens)

    def find_acronyms_for_list(self, tokens: List[Tuple[List[str], bool]]) -> None:
        """
        Searches the known words to find acronyms for the given tokens.

        Tokens must be represented with a list of tuples.
        Each tuple contains the list of the words of the corresponding token
        and a Boolean value representing the optionality of this token.

        :param tokens: The tokens to find acronyms for, as a list in the
                       format described above.
        """
        extracted_tokens = []
        for token, optional in tokens:
            builder = TokenBuilder(self._selection_strategy)
            for word in token:
                builder.add_word(word)
            builder.set_optional(optional)
            extracted_tokens.append(builder.build())
        return self.find_acronyms(extracted_tokens)

    def find_acronyms(self, tokens: List[Token]) -> None:
        """
        Searches the known words to find acronyms for the given Tokens.

        :param tokens: The Tokens to find acronyms for.
        """
        self._matching_strategy.set_tokens(tokens)
        for word in self._known_words:
            acronym = self._matching_strategy.as_acronym(word)
            if acronym is not None:
                self._callback(acronym)
