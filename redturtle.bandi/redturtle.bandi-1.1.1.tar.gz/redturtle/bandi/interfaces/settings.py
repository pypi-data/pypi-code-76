# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from redturtle.bandi import bandiMessageFactory as _


class IBandoSettings(Interface):
    """
    Settings used for announcements default value
    """

    default_ente = schema.Tuple(
        title=_(u"default_ente"),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(u'Regione Emilia-Romagna',),
    )

    default_destinatari = schema.Tuple(
        title=_(u"default_destinatari_bandi"),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(
            u'Cittadini|Cittadini',
            u'Imprese|Imprese',
            u'Enti locali|Enti locali',
            u'Associazioni|Associazioni',
            u'Altro|Altro',
        ),
    )

    tipologie_bando = schema.Tuple(
        title=_(u"Announcement types"),
        description=_(
            u"These values will extend bandi.xml vocabulary on filesystem"
        ),
        required=False,
        value_type=schema.TextLine(),
        missing_value=None,
        default=(
            u'beni_servizi|Acquisizione beni e servizi',
            u'agevolazioni|Agevolazioni, finanziamenti, contributi',
            u'altro|Altro',
        ),
    )
