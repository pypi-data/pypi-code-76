# encoding: utf-8

import socket
import logging_helper
from future.utils import iteritems
from requests.models import Response as _Resp
from http.server import BaseHTTPRequestHandler
from requests.structures import CaseInsensitiveDict
from ..helpers.encoding import encode_requests_response
from ..methods.shared import Shared

logging = logging_helper.setup_logging()


class Response(Shared):

    def __init__(self,
                 response=None,
                 *args,
                 **kwargs):

        """
        
        :param response:    Optionally provide a requests.Response object that will be
                            used to initialise this object
        """

        super(Response, self).__init__(*args,
                                       **kwargs)

        self.canned_responses = BaseHTTPRequestHandler.responses

        # Initialise response parameters with defaults
        self.headers = {u'content-length': 0}
        self.content = None
        self.status = 200  # Start with a good status, any errors will modify this!

        # If response passed then update
        if response is not None:
            self.update_response(response=response)

    def update_response(self,
                        response):

        # Response parameters
        if isinstance(response, _Resp):
            # Initialise response from requests.Response object
            encode_requests_response(response)

            self.headers = response.headers
            self.content = response.content
            self.status = response.status_code

        else:
            logging.error(u'Cannot update response as passed response is not a requests response object.')

    def generate_error(self,
                       err,
                       status=500):  # Internal server error

        # Setup error response
        self.status = status
        self.content = u''

        # Check if we can get a defined description for failure.
        if self.canned_responses.get(self.status):
            self.content += (u'<h1>{short}</h1>'
                             u'<p>{long}:</p>'.format(short=self.canned_responses[self.status][0],
                                                      long=self.canned_responses[self.status][1]))

        self.content += (u'<pre>{err}</pre>'.format(err=err))

        # Headers must be last so we generate correct content length!
        self.headers = {u'Content-Type': u'text/html',
                        u'Connection': u'close',
                        u'content-length': len(self.content)}

    def prepare_headers(self,
                        modified_headers=None):

        if modified_headers is None:
            modified_headers = {}  # Initialise modifier_headers if not provided

        # Push the modified headers to a case insensitive dict so that
        # the case does not have to be checked when fetching from
        # the dictionary
        modified_headers = CaseInsensitiveDict(data=modified_headers)

        logging.debug(self.prefix_message(u'Modified headers: {h}'.format(h=modified_headers)))

        # Check for and remove chunked transfer encoding
        for header in self.headers.keys():
            if header.lower() == u'transfer-encoding' and u'chunked' in self.headers[header]:
                logging.debug(self.prefix_message(u'Removing chunked transfer-encoding'))
                del self.headers[header]

        try:
            original_header_length = self.headers[[h for h in self.headers if h.lower() == u'content-length'][0]]
        except IndexError:
            original_header_length = None

        # Apply modified headers
        for modified_header in modified_headers:
            try:
                header = [h for h in self.headers if h.lower() == modified_header.lower()][0]
            except IndexError:
                self.headers[modified_header] = modified_headers[modified_header]
                logging.info(self.prefix_message(u'Adding header to response {k}: {v}'
                                                 .format(k=modified_header,
                                                         v=modified_headers[modified_header])))
            else:
                del self.headers[header]
                self.headers[header] = modified_headers[modified_header]
                logging.info(self.prefix_message(u'Modifying response header {k}: {v}'
                                                 .format(k=header,
                                                         v=modified_headers[modified_header])))

        # update content-length
        try:
            content_length_header = [h for h in self.headers if h.lower() == u'content-length'][0]
        except IndexError:
            logging.warning('Message has no content-length')
        else:
            if self.headers[content_length_header] == "?" or content_length_header not in modified_headers:
                logging.info(self.prefix_message(u'Updating content-length to reflect modifications '
                                                 u'to content ({o} -> {len}).'.format(o=original_header_length,
                                                                                      len=len(self.content))))
                self.headers[content_length_header] = len(self.content)
            elif content_length_header not in modified_headers:
                logging.warning(self.prefix_message(u'Using explicit modified content-length: {m}. Actual: {a} '
                                                    .format(m=self.headers[content_length_header],
                                                            a=len(self.content))))
        headers_to_remove = [k for k, v in iter(self.headers.items()) if v is None]
        if headers_to_remove:
            logging.info(self.prefix_message('Removing headers: {h}'
                                             .format(h=', '.join(headers_to_remove))))

            self.headers = CaseInsensitiveDict({k: v
                                                for k, v in iter(self.headers.items())
                                                if v is not None})

    def _send_headers(self):

        # Send the headers
        for header, value in iteritems(self.headers):
            try:
                self._request.send_header(header, value)

            except Exception as err:
                logging.debug(self.prefix_message(u'Error Sending header '
                                                  u'({header}:{value}) '
                                                  u'to {client} for {url}!'.format(header=header,
                                                                                   value=value,
                                                                                   client=self.client_address,
                                                                                   url=self.request_uri)))
                logging.error(self.prefix_message(err))
            else:
                logging.debug(self.prefix_message(u'Sent header '
                                                  u'({header}:{value}) '
                                                  u'to {client} for {url}!'.format(header=header,
                                                                                   value=value,
                                                                                   client=self.client_address,
                                                                                   url=self.request_uri)))
        # Notify end of headers
        try:
            logging.debug(self.prefix_message(u'Sending end headers for response'))
            self._request.end_headers()

        except Exception as err:
            logging.exception(self.prefix_message(u'Error sending end headers for response'))
            raise err

    def respond(self):

        try:
            # This Sends the response code plus Server & Date headers
            logging.debug(self.prefix_message(u'Sending status ({s})'.format(s=self.status)))
            self._request.send_response(self.status)

            # Send our response headers including the "End Header" message
            self._send_headers()

            # Check whether we should send content body
            # --> HEAD requests expect no body
            # --> only send if status code is 200 or above
            # --> do not send if status code is 204 (No Content) or 304 (Not Modified)
            if self._request.command.upper() != u'HEAD' and self.status >= 200 and self.status not in (204, 304):
                # Send content body
                logging.debug(self.prefix_message(u'Sending content'))
                try:
                    self._request.wfile.write(str(self.content))  # PY2
                except TypeError:
                    logging.info(self.content.__class__)
                    self._request.wfile.write(bytes(self.content), 'utf-8')  # PY3

                try:
                    logging.debug(self.prefix_message(u'Content: {content}'.format(content=str(self.content))))

                except UnicodeDecodeError:
                    logging.debug(self.prefix_message(u'Content: <UnicodeDecodeError>'))

        except socket.error as err:
            self._request.close_connection = 1  # Stop any further connections as we have a socket error
            self._log_error(err=err,
                            log_msg=u'Response socket error',
                            exception=False)

        except Exception as err:
            self._request.close_connection = 1  # Stop any further connections as we have a socket error
            self._log_error(err=err,
                            log_msg=u'Error sending response to client')
