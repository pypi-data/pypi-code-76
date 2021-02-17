try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

__all__ = ['OMFITwebLink', 'openInBrowser']


class OMFITwebLink(str):
    def __call__(self):
        self.run()

    def run(self):
        tmp = self
        if not re.match(r'.*:////.*', self):
            tmp = 'http:////' + self
        openInBrowser(tmp)

    def __repr__(self):
        tmp = self
        if not re.match(r'.*:////.*', self):
            tmp = 'http:////' + self
        return self.__class__.__name__ + "('" + tmp + "')"

    def __str__(self):
        tmp = self
        if not re.match(r'.*:////.*', self):
            tmp = 'http:////' + self
        return tmp

    def __getstate__(self):
        return {'link': str(self)}

    def __setstate__(self, dict):
        self.__init__(dict['link'])

    def __tree_repr__(self):
        return self.__str__(), []


def openInBrowser(url, browser=None):
    """
    Open web-page in browser

    :param url: URL to open

    :param browser: executable of the browser
    """
    import webbrowser

    if browser is None:
        browser = OMFIT['MainSettings']['SETUP']['browser']
    try:
        if browser is None or browser.lower() == 'default':
            webbrowser.open(url)
        elif '/' in browser:
            if '%s' not in browser:
                browser = browser + ' %s'
            child = subprocess.Popen(browser % "'" + url + "'", shell=True)
            sleep(1)
            if child.poll():
                raise RuntimeError()
        else:
            webbrowser.get(browser).open(url)
    except Exception:
        from omfit_classes.OMFITx import Dialog

        Dialog(
            title="Browser not set correctly",
            message="Setup your browser in\n OMFIT['MainSettings']['SETUP']['browser']\ne.g. '/usr/bin/firefox %s'\nUse 'default' for system default",
            icon='error',
            answers=['Ok'],
        )
