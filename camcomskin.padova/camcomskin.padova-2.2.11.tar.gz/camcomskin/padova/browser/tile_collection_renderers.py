# -*- coding: utf-8 -*-
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five.browser import BrowserView
from rer.bandi import bandiMessageFactory
from ZODB.POSException import POSKeyError
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements

from camcomskin.padova import _

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory


class HelpersView(BrowserView):
    """
    A set of helper functions for tile collection views.
    """

    def get_image_tag(
        self, item, scale="thumb", direction="down", css_class=""
    ):
        try:
            scale_view = api.content.get_view(
                name="images", context=item, request=self.request
            )
            return scale_view.scale(
                "image", scale=scale, direction=direction
            ).tag(css_class=css_class)
        except (InvalidParameterError, POSKeyError, AttributeError, KeyError):
            # The object doesn't have an image field
            return ""

    def get_bg_url(self, item, scale="thumb"):
        try:
            scale_view = api.content.get_view(
                name="images", context=item, request=self.request
            )
            return (
                'background-image: url("'
                + str(scale_view.scale("image", scale=scale).url)
                + '");'
            )
        except (InvalidParameterError, POSKeyError, AttributeError):
            # The object doesn't have an image field
            return ""

    def get_formatted_date(self, item):
        """
        return a formatted date
        """
        effective = item.effective
        if effective.year() == 1969:
            # not yet published
            return {}
        return {
            "weekday": u"weekday_{0}".format(effective.aDay().lower()),
            "month": u"month_{0}".format(effective.aMonth().lower()),
            "month_abbr": u"month_{0}_abbr".format(effective.aMonth().lower()),
            "day": effective.day(),
            "year": effective.year(),
        }

    def get_event_dates(self, event):
        """
        returns a string with date info (range, hours,...)
        """

        months = {
            "1": "Gennaio",
            "2": "Febbraio",
            "3": "Marzo",
            "4": "Aprile",
            "5": "Maggio",
            "6": "Giugno",
            "7": "Luglio",
            "8": "Agosto",
            "9": "Settembre",
            "10": "Ottobre",
            "11": "Novembre",
            "12": "Dicembre",
        }

        date_string = ""
        start_date_parts = [
            event.startDate.day(),
            months[str(event.startDate.month())],
            event.startDate.year(),
        ]
        startDate = " ".join([str(x) for x in start_date_parts])

        if event.startDate.Date() == event.endDate.Date():
            date_string = (
                startDate
                + ", ore "
                + event.startDate.TimeMinutes()
                + " - "
                + event.endDate.TimeMinutes()
            )

        else:
            end_date_parts = [
                event.endDate.day(),
                months[str(event.endDate.month())],
                event.endDate.year(),
            ]
            endDate = " ".join([str(x) for x in end_date_parts])
            date_string = "dal " + startDate + " al " + endDate

        return date_string

    def getTipologiaTitle(self, key):
        """
        """
        try:
            voc_tipologia = getUtility(
                IVocabularyFactory, name='rer.bandi.tipologia.vocabulary'
            )(self.context)
            value = voc_tipologia.getTermByToken(key)
            return value.title
        except LookupError:
            return key

    def isTipologiaValid(self, tipologia_bando):
        """
        """
        try:
            voc_tipologia = getUtility(
                IVocabularyFactory, name='rer.bandi.tipologia.vocabulary'
            )(self.context)
            return tipologia_bando in [x.value for x in voc_tipologia._terms]
        except LookupError:
            return tipologia_bando

    def isValidDeadline(self, date):
        """
        """
        if not date:
            return False
        if date.Date() == '2100/12/31':
            # a default date for bandi that don't have a defined deadline
            return False
        return True

    def getScadenzaDate(self, brain):
        date = brain.getScadenza_bando
        long_format = True
        if brain.getScadenza_bando.Time() == '00:00:00':
            # indexer add 1 day to this date, to make a bando ends at midnight
            # of the day-after, if time is not provided
            date = date - 1
            long_format = False
        return api.portal.get_localized_time(
            datetime=date, long_format=long_format
        )

    def getBandoState(self, bando):
        """
        return corretc bando state
        """
        scadenza_bando = bando.getScadenza_bando
        chiusura_procedimento_bando = bando.getChiusura_procedimento_bando
        state = (
            'open',
            translate(bandiMessageFactory(u'Open'), context=self.request),
        )
        if scadenza_bando and scadenza_bando.isPast():
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    'closed',
                    translate(
                        bandiMessageFactory(u'Closed'), context=self.request
                    ),
                )
            else:
                state = (
                    'inProgress',
                    translate(
                        bandiMessageFactory(u'In progress'),
                        context=self.request,
                    ),
                )
        else:
            if (
                chiusura_procedimento_bando
                and chiusura_procedimento_bando.isPast()
            ):
                state = (
                    'closed',
                    translate(_(u'Closed'), context=self.request),
                )
        return state


class SightsView(BrowserView):
    """
    Custom view that shows sights
    """

    implements(ICollectionTileRenderer)

    display_name = _("Sights layout")


class NewsHighlightView(BrowserView):
    """
    Custom view that shows an highlighted news
    """

    implements(ICollectionTileRenderer)

    display_name = _("News highlight")


class NewsTwoRowsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout news su due righe")


class PairedCollectionView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout tile affiancate")


class BandiCollectionView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout bandi")


class NewsBigPhotoView(BrowserView):
    """
    Custom view that shows a news with a big photo on the background
    """

    implements(ICollectionTileRenderer)

    display_name = _("News with big photo")


class NewsAreaTematicaView(BrowserView):
    """
    Custom view that shows news in area tematica
    """

    implements(ICollectionTileRenderer)

    display_name = _("News in area tematica")


class ServiziAreaTematicaView(BrowserView):
    """
    Custom view that shows servizi in area tematica
    """

    implements(ICollectionTileRenderer)

    display_name = _("Servizi in area tematica")


class NewsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("News layout with image")


class VideoView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Video layout")


class EventsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Events layout")


class GalleryView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Gallery layout")


class AreeTematicheView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Link aree tematiche")


class LandingAreeTematicheView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Landing page aree tematiche")


class OnlineServicesView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout servizi online")


class CCIAACollectionTileView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout collezione CCIAA")
