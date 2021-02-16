# -*- coding: utf-8 -*-
from plone import api
from plone.app.vocabularies.catalog import CatalogSource as CatalogSourceBase
from plone.autoform import directives
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.supermodel.model import Schema
from plone.tiles import PersistentTile
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


layouts = SimpleVocabulary(
    [
        SimpleTerm(value='', title=u'Espanso'),
        SimpleTerm(value='paired-collection tile-sx', title=u'Metà sinistra'),
        SimpleTerm(value='paired-collection tile-dx', title=u'Metà destra'),
    ]
)


class CatalogSource(CatalogSourceBase):
    """Navigation tile specific catalog source to allow targeted widget"""


class IPrenotazioniTile(Schema):
    """
    """

    prenotazione_folder = schema.Choice(
        title=u'Sportello prenotazione',
        description=u'Seleziona uno sportello prenotazione.',
        source=UUIDSourceBinder(portal_type=('PrenotazioniFolder')),
        required=True,
    )
    directives.widget(prenotazione_folder=ContentTreeFieldWidget)

    calendar_layout = schema.Choice(
        title=u'Layout calendario',
        description=u'Seleziona se mostrare il calendario a tutta larghezza o'
        u' a metà. I calendari a metà larghezza vanno accoppiati a due a due.',
        required=True,
        vocabulary=layouts,
    )

    css_class = schema.TextLine(
        title=u'Classe CSS',
        description=u'Inserisci una lista di classi CSS aggiuntive per'
        u' questa tile.',
        required=False,
    )


@implementer(IPrenotazioniTile)
class PrenotazioniTile(PersistentTile):
    def title(self):
        return self.data.get('title', u'')

    def get_folder(self):
        uid = self.data.get('prenotazione_folder', None)
        if not uid:
            return {}
        folder = api.content.get(UID=uid)
        if not folder:
            return {}
        return {'title': folder.Title(), 'url': folder.absolute_url()}

    def get_additional_css_classes(self, tile_class):
        if self.data.get('calendar_layout', ''):
            tile_class = '{0} {1}'.format(
                tile_class, self.data.get('calendar_layout', '')
            )
        if self.data.get('css_class', ''):
            tile_class = '{0} {1}'.format(
                tile_class, self.data.get('css_class', '')
            )
        return tile_class
