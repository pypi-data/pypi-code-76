from gracie_feeds_api import GracieBaseAPI


class invalidateController(GracieBaseAPI):
    """Invalidate user's session forcefully."""

    _controller_name = "invalidateController"

    def invalidate(self, id):
        """Invalidate user's session forcefully.

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/invalidate'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
