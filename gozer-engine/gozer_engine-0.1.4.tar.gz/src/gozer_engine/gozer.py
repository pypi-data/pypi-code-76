from __future__ import annotations

from gozer_engine.engine import BrowserEngine
from gozer_engine.network import NetworkClient
from gozer_engine.render import RenderEngine
from gozer_engine.parser import GopherSourceParser
from gozer_engine.history import BrowserHistory

class Gozer():
    '''The main interface for the browser engine'''
    def __init__(self):
        network_client = NetworkClient()
        parser = GopherSourceParser()
        render_engine = RenderEngine()
        history = BrowserHistory()

        self._browser_engine = BrowserEngine(
            network_client,
            render_engine,
            parser,
            history
        )

    # General
    def start(self, uri: str = None):
        '''Initialize an instance of the Gozer engine
        
        :param uri: Gopher URI passed from the command line
        :type uri: str
        '''
        self._browser_engine.start(uri)

    # Page Contents
    def get_page_contents(self):
        '''Get the current contents of the browser page

        :return: Page contents
        :rtype: str
        '''
        return self._browser_engine._page_str

    def get_page_dom(self):
        '''Get the Document Object Model representation
        of the page
        
        :return: Page DOM
        :rtype: list
        '''
        return self._browser_engine._dom

    # Network
    def send_request(self, uri: str, init: bool = False, request_type: int = 1):
        '''Send URI as network request to Gopher server

        :param uri: Gopher URI
        :type uri: str
        '''
        if init:
            self._browser_engine._direct_request(uri)
        else:
            self._browser_engine.notify(self, {
                'msg': 'request_received',
                'data': {
                    'uri': uri,
                    'request_type': request_type
                }
            })

    # History

    # TODO: Will need a LoD refactor
    def back_one_page(self):
        '''Shift back one page in browser history'''
        if self._browser_engine._history._cursor == 0:
            # Send notification that browser
            # is at beginning of history
            pass
        else:
            self._browser_engine._history._cursor -= 1
            new_current_page = self._browser_engine._history.get_current_page()

            self._browser_engine._history.mediator.notify(self, {
                'msg': 'shift_back_one_page',
                'data': {
                    'dom': new_current_page['dom'],
                    'page_str': new_current_page['page_str']
                }
            })

    #  TODO: Will need a LoD refactor
    def forward_one_page(self):
        '''Shift forward one page in browser history'''
        if self._browser_engine._history._cursor == len(self._browser_engine._history._history) -1:
            # Send notification that browser
            # is at beginning of history
            pass
        else:
            self._browser_engine._history._cursor += 1
            new_current_page = self._browser_engine._history.get_current_page()

            self._browser_engine._history.mediator.notify(self, {
                'msg': 'shift_forward_one_page',
                'data': {
                    'dom': new_current_page['dom'],
                    'page_str': new_current_page['page_str']
                }
            })