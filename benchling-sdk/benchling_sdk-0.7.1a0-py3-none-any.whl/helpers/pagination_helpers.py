from typing import Any, Iterable, Iterator, List, Optional, TypeVar

from benchling_api_client.types import Response
from typing_extensions import Protocol

from benchling_sdk.helpers.logging_helpers import sdk_logger
from benchling_sdk.helpers.response_helpers import model_from_detailed

# TODO BNCH-15439 Make bounded if we can inherit from a common model
ResultsBody = TypeVar("ResultsBody")
Model = TypeVar("Model")
NextToken = str

RESULTS_COUNT_HEADER = "Result-Count"


class PagedApiCall(Protocol):
    def __call__(self, next_token: NextToken) -> Response[Any]:
        ...


class ResultsExtractor(Protocol):
    def __call__(self, body: Any) -> Optional[List[Any]]:
        ...


class TokenExtractor(Protocol):
    def __call__(self, body: Any) -> NextToken:
        ...


class LengthExtractor(Protocol):
    def __call__(self, response: Response[Model]) -> Optional[int]:
        ...


def _default_token_extractor(body: ResultsBody) -> NextToken:
    """
    A default method that returns the `next_token` from a model returned by
    the API. Since the generated API models do not inherit from a common base class,
    the `ResultsBody` type is unbounded.

    :param body: A model returned from the API which should have a `next_token` attribute
    :return: A str of the `next_token` from the results body
    """
    return body.next_token  # type: ignore


def _default_length_extractor(response: Response[Model]) -> Optional[int]:
    """
    A default method that returns the estimated length of total available results from the API.
    It will return None if the API did not indicate how many results were available.

    :param response: A response returned from the API
    :return: An optional int containing the estimated length of the results
    """
    if (
        response.headers
        and RESULTS_COUNT_HEADER in response.headers
        and response.headers[RESULTS_COUNT_HEADER].isdigit()
    ):
        return int(response.headers[RESULTS_COUNT_HEADER])
    return None


class PageIterator(Iterable[List[Model]]):
    """
    Used to paginate arbitrary Benchling API endpoints which support the
    concept of a `next_token` for pointing to subsequent pages of results. Supporting API
    endpoints typically return a "results body" object which contains a key for `next_token`,
    as well as a key for a collection of results representing the current page.

    Any API errors encountered during retrieval of a page will be marshaled to
    :class:`benchling_sdk.errors.BenchlingError`.
    """

    _api_call: PagedApiCall
    _results_extractor: ResultsExtractor
    _token_extractor: TokenExtractor
    _length_extractor: LengthExtractor
    _next_token: Optional[NextToken]
    _approximate_length: Optional[int]

    def __init__(
        self,
        api_call: PagedApiCall,
        results_extractor: ResultsExtractor,
        token_extractor: TokenExtractor = _default_token_extractor,
        length_extractor: LengthExtractor = _default_length_extractor,
    ) -> None:
        """
        :param api_call: A Callable that accepts a str for the next_token
        :param results_extractor: A Callable that can extract a list of models from a results body
        :param token_extractor: A Callable that can extract the next_token str value from a results body
        :param length_extractor: A Callable that can extract the approximated available results
            count from a response
        """
        self._api_call = api_call
        self._results_extractor = results_extractor
        self._token_extractor = token_extractor
        self._length_extractor = length_extractor
        self._next_token = None
        self._approximate_length = None

    @property
    def next_token(self) -> Optional[NextToken]:
        """Returns the last nextToken provided by the API, if applicable"""
        return self._next_token

    @property
    def estimated_count(self) -> Optional[int]:
        """Returns the value of the Result-Count header provided by the API, if applicable.
        Some endpoints may not implement this header. This value will also not be available until
        the iterator has been advanced to make an API call (e.g., via `next()`).
        """
        return self._approximate_length

    def __iter__(self) -> Iterator[List[Model]]:
        return self

    def __next__(self) -> List[Model]:
        if self._next_token is None or len(self._next_token) > 0:
            return self._fetch_data()
        raise StopIteration

    def _fetch_data(self) -> List[Model]:
        next_token = self._next_token if self._next_token else ""
        response: Response[Model] = self._api_call(next_token)
        result_body: Model = model_from_detailed(response)
        self._approximate_length = self._length_extractor(response)
        self._next_token = self._token_extractor(result_body)
        sdk_logger.debug(
            "Next token: %s Approximate Result Count: %s", self._next_token, self._approximate_length
        )
        data = self._results_extractor(result_body)
        return [] if data is None else data
