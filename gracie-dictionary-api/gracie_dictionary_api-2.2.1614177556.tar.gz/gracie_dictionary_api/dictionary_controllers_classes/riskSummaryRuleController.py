from gracie_dictionary_api import GracieBaseAPI


class riskSummaryRuleController(GracieBaseAPI):
    """Risk Summary Rule Controller"""

    _controller_name = "riskSummaryRuleController"

    def addLabel(self, id, label):
        """

        Args:
            id: (string): Id of risk summary rule to add label to
            label: (string): Label to add to risk summary rule

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/addLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def create(self, excludeRefs, includeRefs, operation, riskLabel):
        """

        Args:
            excludeRefs: (array): List of risk labels to exclude
            includeRefs: (array): List of classifier risk rule labels to include in the operation, can be any combination of [RiskLabel, "All", "AllClassifier", "AllEntity"]
            operation: (string): Operation to apply to all matching classifier risk rule values, one of [COUNT, MEAN, MEDIAN, MODE, MAX, SUM, RANGE]
            riskLabel: (string): Risk label to apply if classifier risk rule matches

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'excludeRefs': {'name': 'excludeRefs', 'required': True, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': True, 'in': 'query'}, 'operation': {'name': 'operation', 'required': True, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/create'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            excludeRefs: (array): New list of risk summary rule labels to exclude
            id: (string): Id of risk summary rule to change
            includeRefs: (array): New list of risk summary rule labels to include
            operation: (string): New risk summary rule operation
            riskLabel: (string): New risk summary rule label

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'excludeRefs': {'name': 'excludeRefs', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': False, 'in': 'query'}, 'operation': {'name': 'operation', 'required': False, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): Limit list of risk summary rules to those with the specified label

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'label': {'name': 'label', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def listLabels(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/riskSummaryRules/listLabels'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
        """

        Args:
            id: (string): Id of risk summary rule to remove

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeLabel(self, id, label):
        """

        Args:
            id: (string): Id of classifier risk rule to remove label from
            label: (string): Label to remove from classifier risk rule

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/removeLabel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of rule to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
