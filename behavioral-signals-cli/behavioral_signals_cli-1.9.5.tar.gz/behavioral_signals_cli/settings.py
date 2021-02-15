API_PROCESSING_REQUIRED_METADATA = ['filename', 'channels', 'calldirection']

NUM_PROCESSING_REQUIRED_METADATA = len(API_PROCESSING_REQUIRED_METADATA)

MAX_REQUESTS_PER_SEC = 100

REQUESTS_LIMIT_PERIOD_SECS = 1

# Calculate the max rate limit as half of the max request per sec, since two http requests are required to get result.
# Lowered by 5% which functions as a gurad that takes into account variations rate limiter both on CLI and API
MAX_REQUESTS_PER_SEC_PER_ENDPOINT = int((MAX_REQUESTS_PER_SEC / 2) - (MAX_REQUESTS_PER_SEC / 2) * 0.05)

MAX_POLLING_WINDOW = int((MAX_REQUESTS_PER_SEC / 2) - (MAX_REQUESTS_PER_SEC / 2) * 0.05)

DEFAULT_POLLING_WINDOW = min(5, MAX_POLLING_WINDOW)

MAX_ASYNC_UPLOADS = int((MAX_REQUESTS_PER_SEC / 2) - (MAX_REQUESTS_PER_SEC / 2) * 0.05)

DEFAULT_ASYNC_UPLOADS = min(5, MAX_ASYNC_UPLOADS)

API_CONNECTION_TIMEOUT = 5
