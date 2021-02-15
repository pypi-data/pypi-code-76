# -*- coding: utf-8 -*-

from imio.restapi.vocabularies import base
from imio.restapi.form.link import get_links
from plone.memoize import view


class PSTActionVocabularyFactory(base.RestSearchVocabularyFactory):
    """ Vocabulary that return all the pst actions from the app """
    application_id = "PST"

    @property
    def parameters(self):
        return "portal_type=pstaction&b_size=999"

    def _existing_link(self, obj):
        """ Return the link paths for the given content """
        link = get_links(obj)
        result = []
        if not link:  # This can happen with content created manually
            return result
        for link in get_links(obj):
            if link.back_link is True:
                result.append(link.path)
        return result

    @property
    @view.memoize
    def _children(self):
        return [self.context[k] for k in self.context.keys()]

    @property
    @view.memoize
    def _existing_links(self):
        context_links = []
        for child in self._children:
            context_links.extend(self._existing_link(child))
        return context_links

    def _filter(self, value):
        return value not in self._existing_links


PSTActionVocabulary = PSTActionVocabularyFactory()


class PSTActionProgressVocabularyFactory(base.RestSearchVocabularyFactory):
    """Vocabulary that return all the pst actions progress from a given context"""
    application_id = "PST"

    @property
    def parameters(self):
        link = get_links(self.context)
        if not link:
            # This should not happen
            link = self.context.UID()
        return (
            "base_search_uid={0}"
            "&portal_type=pstsubaction"
            "&b_size=999"
            "&metadata_fields=modified"
        ).format(link[0].uid)

    def _existing_link(self, obj):
        """ Return the link paths for the given content """
        link = get_links(obj)
        result = []
        if not link:  # This can happen with content created manually
            return result
        for link in get_links(obj):
            if link.back_link is True:
                result.append(link.path)
        return result

    @property
    @view.memoize
    def _children(self):
        return [self.context[k] for k in self.context.keys()]

    @property
    @view.memoize
    def _existing_links(self):
        context_links = []
        for child in self._children:
            context_links.extend(self._existing_link(child))
        return context_links

    def _filter(self, value):
        return value not in self._existing_links


PSTActionProgressVocabulary = PSTActionProgressVocabularyFactory()
