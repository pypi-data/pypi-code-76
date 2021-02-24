from typing import Optional, Any

from pydantic import BaseModel

from ..connection import Connection
from ..serialization.deserialization import json_loads
from ..serialization.serialization import json_dumps
from ... import TeralityInternalError


class _PandasJob(BaseModel):
    function_type: str
    function_accessor: Optional[str]
    function_name: str
    args: str
    kwargs: str


def call_pandas_function(function_type: str, function_prefix: Optional[str], function_name: str,
                         *args, **kwargs) -> Any:
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    job = _PandasJob(function_type=function_type, function_accessor=function_prefix, function_name=function_name,
                     args=json_dumps(args), kwargs=json_dumps(kwargs))

    response_json = Connection.send_request('compute', job.json())
    response = json_loads(response_json)

    # Poll the server until the result is available.
    while response['status'] == 'pending':
        response_json = Connection.send_request('follow_up', {'function_id': response['pending']})
        response = json_loads(response_json)

    if response['status'] != 'finished':
        raise TeralityInternalError('Received response with neither `pending` nor `finished` status')
    result = response['result']
    inplace = response.get('inplace', False)

    # Handle in-place modification of data structures.
    # NOTE: Because `inplace` is only available on methods, the first argument is guaranteed to be positional (`self`).
    if inplace:
        from terality._terality.terality_structures.structure import Struct  # break cyclic import
        if not args or not isinstance(args[0], Struct):
            raise TeralityInternalError('Received in-place response but the target is not a data structure')
        target = args[0]
        if not isinstance(result, Struct):
            raise TeralityInternalError('Received in-place response but the result is not a data structure')
        target._assign(result)
        result = None

    return result
