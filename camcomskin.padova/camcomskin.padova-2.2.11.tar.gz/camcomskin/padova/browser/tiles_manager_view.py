# -*- coding: utf-8 -*-
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.memoize import view
from redturtle.tiles.management.browser import tiles_view
from zope.interface import implementer
from pkg_resources import get_distribution


@implementer(IBlocksTransformEnabled)
class CCPDTilesView(tiles_view.BaseView):

    """
    La vista specifica usata per le tile delle Pagine (portal_type Document)
    """

    @property
    @view.memoize
    def pkg_version(self):
        return get_distribution("camcomskin.padova").version
