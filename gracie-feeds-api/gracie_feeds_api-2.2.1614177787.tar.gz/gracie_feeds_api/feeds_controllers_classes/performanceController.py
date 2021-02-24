from gracie_feeds_api import GracieBaseAPI


class performanceController(GracieBaseAPI):
    """Performance Controller"""

    _controller_name = "performanceController"

    def enable(self, enabled):
        """Switch enableStatistics flag ON.

        Args:
            enabled: (boolean): enabled

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/performance/enable'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self):
        """Return the statistics instance."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/performance/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
