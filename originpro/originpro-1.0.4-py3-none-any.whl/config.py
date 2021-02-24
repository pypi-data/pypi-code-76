"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0103,W0611
oext=False
try:
    import PyOrigin as po
except ImportError:
    import OriginExt
    class APP:
        'OriginExt.Application() wrapper'
        def __init__(self):
            self._app = None
        def __getattr__(self, name):
            if self._app is None:
                self._app = OriginExt.Application()
            return getattr(self._app, name)
        def Exit(self):
            'Exit if Application exists'
            if self._app is not None:
                self._app.Exit()
                self._app = None
    po = APP()
    oext = True
