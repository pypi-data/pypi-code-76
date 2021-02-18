from arc.middleware import Middleware
from arc.errors import AppException
import os
import pathlib


class DefaultMiddleware(Middleware):
    def process_request(self, req):
        print(f"\n[REQUEST][{req.method}] {req.url}")

    def process_response(self, req, res):
        print(f"\n[RESPONSE] {req.url}")


class DefaultExceptionHandler:
    def __init__(self, app):
        self.app = app

    def handle_error(self, request, response, error):
        response.status_code = 500
        response.body = self.app.custom_template(pathlib.Path("selfpages").absolute(),
                                                 "index.html", context={"error": str(error)})

error_404 = open(os.path.join(os.path.abspath(r"selfpages"), os.path.abspath(r"error-404.html")))