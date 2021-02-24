from gracie_dictionary_api import GracieBaseAPI


class tagController(GracieBaseAPI):
    """Tag Controller"""

    _controller_name = "tagController"

    def add(self, key, type, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default adds to root tags
            included: (boolean): Include tag is processing results
            key: (string): Name of new tag
            type: (string): Type of new tag, one of [INTERNAL, EXTERNAL]
            value: (string): List of new tag values

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'included': {'name': 'included', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}, 'type': {'name': 'type', 'required': True, 'in': 'query'}, 'value': {'name': 'value', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, keys, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default deletes root tag
            keys: (array): List of tag names to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'keys': {'name': 'keys', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, key, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default deletes root tag
            key: (string): Name of tag to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, key, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default edits root tag
            included: (boolean): Include tag is processing results
            key: (string): Name of tag to edit
            value: (string): Value to add to named tag

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'included': {'name': 'included', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}, 'value': {'name': 'value', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default returns root tags
            internalFilter: (string): Limit results to tags of the specified type, one of [ALL, INTERNAL, EXTERNAL]
            limit: (integer): Number of results to return
            offset: (integer): Initial offset into result list
            orderAsc: (boolean): Return results in ascending order
            orderBy: (string): Sort order of results, one of [KEY, TYPE]

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'internalFilter': {'name': 'internalFilter', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, key, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default retrieves root tag
            key: (string): Name of tag to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def search(self, **kwargs):
        """

        Args:
            folderId: (string): Id of [topic, topic-type, skill, profile, profile-class], default returns root tags
            internalFilter: (string): Limit results to tags of the specified type, one of [ALL, INTERNAL, EXTERNAL]
            keyName: (string): Tag name prefix to match on, case insensitive.
            limit: (integer): Number of results to return
            offset: (integer): Initial offset into result list
            orderAsc: (boolean): Return results in ascending order
            orderBy: (string): Sort order of results, one of [KEY, TYPE]

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'internalFilter': {'name': 'internalFilter', 'required': False, 'in': 'query'}, 'keyName': {'name': 'keyName', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/search'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
