from gracie_feeds_api import GracieBaseAPI


class entitiesController(GracieBaseAPI):
    """Entities Controller"""

    _controller_name = "entitiesController"

    def getTopicEntities(self, languageId, name, **kwargs):
        """Return JSON array of the objects which represent the entities with the requested name.

        Args:
            languageId: (string): languageId
            maxEntitiesNumber: (integer): maxEntitiesNumber
            name: (string): name
            onlyMainNames: (boolean): onlyMainNames
            sortByPopularity: (boolean): sortByPopularity
            topicTypeId: (string): topicTypeId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': True, 'in': 'query'}, 'maxEntitiesNumber': {'name': 'maxEntitiesNumber', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'sortByPopularity': {'name': 'sortByPopularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/getTopicEntities'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def topicRetrieve(self, entityId):
        """Return the entity with specified ID.

        Args:
            entityId: (string): entityId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/topic/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
