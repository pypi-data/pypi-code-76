from gracie_dictionary_api import GracieBaseAPI


class blacklistKeywordController(GracieBaseAPI):
    """Blacklist Keyword Controller"""

    _controller_name = "blacklistKeywordController"

    def add(self, name, **kwargs):
        """

        Args:
            folderId: (string): Id is some of { topic, topic-type, skillset, skill, cluster set, cluster group, cluster }
            languageId: (string): Language id for new blacklist keyword, default to user language
            name: (string): Name of new blacklist keyword

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, **kwargs):
        """

        Args:
            ids: (array): Ids of existing blacklist keyword to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing blacklist keyword to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            folderId: (string): Id is some of { topic, topic-type, skillset, skill, cluster set, cluster group, cluster }
            languageId: (string): * - request keywords in all languages. For sorting folders by proximity user's language is used.
            languageId: (integer): Language id for results, default to user language
            offset: (integer): Start offset for results
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): { "NONE", "NAME", "WEIGHT", "PROXIMITY", "DOC2VEC", "KEYWORDS", "ENTITIES" }

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing blacklist keyword to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
