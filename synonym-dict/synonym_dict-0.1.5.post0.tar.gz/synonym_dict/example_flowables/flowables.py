"""
A JSON-serializable collection of Flowable objects
"""

from .flowable import Flowable
from ..synonym_dict import SynonymDict
from .cas_number import cas_regex, CasNumber


class FlowablesDict(SynonymDict):

    _entry_group = 'Flowables'
    _syn_type = Flowable
    _ignore_case = True

    def add_synonym(self, term, syn):
        """
        Add a new term as a synonym to an existing term
        Need to catch CAS numbers here and not just at instantiation
        :param term: the existing term
        :param syn: the new synonym
        :return:
        """
        syn = str(syn)
        if isinstance(term, self._syn_type):
            term = term.name
        ent = self._d[term]
        if bool(cas_regex.match(syn)):
            cas = CasNumber(syn)
            for c in cas.terms:
                self._add_term(c, ent)
            ent.add_child(cas)
        else:
            self._add_term(syn, ent)  # checks TermExists
            ent.add_term(syn)

    def matching_flowables(self, *args):
        """
        just exposes the match_set function
        :param args:
        :return:
        """
        for k in self._match_set(args):
            yield k.name
