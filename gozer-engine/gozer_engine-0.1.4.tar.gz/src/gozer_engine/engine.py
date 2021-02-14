from __future__ import annotations
import time
import sys
from abc import ABC

from gozer_engine.base import BaseMediator

class BrowserEngine(BaseMediator):
    '''Central mediator object of the browser. Handles communication
       between all browser components
    '''
    def __init__(self, network_client: NetworkClient, render_engine: RenderEngine,
                parser: GopherSourceParser, history: BrowserHistory) -> None:
        self._network_client = network_client
        self._network_client.mediator = self
        self._render_engine = render_engine
        self._render_engine.mediator = self
        self._parser = parser
        self._parser.mediator = self
        self._history = history
        self._history.mediator = self


        # TODO: Better naming, re-evaluate location
        self._tree = None
        self._request_type = None
        self._page_str = ''

    def start(self, uri: str = None):
        '''Initialize the mediator object. If Gozer was started with a
           URI arg from the command line, initialize the interface and
           send a network request for the specified URI.

        :param uri: Gopher URI passed from the command line
        :type uri: str
        '''
        if uri:
            self.notify(self, {
                'msg': 'browser_initialized'
            })
            # TODO: Cheating a bit here. Find a way
            # to not have to rely on manually waiting
            # for the window/canvas/addr_bar to init
            time.sleep(1)
            self._direct_request(uri)
        else:
            self.notify(self, {
                'msg': 'browser_initialized'
            })


    def _direct_request(self, uri: str):
        '''Send URI to network module to make Gopher request

        :param uri: Gopher address
        :type uri: str
        '''
        self._network_client.send_request(uri)

    def notify(self, sender: object, event: dict) -> None:
        '''Receive events from other components and take
        action based on message/data

        :param sender: Component object sending the event
        :type object:
        :param event: Payload from Component object containing message and data
        :type event: dict
        '''

        # Network request events
        if event['msg'] == 'request_received':
            self._request_type = event['data']['request_type']
            self._network_client.send_request(event['data']['uri'])
        if event['msg'] == 'response_received':
            if self._request_type == 0:
                # Plain text file. Do not run through
                # the Gopher parser/renderer
                self._page_str = event["data"]['resp_str']

                # self._request_type = None

                self._history.truncate()
                self._history.push_page({
                    'dom': None,
                    'page_str': self._page_str
                })

            else:
                self._parser.parse_source(event['data']['resp_str'])

        # Output events
        if event['msg'] == 'source_parsed':
            self._tree = event['data']['page_tree']
            self._render_engine.render_source(self._tree)
        if event['msg'] == 'page_rendered':
            self._dom = event['data']['dom']
            self._page_str = event['data']['page_str']

            self._history.truncate()
            self._history.push_page({
                'dom': self._dom,
                'page_str': self._page_str
            })

        if event['msg'] in ['shift_back_one_page', 'shift_forward_one_page']:
            self._dom = event['data']['dom']
            self._page_str = event['data']['page_str']

