import requests


class Client:
    class Method:
        GET = 'get'
        POST = 'post'
        PUT = 'put'
        PATCH = 'patch'
        DELETE = 'delete'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_auth(self, key: str, value: str) -> None:
        """
        Authorization  : {key} {value}
        """
        token = F"{key}{value}"
        setattr(self, 'token', token)

    def set_bearer_token(self, value: str) -> None:
        """
        Authorization  : bearer {value}
        """
        self.set_auth(
            key="Bearer ",
            value=value
        )

    @staticmethod
    def clear_endpoint(old_endpoint: str) -> str:
        new_endpoint = old_endpoint.replace('//', '/')
        new_endpoint = new_endpoint.replace(':/', '://')
        return new_endpoint

    def request(self, method, url, data=None, json=None, query_params=None, **kwargs) -> requests.Response:
        if data is None:
            data = {}
        if json is None:
            json = {}
        if query_params is None:
            query_params = {}
        endpoint = getattr(self, 'url', '') + url
        clear_endpoint = self.clear_endpoint(endpoint)
        headers = kwargs.pop('headers', {})
        headers.update({
            'Authorization': getattr(self, 'token', '')
        })
        if method == Client.Method.GET:
            return self._get(
                url=clear_endpoint,
                query_params=query_params,
                headers=headers,
                **kwargs
            )
        elif method == Client.Method.POST:
            return self._post(
                url=clear_endpoint,
                data=data,
                json=json,
                query_params=query_params,
                headers=headers,
                **kwargs
            )
        elif method == Client.Method.PUT:
            return self._put(
                url=clear_endpoint,
                data=data,
                headers=headers,
                query_params=query_params,
                **kwargs
            )
        elif method == Client.Method.PATCH:
            return self._patch(
                url=clear_endpoint,
                data=data,
                headers=headers,
                query_params=query_params,
                **kwargs
            )
        elif method == Client.Method.DELETE:
            return self._delete(
                url=clear_endpoint,
                data=data,
                headers=headers,
                query_params=query_params,
                **kwargs
            )

    @staticmethod
    def _get(url, query_params, **kwargs) -> requests.Response:
        return requests.get(
            url=url,
            params=query_params,
            **kwargs
        )

    @staticmethod
    def _post(url, data, json, query_params, **kwargs) -> requests.Response:
        return requests.post(
            url=url,
            data=data,
            json=json,
            params=query_params,
            **kwargs
        )

    @staticmethod
    def _put(url, data, query_params, **kwargs) -> requests.Response:
        return requests.put(
            url=url,
            data=data,
            params=query_params,
            **kwargs
        )

    @staticmethod
    def _patch(url, data, query_params, **kwargs) -> requests.Response:
        return requests.patch(
            url=url,
            data=data,
            params=query_params,
            **kwargs
        )

    @staticmethod
    def _delete(url, query_params, data, **kwargs) -> requests.Response:
        return requests.delete(
            url=url,
            data=data,
            params=query_params,
            **kwargs
        )
