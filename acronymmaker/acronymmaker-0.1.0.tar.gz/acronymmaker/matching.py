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
This module provides strategies allowing to identify whether a given word
matches a sequence of tokens as an acronym.
"""


from re import compile
from typing import Dict, List, Optional, Pattern, Set, Tuple

from hopcroftkarp import HopcroftKarp

from acronymmaker.token import MatchingToken, Token


class Acronym:
    """
    An Acronym represents a sequence of MatchingTokens combined so as to
    explain a given word (the actual acronym).
    """

    def __init__(self, word: str, matching_tokens: List[MatchingToken]) -> None:
        """
        Creates a new Acronym.

        :param word: The word that is explained, i.e., the actual acronym.
        :param matching_tokens: The sequence of MatchingTokens explaining
                                the word.
        """
        self._word = word
        self._matching_tokens = matching_tokens

    def get_word(self) -> str:
        """
        Gives the word that this Acronym explains.
        It is camel-cased so as to highlight the letters that are matched by
        the associated MatchingTokens.

        :return: The word that is explained.
        """
        return self._word

    def get_explanations(self) -> List[str]:
        """
        Gives the explanations of this Acronym, i.e., the list of all possible
        combinations of words that explain it.
        The words in these explanations are camel-cased so as to highlight the
        letters that appear in the explained word.

        :return: The explanations of this Acronym.
        """
        return self._combine_tokens()

    def _combine_tokens(self, index: int = 0) -> List[str]:
        """
        Combines the associated MatchingTokens so as to create all the possible
        explanations for this Acronym.

        :param index: The index at which to start exploring MatchingTokens.

        :return: The computed explanations.
        """
        if index == len(self._matching_tokens) - 1:
            # Computing the explanations of the last Token.
            return self._matching_tokens[index].get_explanations()

        # Computing the explanations of the rest of the tokens.
        sub_explanations = self._combine_tokens(index + 1)

        # Combining them with the explanations of the current Token.
        explanations = []
        for explanation in self._matching_tokens[index].get_explanations():
            for sub_explanation in sub_explanations:
                explanations.append(f'{explanation} {sub_explanation}')
        return explanations

    def __str__(self) -> str:
        """
        Gives a string representation of this Acronym.
        It is a multi-line string, in which each line is composed of the
        actual acronym, followed by one possible explanation of this acronym.

        :return: The string representation of this Acronym.
        """
        explanations = []
        for explanation in self.get_explanations():
            explanations.append(f'{self._word}\t{explanation}')
        return '\n'.join(explanations)


class MatchingStrategy:
    """
    The MatchingStrategy is the parent class of the strategies that check
    whether a word can be explained as an Acronym by a sequence of Tokens.
    """

    def __init__(self, max_consecutive_unused: int, max_total_unused: int) -> None:
        """
        Creates a new MatchingStrategy.

        :param max_consecutive_unused: The maximum number of consecutive
                                       unused letters in the acronyms (i.e.,
                                       letters that do not match the Tokens).
        :param max_total_unused: The maximum number of overall unused letters
                                 in the acronyms (i.e., letters that do not
                                 match the Tokens).
        """
        self._max_consecutive_unused = max_consecutive_unused
        self._max_total_unused = max_total_unused
        self._tokens = None

    def set_tokens(self, tokens: List[Token]) -> None:
        """
        Sets the Tokens for which this MatchingStrategy must identify acronyms.

        :param tokens: The Tokens to set.
        """
        self._tokens = tokens

    def as_acronym(self, word: str) -> Optional[Acronym]:
        """
        Finds an Acronym that explains the given word based on the associated
        sequence of Tokens.

        :param word: The word to explain.

        :return: The Acronym explaining the given word, or None if the word
                 cannot be explained.

        :raises ValueError: If the sequence of Tokens has not been set.
        """
        if self._tokens is None:
            raise ValueError('There are no tokens to find acronyms for')

        acronym, matching_tokens = self.search_explanation(word.lower())
        if matching_tokens:
            return Acronym(acronym, matching_tokens)
        return None

    def search_explanation(self, word: str) -> Tuple[str, List[MatchingToken]]:
        """
        Tries to find a combination of the associated Tokens explaining the
        given word.

        :param word: The word to explain.

        :return: A tuple containing the camel-cased word highlighting the
                 matching letters, and the list of MatchingTokens explaining
                 the word.
                 If the latter list is empty, then the word cannot be explained
                 with the associated Tokens.
                 In this case, the content of the first string is undefined.
        """
        # Looking for a candidate explanation.
        explanation = [None] * len(word)
        if not self._internal_search_explanation(word, explanation):
            return word, []

        # Building the Acronym, unless the explanation is invalidated.
        acronym, matching_tokens = '', []
        consecutive_unused, total_unused = 0, 0

        # Trying to explain the letters of the word.
        for index, letter in enumerate(word):
            token = explanation[index]

            if token is None:
                # The letter is not explained.
                acronym += letter
                consecutive_unused += 1
                total_unused += 1

            else:
                # The letter is explained by the current Token.
                acronym += letter.upper()
                consecutive_unused = 0
                matching_tokens.append(MatchingToken(token, letter))

            if consecutive_unused > self._max_consecutive_unused or total_unused > self._max_total_unused:
                # Too many letters are not used: the explanation is invalidated.
                return word, []

        # The explanation is validated.
        return acronym, matching_tokens

    def _internal_search_explanation(self, word: str, explanation: List[Optional[Token]]) -> bool:
        """
        Tries to fill in an explanation for the given word based on the
        associated sequence of Tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.

        :return: Whether an explanation has been found.
                 If not, the content of explanation is undefined.
        """
        raise NotImplementedError('Method "_internal_search_explanation()" is abstract')


class GreedyOrderedMatchingStrategy(MatchingStrategy):
    """
    The GreedyOrderedMatchingStrategy checks whether a word can be explained
    as an Acronym while preserving the order of the sequence of Tokens, using
    a greedy algorithm.
    """

    def _internal_search_explanation(self, word: str, explanation: List[Optional[Token]]) -> bool:
        """
        Tries to fill in an explanation for the given word based on the
        associated sequence of Tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.

        :return: Whether an explanation has been found.
                 If not, the content of explanation is undefined.
        """
        # First, we try to use the mandatory Tokens.
        token_indices = {}
        if not self._explain_mandatory(word, explanation, token_indices):
            return False

        # Then, we use the optional Tokens, when possible.
        self._explain_optional(word, explanation, token_indices)
        return True

    def _explain_mandatory(self, word: str, explanation: List[Optional[Token]],
                           token_indices: Dict[int, int]) -> bool:
        """
        Tries to find an explanation for the given word based on the
        associated sequence of Tokens, considering only mandatory tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.
        :param token_indices: The dictionary storing, for each Token index, the index
                              of the letter it explains in the word.

        :return: Whether all mandatory tokens have been explained.
                 If not, the content of explanation is undefined.
        """
        # Looking for the first mandatory Token.
        token_index, token = self._next_mandatory(0)

        # Trying to explain each letter.
        for index, letter in enumerate(word):
            if not token:
                # There is no more mandatory Tokens.
                break

            # Trying to explain the current letter with the current Token.
            if letter in token:
                explanation[index] = token
                token_indices[token_index] = index
                token_index, token = self._next_mandatory(token_index + 1)

        # An explanation has been found if all mandatory tokens have been used.
        return token is None

    def _next_mandatory(self, index: int) -> Tuple[int, Optional[Token]]:
        """
        Looks for the next mandatory Token, starting from the given index.

        :param index: The index at which to start looking for.

        :return: A tuple containing the index of the next mandatory Token and
                 this Token, or -1 and None if there is no more such Tokens.
        """
        for i, token in enumerate(self._tokens[index:]):
            if not token.is_optional():
                return index + i, token
        return -1, None

    def _explain_optional(self, word: str, explanation: List[Optional[Token]],
                          token_indices: Dict[int, int]) -> None:
        """
        Tries to find an explanation for the given word based on the
        associated sequence of Tokens, considering only optional tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.
        :param token_indices: The dictionary storing, for each Token index, the index
                              of the letter it explains in the word.
        """
        for token_index, token in enumerate(self._tokens):
            # Only optional tokens are considered.
            if not token.is_optional():
                continue

            # Looking for a letter to explain.
            lower, upper = self._explainable_letters(word, token_index, token_indices)
            for letter_index in range(lower, upper):
                if word[letter_index] in token:
                    explanation[letter_index] = token
                    token_indices[token_index] = letter_index
                    break

    def _explainable_letters(self, word: str, current_index: int,
                             token_indices: Dict[int, int]) -> Tuple[int, int]:
        """
        Computes the lower and upper bounds for the indices of the letters that
        the (optional) Token at the given index can possibly explain.

        :param word: The word to explain
        :param current_index: The index of the current Token.
        :param token_indices: The dictionary storing, for each Token index, the index
                              of the letter it explains in the word.

        :return: The bounds for the possibly explainable letters.
        """
        # The first letter that can be explained is that following the latest already explained.
        lower_bound = 0
        for index in range(current_index - 1, -1, -1):
            latest_used = token_indices.get(index)
            if latest_used is not None:
                lower_bound = latest_used + 1
                break

        # The first non-explainable letter is that explained by the next mandatory Token.
        upper_bound = len(word)
        next_mandatory, _ = self._next_mandatory(current_index)
        if next_mandatory >= 0:
            upper_bound = token_indices[next_mandatory]

        return lower_bound, upper_bound


class RegexBasedOrderedMatchingStrategy(MatchingStrategy):
    """
    The RegexBasedOrderedMatchingStrategy checks whether a word can be
    explained as an Acronym while preserving the order of the sequence
    of Tokens, using regular expressions.
    """

    def __init__(self, max_consecutive_unused: int, max_total_unused: int) -> None:
        """
        Creates a new RegexBasedOrderedMatchingStrategy.

        :param max_consecutive_unused: The maximum number of consecutive
               unused letters in the acronym (i.e., letters that do not match
               the Tokens).
        :param max_total_unused: The maximum number of overall unused letters in the
               acronym (i.e., letters that do not match the Tokens).
        """
        super().__init__(max_consecutive_unused, max_total_unused)
        self._pattern = None

    def set_tokens(self, tokens: List[Token]) -> None:
        """
        Sets the tokens for which this RegexBasedOrderedMatchingStrategy must
        identify acronyms.

        :param tokens: The tokens to set.
        """
        super().set_tokens(tokens)
        self._pattern = self._create_pattern()

    def _create_pattern(self) -> Pattern:
        """
        Creates the pattern used to identify words matching as Acronyms.

        :return: The created pattern.
        """
        unused = '(.{0,' + str(self._max_consecutive_unused) + '}?)'
        regex = unused
        for token in self._tokens:
            token_regex = '(?:([' + ''.join(token) + '])' + unused + ')'
            if token.is_optional():
                token_regex = token_regex + '?'
            regex += token_regex
        return compile(f'^{regex}$')

    def _internal_search_explanation(self, word: str, explanation: List[Optional[Token]]) -> bool:
        """
        Tries to fill in an explanation for the given word based on the
        associated sequence of Tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.

        :return: Whether an explanation has been found.
                 If not, the content of explanation is undefined.
        """
        # Checking whether the word matches as an acronym.
        match = self._pattern.match(word)
        if not match:
            return False

        # Interpreting the groups of the regular expression as an explanation.
        self._explain_acronym(match.groups(), explanation)
        return True

    def _explain_acronym(self, groups: Tuple[str], explanation: List[Optional[Token]]) -> None:
        """
        Explains a word that matches as an acronym based on the groups extracted
        with the regular expression.

        :param groups: The groups identified by the regular expression.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.
        """
        token_index, char_index = 0, 0
        for index, group in enumerate(groups):
            # Explaining a Token when the group corresponds to this Token.
            if index % 2 != 0:
                if group:
                    explanation[char_index] = self._tokens[token_index]
                token_index += 1

            # Updating the current position in the word.
            if group:
                char_index += len(group)


class UnorderedMatchingStrategy(MatchingStrategy):
    """
    The UnorderedMatchingStrategy checks whether a word can be explained as an
    Acronym without considering the order of the sequence of Tokens, based on
    the Hopcroft-Karp matching algorithm.
    """

    def __init__(self, max_consecutive_unused: int, max_total_unused: int) -> None:
        """
        Creates a new UnorderedMatchingStrategy.

        :param max_consecutive_unused: The maximum number of consecutive
               unused letters in the acronym (i.e., letters that do not match
               the Tokens).
        :param max_total_unused: The maximum number of overall unused letters in the
               acronym (i.e., letters that do not match the Tokens).
        """
        super().__init__(max_consecutive_unused, max_total_unused)
        self._mandatory_tokens = None
        self._optional_tokens = None

    def set_tokens(self, tokens: List[Token]) -> None:
        """
        Sets the tokens for which this UnorderedMatchingStrategy must identify
        acronyms.

        :param tokens: The tokens to set.
        """
        super().set_tokens(tokens)
        self._mandatory_tokens = []
        self._optional_tokens = []

        for index, token in enumerate(tokens):
            if token.is_optional():
                self._optional_tokens.append(index)
            else:
                self._mandatory_tokens.append(index)

    def _internal_search_explanation(self, word: str, explanation: List[Optional[Token]]) -> bool:
        """
        Tries to fill in an explanation for the given word based on the
        associated sequence of Tokens.

        :param word: The word to explain.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.

        :return: Whether an explanation has been found.
                 If not, the content of explanation is undefined.
        """
        # First, looking for a matching of the mandatory tokens.
        letters = {str(index): set() for index in range(len(word))}
        matching = self._find_maximum_matching(word, self._mandatory_tokens, letters)

        # If there is no complete matching, the word cannot be explained as an acronym.
        if len(matching) != len(self._mandatory_tokens):
            return False

        # Removing the letters that are explained by the mapping.
        for letter_index in matching:
            del letters[letter_index]

        # Trying to use optional tokens to explain more letters.
        matching.update(self._find_maximum_matching(word, self._optional_tokens, letters))

        # Interpreting the matching as an explanation.
        self._explain_acronym(word, matching, explanation)
        return True

    def _find_maximum_matching(self, word: str, tokens: List[int], letters: Dict[str, Set[int]]) -> Dict[str, int]:
        """
        Finds a maximum matching between a set of Tokens and a set of letters
        from a word to explain.

        :param word: The word to explain.
        :param tokens: The list of the indices of the Tokens to consider in
                       the matching.
        :param letters: The indices of the letters to consider in the matching
                        (as strings).

        :return: The maximum matching between the specified Tokens and the
                 specified subset of the letters of the word.
        """
        # Creating the bipartite graph to compute the maximum matching of.
        for index, letter in enumerate(word):
            str_index = str(index)
            if str_index in letters:
                letters[str_index] = self._get_tokens_with(letter, tokens)

        # Actually computing the maximum matching.
        hopcroft_karp = HopcroftKarp(letters)
        return hopcroft_karp.maximum_matching(keys_only=True)

    def _get_tokens_with(self, letter: str, tokens: List[int]) -> Set[int]:
        """
        Searches for Tokens that can explain the given letter.

        :param letter: The letter to explain.
        :param tokens: The list of the indices of the Tokens that may explain
                       the letter.

        :return: The set of the indices of the Tokens that explain the letter.
        """
        token_indices = set()
        for token_index in tokens:
            if letter in self._tokens[token_index]:
                token_indices.add(token_index)
        return token_indices

    def _explain_acronym(self, word: str, matching: Dict[str, int],
                         explanation: List[Optional[Token]]) -> None:
        """
        Explains a word that matches as an acronym based on the computed maximum
        matching.

        :param word: The word to explain.
        :param matching: The maximum matching that matches a Token to the index
                         of the letter it explains in the word.
        :param explanation: The explanation to fill in.
                            This list has the same length as word, and is initially
                            filled with None.
                            After invoking this method, the i-th element of this
                            list will be a Token explaining the i-th letter of the
                            word, or None if this letter is not explained.
        """
        for index in range(len(word)):
            token_index = matching.get(str(index))
            if token_index is not None:
                explanation[index] = self._tokens[token_index]
