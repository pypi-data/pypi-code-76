# -*- coding: utf-8 -*-
"""fds implementation of base components

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from logilab.common.registry import yes

from cubicweb.web.views.basecomponents import HeaderComponent
from cubicweb.web.views.basetemplates import TheMainTemplate

from cubicweb.web import component

from cubicweb_fds import monkeypatch_default_value

monkeypatch_default_value(component.CtxComponent.render_items, 'klass', u'list-unstyled')


class HideAsidesBar(HeaderComponent):
    """ Hide the left bar """
    __regid__ = 'hide-left-bar'
    __select__ = yes()
    context = 'header-right'
    order = 3
    visible = False
    icon_css_cls = 'glyphicon glyphicon-align-justify'

    def render(self, w):
        define_var = self._cw.html_headers.define_var
        define_var('twbs_col_cls', TheMainTemplate.twbs_col_cls)
        define_var('twbs_col_size', TheMainTemplate.twbs_col_size)
        define_var('twbs_grid_columns', TheMainTemplate.twbs_grid_columns)
        w(u'''<button class="btn btn-default navbar-btn" id="cw-aside-toggle"
              onclick="cw.cubes.squareui.toggleLeftColumn()" title="%(label)s">
              <span class="%(icon_class)s"></span>
              </button>''' % {'icon_class': self.icon_css_cls,
                              'label': self._cw._('collapse boxes')})
