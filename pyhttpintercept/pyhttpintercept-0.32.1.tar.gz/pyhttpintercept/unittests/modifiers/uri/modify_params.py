# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_uri_modifier
from pyhttpintercept.intercept.modifiers.uri import modify_params as module_to_test
from simpil import SimpilImage

logging = logging_helper.setup_logging()

params = {"remove": {"paramtoremove": "whatever"},
          "modify": [{"p2": "p2v"},
                     {"p1": {"old": "xxx",
                             "new": "p1v2"}
                      }],
          "add": [{"p3": "v3"}]
          }

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=(u'http://user:pass@www.hostname.com:8080'
                                   u'/some_method'
                                   u'?p1=p1v1'
                                   u'&p1=xxx'
                                   u'&p2=x'
                                   u'&paramtoremove=whatever'
                                   u'&paramtoremove=bovvered'
                                   u'#hash'),
                              filter=u'some_method',
                              params=params)

print(uri)
assert '/some_method?' in uri
assert 'p1=p1v1' in uri
assert 'p1=p1v2' in uri
assert 'p2=p2v' in uri
assert 'p3=v3' in uri
assert 'paramtoremove=whatever' not in uri
assert 'paramtoremove=bovvered' in uri
assert '&' in uri
assert uri.startswith('http://user:pass@www.hostname.com:8080')
assert uri.endswith('#hash')

# ---------------------

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=(u'http://www.hostname.com'
                                   u'/some_method'
                                   u'?p1=p1v1'
                                   u'&p1=xxx'
                                   u'&p2=x'
                                   u'&paramtoremove=whatever'
                                   u'&paramtoremove=bovvered'
                                   u'#hash'),
                              filter=u'some_method',
                              params=params)

print(uri)
assert '/some_method?' in uri
assert 'p1=p1v1' in uri
assert 'p1=p1v2' in uri
assert 'p2=p2v' in uri
assert 'p3=v3' in uri
assert 'paramtoremove=whatever' not in uri
assert 'paramtoremove=bovvered' in uri
assert '&' in uri
assert uri.startswith('http://www.hostname.com')
assert uri.endswith('#hash')

# ---------------------

params = {"remove": [{"paramtoremove": ""},
                     {"p1": ""},
                     {"p2": ""}]}

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=(u'http://www.hostname.com'
                                   u'/some_method'
                                   u'?p1=p1v1'
                                   u'&p1=xxx'
                                   u'&p2=x'
                                   u'&paramtoremove=whatever'
                                   u'&paramtoremove=bovvered'
                                   u'#hash'),
                              filter=u'some_method',
                              params=params)


print(uri)
assert '/some_method?' not in uri
assert '/some_method' in uri
assert 'p1=' not in uri
assert 'p2=' not in uri
assert 'p3=v3' not in uri
assert 'paramtoremove' not in uri
assert '&' not in uri
assert uri.startswith('http://www.hostname.com/')
assert uri.endswith('#hash')

