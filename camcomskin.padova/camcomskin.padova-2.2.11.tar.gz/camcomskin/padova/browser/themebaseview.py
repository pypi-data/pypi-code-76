from Products.Five import BrowserView
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize import view
from zope.component import getMultiAdapter
from zope.interface import implements

from camcomskin.padova.browser.interfaces import IThemeBaseView

_marker = []


class ThemeBaseView(BrowserView):
    implements(IThemeBaseView)

    # Utility methods

    def getColumnsClasses(self, view=None):
        """Determine whether a column should be shown. The left column is
        called plone.leftcolumn; the right column is called plone.rightcolumn.
        """

        plone_view = getMultiAdapter(
            (self.context, self.request), name=u'plone')
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        #  sl = plone_view.have_portlets('plone.leftcolumn', view=view)
        sl = False # hidden by italia design guidelines
        sr = plone_view.have_portlets('plone.rightcolumn', view=view)

        isRTL = portal_state.is_rtl()

        # pre-fill dictionary
        columns = dict(one="", content="", two="")

        if not sl and not sr:
            # we don't have columns, thus conten takes the whole width
            columns['content'] = "with-no-columns"

        elif sl and sr:
            # In case we have both columns, content takes 50% of the whole
            # width and the rest 50% is spread between the columns
            columns['one'] = "two-columns"
            columns['content'] = "with-column-one with-column-two"
            columns['two'] = "two-columns"

        elif (sr and not sl) and isRTL:
            # We have right column and we are in RTL language
            columns['content'] = "with-column-two rtl"
            columns['two'] = "column-two rtl"

        elif (sr and not sl) and not isRTL:
            # We have right column and we are NOT in RTL language
            columns['content'] = "with-column-two ltr"
            columns['two'] = "column-two ltr"

        elif (sl and not sr) and isRTL:
            # We have left column and we are in RTL language
            columns['one'] = "column-one rtl"
            columns['content'] = "with-column-one rtl"

        elif (sl and not sr) and not isRTL:
            # We have left column and we are in NOT RTL language
            columns['one'] = "column-one ltr"
            columns['content'] = "with-column-one ltr"

        return columns

    @view.memoize
    def is_homepage(self):
        """Determine whether the current context is the home page
           of the website.
        """
        pcs = getMultiAdapter((self.context, self.request),
                              name=u'plone_context_state')
        canonical = pcs.canonical_object()
        return INavigationRoot.providedBy(canonical)
