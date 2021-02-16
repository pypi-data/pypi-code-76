from circle import api_requestor, util


class CircleObject(dict):
    def __init__(self, id=None, api_key=None, **params):
        super().__init__()

        self._unsaved_values = (
            set()
        )  # Values that haven't change in a refresh and should persist to the new state
        self._transient_values = set()
        self._retrieve_params = params
        # TODO: I forget why I did this?
        for k, v in params.items():
            self.__setattr__(k, v)

        self.__setattr__("api_key", api_key)

        if id:
            self["id"] = id

    def __setattr__(self, k, v):
        if k[0] == "_" or k in self.__dict__:
            return super().__setattr__(k, v)
        self[k] = v
        return None

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError as e:
            raise AttributeError(e)

    @classmethod
    def construct_from(cls, values, api_key):
        instance = cls(values.get("id"), api_key=api_key)
        instance.refresh_from(values, api_key)
        return instance

    def request(self, method, url, params=None, headers=None):

        requestor = api_requestor.APIRequestor(api_key=self.api_key)
        response, api_key = requestor.request(method, url, params, headers)

        return util.convert_to_circle_object(response, api_key)

    def refresh_from(self, values, api_key=None, partial=False, last_response=None):
        self.api_key = api_key or getattr(values, "api_key", None)
        if partial:
            # Record values that aren't set but, since this is partial=True, will persist to the new state
            self._unsaved_values = self._unsaved_values - set(values)
        else:
            removed = set(self.keys()) - set(values)
            self._transient_values = (
                self._transient_values | removed
            )  # include existing transient values and any removed values
            self._unsaved_values = (
                set()
            )  # This is not a partial update, so all state will be refreshed.
            self.clear()

        self._transient_values = self._transient_values - set(values)

        for k, v in values.items():
            super().__setitem__(
                k,
                util.convert_to_circle_object(
                    v, api_key, klass_name=self.__class__.__name__
                ),
            )
