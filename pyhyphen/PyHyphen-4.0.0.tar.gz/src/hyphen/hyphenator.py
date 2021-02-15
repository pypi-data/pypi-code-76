# -*- coding: utf-8 -*-

# Without prejudice to the license governing the use of
# the Python standard module textwrap on which textwrap2 is based,
# PyHyphen is licensed under the same terms as the underlying
# `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_.
# The essential parts of the license terms of libhyphen are quoted hereunder.
#
#
#
# Extract from the license information of hyphen-2.8 library
# ============================================================
#
#
#
# GPL 2.0/LGPL 2.1/MPL 1.1 tri-license
#
# Software distributed under these licenses is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the licences
# for the specific language governing rights and limitations under the licenses.
#
# The contents of this software may be used under the terms of
# the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL",

from . import dictools
from . import hnj


__all__ = ['Hyphenator']


class Hyphenator:
    """
    Wrapper class around the class 'hnj.hyphenator_' from the C extension.
    It provides convenient access to the C library libhyphen.
    """

    def __init__(self, language='en_US', lmin=2, rmin=2, compound_lmin=2,
                 compound_rmin=2, directory=None,
                 **request_args):
        '''
        Return a hyphenator object initialized with a dictionary for the specified language, typically a locale name.

            Example: 'en_NZ' for English / New Zealand

        If the corresponding dictionary was not installed, it will be
        downloaded automatically to `directory`, which defaults to the user
        data directory.

        lmin, rmin, compound_lmin and compound_rmin: set minimum number of chars to be cut off by hyphenation in
        single or compound words
        
        **request_args: any kwargs to be  passed on to `requests.get` 
            to configure the HTTP connection if 
            a dictionary needs to be downloaded.
        '''
        file_path = dictools.install(language, directory=directory, **request_args)
        try:
            self.__hyphenate__ = hnj.hyphenator_(file_path, 
                lmin, rmin, 
                compound_lmin, compound_rmin)
        except Exception as E:
                raise RuntimeError(f'C extension    raised  error \
                when initializing Hyphenator for dictionary at {file_path}') from E
        self.apply = self.__hyphenate__.apply
        self.language = language
        self.dict_path = file_path

    def __repr__(self):
        return f"""hyphen.hyphenator.Hyphenator object. 
            language: {self.language}, dictionary at {self.dict_path}"""  
        
    def pairs(self, word):
        '''
        Hyphenate a  string and return a list of lists of the form
        [['hy', 'phenation'], ['hyphen', 'ation']].

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding, or
        * the hyphenator could not find any hyphenation point
        '''
        if not isinstance(word, str):
            raise TypeError(f'str expected, {type(word)} given.')

        # Discard very short words
        if (len(word) < 4) or ('=' in word):
            return []
        # Set bit 0 of mode to 1 as we want a list of pairs.      
        # Set bit 1 if word is capitalized. 
        # In this case, the 
        # hyphenator will return    capitalized      word.
        if word.isupper():
            word = word.lower()
            mode = 3
        else: 
            mode = 1
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.'
        try:
            return self.apply(word, mode)
        except UnicodeError:
            return []


    def syllables(self, word):
        '''
        Hyphenate a unicode string and return list of syllables.

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding, or
        * the hyphenator could not find any hyphenation point

        Results are not consistent in case of non-standard hyphenation as a join of the syllables
        would not yield the original word.
        '''
        if not isinstance(word, str):
            raise TypeError(f'str expected, {type(word)} given.')
        # discard very short words
        if (len(word) < 4) or ('=' in word):
            return []
        if word.isupper():
            word = word.lower()
            mode = 2
        else: 
            mode = 0
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.'
        try:                
            return self.apply(word, mode).split('=')
        except UnicodeError:
            return []


    def wrap(self, word, width, hyphen='-'):
        '''
        Hyphenate 'word' and determine the best hyphenation fitting
        into 'width' characters.
        Return a list of the form [u'hypen-', u'ation']
        The '-' in the above example is the default value of 'hyphen'.
        It is added automatically and must fit
        into 'width' as well. If no hyphenation was found such that the
        shortest prefix (plus 'hyphen') fits into 'width', [] is returned.
        '''

        p = self.pairs(word)
        max_chars = width - len(hyphen)
        while p:
            if p[-1][0].endswith(hyphen):
                cur_max_chars = max_chars + 1
            else: cur_max_chars = max_chars
            if len(p[-1][0]) > cur_max_chars:
                p.pop()
            else:
                break
        if p:
            # Need to append a hyphen?
            if cur_max_chars == max_chars:
                p[-1][0] += hyphen
            return p[-1]
        else:
            return []
