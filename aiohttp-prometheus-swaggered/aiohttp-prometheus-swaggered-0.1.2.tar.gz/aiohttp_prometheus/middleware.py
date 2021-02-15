from aiohttp import web
from time import time
from functools import partial
from prometheus_client import Counter, Histogram

BUCKETS = (0.01, 0.05, 0.1, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0)

requests_total = Counter(
    namespace='aiohttp',
    subsystem='http',
    name='requests_total',
    documentation='Asyncio total Request Count',
    labelnames=['method', 'handler', 'status']
)

request_duration = Histogram(
    namespace='aiohttp',
    subsystem='http',
    name='request_duration_seconds',
    documentation='Request latency',
    labelnames=['method', 'handler'],
    buckets=BUCKETS,
)


@web.middleware
async def metrics_middleware(
    request: web.Request,
    handler
) -> web.Response:
    """Middleware captures request execution statuses,
    request method, request execution time and increments
    the corresponding counters"""

    start_time = time()
    match_info = request.match_info.route.resource.get_info()
    handler_name = match_info.get('path', match_info.get('formatter', 'undefined').replace('}', '>').replace('{', '<'))

    try:
        response = await handler(request)
        spent = time() - start_time
        requests_total.labels(request.method, handler_name, classify_status_code(response.status)).inc()
        request_duration.labels(request.method, handler_name).observe(spent)
        return response
    except:
        spent = time() - start_time
        requests_total.labels(request.method, handler_name, '5xx').inc()
        request_duration.labels(request.method, handler_name).observe(spent)

        raise


def classify_status_code(status_code):
    """
    Prometheus recomends to have lower number of cardinality,
    each combination creates a new metric in datastore,
    to reduce this risk we store only the class of status code
    """
    if 200 <= status_code < 300:
        return "2xx"

    if 300 <= status_code < 400:
        return "3xx"

    if 400 <= status_code < 500:
        return "4xx"

    return "5xx"
