import threading
import time

import requests


def new_default_http_client(*args, **kwargs):
    if requests:
        return RequestsClient(*args, **kwargs)
    else:
        raise Exception(
            "Requests must be installed as it is currently the only option for an HTTP client."
        )


class HttpClient:
    MAX_DELAY = 2  # in seconds
    INITIAL_DELAY = 0.5  # in seconds

    def __init__(self):
        self._thread_local = threading.local()

    def request_with_retries(self, method, url, headers, post_data=None):
        num_retries = 0
        while True:
            try:
                response = self.request(method, url, headers, post_data)
                connection_error = None
            except Exception as e:  # TODO: use custom error
                response = None
                connection_error = e

            if self._should_retry(response, connection_error, num_retries):
                num_retries += 1
                sleep_time = self._sleep_time_seconds(num_retries, response)
                time.sleep(sleep_time)
            else:
                if response is not None:
                    return response
                else:
                    raise Exception  # TODO: raise connection error

    def request(self, method, url):
        raise NotImplementedError(
            f"HttpClient sublcass must implement `request` method."
        )

    @property
    def _max_network_retries(self):
        from circle import max_network_retries

        return max_network_retries

    def _should_retry(self, response, api_connection_error, num_retries):
        if num_retries > self._max_network_retries:
            return False

        if response is None:
            # TODO: we eventually want the subclasses to handle this. for now, default to not retry on connection
            # issues/timeouts.
            return False

        content, status_code, rheaders = response

        if status_code >= 500:
            print("should retry...")
            return True
        return False

    def _sleep_time_seconds(self, num_retries, response=None):
        sleep_seconds = min(
            self.MAX_DELAY, self.INITIAL_DELAY * (2 ** (num_retries - 1))
        )  # Double delay with each retry until we reach the max delay

        return sleep_seconds


class RequestsClient(HttpClient):
    name = "requests"

    def __init__(self, timeout=30, **kwargs):
        self._timeout = timeout
        self._session = None
        super().__init__(**kwargs)

    def request(self, method, url, headers, post_data=None):

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

        try:
            res = self._thread_local.session.request(
                method,
                url,
                headers=headers,
                data=post_data,
                timeout=self._timeout,
            )
        except Exception as e:  # TODO: update exception
            raise e

        return res.content, res.status_code, res.headers
