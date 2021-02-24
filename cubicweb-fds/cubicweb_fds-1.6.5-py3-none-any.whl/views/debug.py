"""fds implementation of base debug views

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__docformat__ = "restructuredtext en"

from time import strftime, localtime

from six import text_type

from logilab.common.decorators import monkeypatch

from logilab.mtconverter import xml_escape

from cubicweb import BadConnectionId
from cubicweb.web.views import debug


def dict_to_html(w, dict):
    # XHTML doesn't allow emtpy <ul> nodes
    if dict:
        w(u'<dl>')
        for key in sorted(dict):
            w(u'<dt>%s</dt><dd>%s</dd>' % (
                xml_escape(str(key)), xml_escape(repr(dict[key]))))
        w(u'</dl>')


@monkeypatch(debug.ProcessInformationView)
def call(self, **kwargs):
    req = self._cw
    dtformat = req.property_value('ui.datetime-format')
    _ = req._
    w = self.w
    repo = req.cnx.repo
    # generic instance information
    w(u'<h2>%s</h2>' % _('Instance'))
    w(u'<table class="table table-striped table-condensed">')
    for key, value in ((_('config type'), self._cw.vreg.config.name),
                       (_('config mode'), self._cw.vreg.config.mode),
                       (_('instance home'), self._cw.vreg.config.apphome)):
        w(u'<tr><th>%s</th><td>%s</td></tr>' % (key, value))
    w(u'</table>')
    vcconf = repo.get_versions()
    w(u'<h3>%s</h3>' % _('versions configuration'))
    w(u'<table class="table table-striped table-condensed">')
    w(u'<tr><th>%s</th><td>%s</td></tr>' % (
        'CubicWeb', vcconf.get('cubicweb', _('no version information'))))
    for cube in sorted(self._cw.vreg.config.cubes()):
        cubeversion = vcconf.get(cube, _('no version information'))
        w(u'<tr><th>%s</th><td>%s</td></tr>' % (
            cube, cubeversion))
    w(u'</table>')
    # repository information
    w(u'<h2>%s</h2>' % _('Repository'))
    w(u'<h3>%s</h3>' % _('resources usage'))
    w(u'<table class="table table-striped table-condensed">')
    stats = self._cw.call_service('repo_stats')
    for element in sorted(stats):
        w(u'<tr><th>%s</th><td>%s %s</td></tr>'
          % (element, xml_escape(text_type(stats[element])),
             element.endswith('percent') and '%' or ''))
    w(u'</table>')
    # web server information
    w(u'<h2>%s</h2>' % _('Web server'))
    w(u'<table class="table table-striped table-condensed">')
    w(u'<tr><th>%s</th><td>%s</td></tr>' % (
        _('base url'), req.base_url()))
    w(u'<tr><th>%s</th><td>%s</td></tr>' % (
        _('data directory url'), req.datadir_url))
    w(u'</table>')
    from cubicweb.web.application import SESSION_MANAGER
    if SESSION_MANAGER is not None and req.user.is_in_group('managers'):
        sessions = SESSION_MANAGER.current_sessions()
        w(u'<h3>%s</h3>' % _('opened web sessions'))
        if sessions:
            w(u'<ul>')
            for session in sessions:
                if hasattr(session, 'cnx'):
                    # cubicweb < 3.19
                    if not session.cnx:
                        w(u'<li>%s (NO CNX)</li>' % session.sessionid)
                        continue
                    try:
                        last_usage_time = session.cnx.check()
                    except BadConnectionId:
                        w(u'<li>%s (INVALID)</li>' % session.sessionid)
                        continue
                else:
                    # cubicweb >= 3.19
                    last_usage_time = session.mtime
                w(u'<li>%s (%s: %s)<br/>' % (
                    session.sessionid,
                    _('last usage'),
                    strftime(dtformat, localtime(last_usage_time))))
                dict_to_html(w, session.data)
                w(u'</li>')
            w(u'</ul>')
        else:
            w(u'<p>%s</p>' % _('no web sessions found'))


@monkeypatch(debug.RegistryView)  # noqa: F811
def call(self, **kwargs):
    self.w(u'<h2>%s</h2>' % self._cw._("Registry's content"))
    keys = sorted(self._cw.vreg)
    url = xml_escape(self._cw.url())
    self.w(u'<p>%s</p>\n' % ' - '.join('<a href="%s#%s">%s</a>'
                                       % (url, key, key) for key in keys))
    for key in keys:
        if key in ('boxes', 'contentnavigation'):  # those are bw compat registries
            continue
        self.w(u'<h3 id="%s">%s</h3>' % (key, key))
        if self._cw.vreg[key]:
            values = sorted(self._cw.vreg[key].items())
            self.wview('pyvaltable', pyvalue=[(key, xml_escape(repr(val)))
                                              for key, val in values])
        else:
            self.w(u'<p>Empty</p>\n')
