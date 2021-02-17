import logging
import mimetypes
import os

from aiohttp import web


class DebugUIEndpoint:

    def __init__(self, session, middlewares=()):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.app = web.Application(middlewares=middlewares)
        self.session = session
        self.endpoints = {}
        self.setup_routes()

    def add_endpoint(self, prefix, endpoint):
        self.endpoints[prefix] = endpoint
        self.app.add_subapp(prefix, endpoint.app)

    def setup_routes(self):
        self.app.add_routes([web.get('/{path:.*}', self.return_files)])

    async def return_files(self, request):
        path = request.match_info['path'] if request.match_info['path'] else 'index.html'
        resource_dir = os.path.join(os.path.dirname(__file__), 'app', 'dist')
        filename = os.path.normpath(os.path.join(resource_dir, path))
        if filename.startswith(resource_dir):
            response = web.FileResponse(filename)
            response.content_type = mimetypes.guess_type(path)[0]
            return response
