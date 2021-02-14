import socket
import sys

from gozer_engine.base import BaseComponent

class NetworkClient(BaseComponent):
    def send_request(self, uri: str):
        '''Send network request to designated Gopher host

        :param uri: Gopher host address with optional selector
        :type uri: str
        '''
        # Assume Gopher protocol unless explicity
        # defined as otherwise
        if '://' in uri:
            protocol, addr = uri.split('://')
        else:
            protocol = None
            addr = uri

        # If no trailing slash in URI, we still need
        # a value to be unpacked into gopher_path
        host, *gopher_path = addr.split('/', maxsplit=1)

        if protocol and protocol.lower() != 'gopher':
            sys.exit('Only Gopher URIs accepted. Please submit a URI with the gopher:// protocol.')
            # TODO: Other error handling
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 70))
            # Per RFC 1463, the frist send must be an empty line
            # which prompts the server to send a list of available
            # gopher_paths.
            if not gopher_path:
                s.sendall(f'\n'.encode('utf-8'))
            else:
                s.sendall(f'{gopher_path[0]}\n'.encode('utf-8'))
            resp = s.makefile(mode='r', errors='ignore')
            content = resp.read()
            s.close()
            s = None

        self.mediator.notify(self, {
            'msg': 'response_received',
            'data': {
                'resp_str': content
            }
        })