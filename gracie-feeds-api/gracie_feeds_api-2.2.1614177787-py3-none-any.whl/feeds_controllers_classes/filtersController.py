from gracie_feeds_api import GracieBaseAPI


class filtersController(GracieBaseAPI):
    """Filters management."""

    _controller_name = "filtersController"

    def getFiltersTree(self, alertRuleId):
        """Get filters tree.

        Args:
            alertRuleId: (string): alertRuleId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/getFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeFiltersTree(self, alertRuleId):
        """Remove filters tree.

        Args:
            alertRuleId: (string): alertRuleId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/removeFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def setFiltersTree(self, alertRuleId, filters):
        """Set filters tree.

        Args:
            alertRuleId: (string): alertRuleId
            filters: (string): filters

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'filters': {'name': 'filters', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/setFiltersTree'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
