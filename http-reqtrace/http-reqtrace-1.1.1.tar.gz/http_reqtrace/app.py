import logging
import time
from flask import Flask, request
from flask.logging import create_logger
from prometheus_flask_exporter import PrometheusMetrics
from . import __version__

app = Flask(__name__)

# Logger Setup
LOGGER = create_logger(app)
LOGGER.setLevel(logging.INFO)


# Metrics set-up
metrics = PrometheusMetrics(app)
metrics.info('up', 'Application health')
metrics.info('info', 'Application information', version=__version__)


@app.route('/healthz')
@metrics.do_not_track()
def healthz():
    """ Healthz endpoint """
    return ''


@app.route('/status/<int:status_code>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def status(status_code: int):
    """ Returns a response with the given status code. """
    return _generic_response(status_code=status_code)


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path: str):  # pylint: disable=unused-argument
    """ Catch all routes. """
    return _generic_response()


def _generic_response(status_code=200):
    # Check if latency is given or not.
    latency_in_ms_argument = request.args.get('latencyInMs', '')
    latency_in_ms = 0
    if latency_in_ms_argument.isdigit():
        latency_in_ms = int(latency_in_ms_argument)

    # Logs input.
    LOGGER.info('> [%s] %s %s', request.method, request.environ.get('SERVER_PROTOCOL'), request.url)
    for header_name, header_value in request.headers.items():
        LOGGER.info('>>     Header : %s : %s', header_name, header_value)

    for query_name, query_value in request.args.items():
        LOGGER.info('>>     Query  : %s : %s', query_name, query_value)

    LOGGER.info('>>     Body   : %s', request.data)

    # Sleeping to simulate latency.
    if latency_in_ms > 0:
        LOGGER.info('<< Waiting for timeout exhaust: %sms.', latency_in_ms)
        time.sleep(latency_in_ms / 1000)

    # Handle response.
    LOGGER.info('< [ HTTP %s ]', status_code)
    message = 'OK' if (200 <= status_code < 400) else 'KO'
    return {'statusCode': status_code, 'message': message}, status_code
