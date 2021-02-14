from gozer_engine.base import BaseComponent

class BrowserHistory(BaseComponent):
    '''Maintains the navigation history for
    the currentbrowsing session
    '''
    def __init__(self):
        self._history = []
        self._cursor = None

    def push_page(self, page: dict):
        '''Add page item to the browser history

        :param page: Payload containing the DOM and str representation of the page. Increment the history cursor.
        :type page: dict
        '''
        if not self._cursor:
            self._cursor = 0

        self._history.append(page)
        self._cursor =+ 1

    def pop_page(self):
        '''Remove page item from the browser history

        :param page: Payload containing the DOM and str representation of the page. Decrement the history cursor.
        :type page: dict
        '''
        if self._cursor == 0:
            # Send notification that browser
            # is at beginning of history
            pass
        else:
            self._history.pop()
            self._cursor =- 1

    def truncate(self):
        '''Remove all future history items, inclusive of
        the current page
        '''
        if self._cursor is not None:
            self._history = self._history[:self._cursor + 1]
            self._cursor = self._cursor - 1

    def get_page(self, idx: int) -> dict:
        '''Get page item from the browser history

        :param idx: History position index
        :type page: int
        :return: DOM and str representation of page
        :rtype: dict
        '''
        return self._history[idx]

    def get_current_page(self) -> dict:
        '''Get DOM and str representation of the page
        marked current in browser history.

        :param idx: History position index
        :type page: dict
        :return: DOM and str representation of page
        :rtype: dict
        '''
        return self.get_page(self._cursor)