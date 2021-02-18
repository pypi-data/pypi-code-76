"""Parse configuration from environment variables."""
import os

from unimatrix.lib import environ


#: Indicates that the application is running in debug mode.
DEBUG = os.getenv('DEBUG') == '1'

#: Specifies which hosts may make requests to application, based on the
#: content of the ``Host`` header.
HTTP_ALLOWED_HOSTS = environ.parselist(
    os.environ, 'HTTP_ALLOWED_HOSTS', sep=';')

#: Indicate if Cross-Origin Resource Sharing (CORS) is enabled for the
#: application.
HTTP_CORS_ENABLED = environ.parsebool(os.environ, 'HTTP_CORS_ENABLED')

#: The allowed origins as determined based on the ``Origin`` header setting
#: for Cross-Origin Resource Sharing (CORS).
HTTP_CORS_ALLOW_ORIGINS = environ.parselist(
    os.environ, 'HTTP_CORS_ALLOW_ORIGINS', sep=';')

#: The allowed request methods for cross-origin requests.
HTTP_CORS_ALLOW_METHODS = environ.parselist(
    os.environ, 'HTTP_CORS_ALLOW_METHODS', sep=':')

#: The allowed request headers setting for Cross-Origin Resource Sharing (CORS).
HTTP_CORS_ALLOW_HEADERS = environ.parselist(
    os.environ, 'HTTP_CORS_ALLOW_HEADERS', sep=':')

#: Indicates if cross-origin responses may include cookies.
HTTP_CORS_ALLOW_CREDENTIALS = environ.parsebool(
    os.environ, 'HTTP_CORS_ALLOW_CREDENTIALS')

#: The list of response headers that may be included in a cross-origin
#: response, separated by a colon.
HTTP_CORS_EXPOSE_HEADERS = environ.parselist(
    os.environ, 'HTTP_CORS_EXPOSE_HEADERS', sep=':')

#: Specifies the maximum time in seconds that a browser may cache a CORS
#: response. Defaults to ``600``.
HTTP_CORS_TTL = environ.parseint(
    os.environ, 'HTTP_CORS_TTL', default=600)

#: The default secret key.
SECRET_KEY = os.getenv('SECRET_KEY')
