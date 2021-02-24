from gracie_dictionary_api import GracieBaseAPI


class profileFeatureController(GracieBaseAPI):
    """Profile Feature Controller"""

    _controller_name = "profileFeatureController"

    def add(self, profileId, **kwargs):
        """

        Args:
            classOrEntityId: (string): Create profile-feature from one of { skillId, topicId, topicTypeId, topicEntityId, geoEntityId }.
            profileId: (string): Id of profile to assign feature

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'classOrEntityId': {'name': 'classOrEntityId', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of feature to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, profileId, **kwargs):
        """

        Args:
            orderAsc: (boolean): Sort returned list in ascending order
            orderBy: (string): Sort order of returned profile features, one of [TYPE, DESCRIPTION]
            profileId: (string): List profile features from the specified profile Id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile-feature

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
