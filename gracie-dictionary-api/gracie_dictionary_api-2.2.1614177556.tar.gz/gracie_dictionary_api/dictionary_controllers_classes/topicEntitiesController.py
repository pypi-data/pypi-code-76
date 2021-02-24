from gracie_dictionary_api import GracieBaseAPI


class topicEntitiesController(GracieBaseAPI):
    """Topic Entities Controller"""

    _controller_name = "topicEntitiesController"

    def add(self, names, popularity, topicTypeId, **kwargs):
        """

        Args:
            alias: (string): Alias of new topic entity
            briefs: (string): Briefs to assign to the new topic entity, an array of:{ "text": "...brief text...", "languageId": "...long id..." }if you only pass one brief, you can omit the languageId
            names: (string): Names to assign to the new topic entity, an array of:{ "name":  "somename", "isMainName":"true", "languageId": "....long id....." }and one of the names must have isMainName == true
            popularity: (integer): Popularity of new topic entity, value should be 0 to 4 in increasing order of popularity
            topicTypeId: (string): Id of topic type of new topic entity

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}, 'names': {'name': 'names', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': True, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, ids):
        """

        Args:
            ids: (array): List of topic entity ids to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def clone(self, id, topicTypeId, **kwargs):
        """

        Args:
            deleteSource: (boolean): Delete original topic entity after cloning
            id: (string): Id of topic entity to clone
            popularity: (integer): Popularity value of cloned entity, value should be 0 to 4 in increasing order of popularity
            topicTypeId: (string): Id of topic type to receive cloned entity

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'deleteSource': {'name': 'deleteSource', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/clone'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of topic entity to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def downloadExportFile(self, taskId):
        """

        Args:
            taskId: (string): Id of export entity task

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'taskId': {'name': 'taskId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/downloadExportFile'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): Id of topic entity to edit
            popularity: (integer): New popularity, value should be 0 to 4 in increasing order of popularity
            topicTypeId: (string): Id of topic type to move this topic entity to

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportTopicEntities(self, topicTypeId, **kwargs):
        """

        Args:
            languageId: (string): Language Id of entities to export, default is caller's language
            topicTypeId: (string): Id of topic type to export entities from

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/exportTopicEntities'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def importTopicEntities(self, file, topicTypeId, **kwargs):
        """

        Args:
            file: (file): File containing topic entities to import
            languageId: (string): Language Id for imported entities, default is caller's language
            stopOnError: (boolean): Stop processing entities if an error occurs
            topicTypeId: (string): Id of topic type to receive imported entities

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'stopOnError': {'name': 'stopOnError', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/importTopicEntities'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            languageId: (string): Id of language to match on, defaults to callers language
            limit: (integer): Limit the number of entities returned
            name: (string): Entity name prefix to match on, case insensitive
            offset: (integer): Start offset of returned list
            onlyMainNames: (boolean): Only return main names
            orderAsc: (boolean): Sort result in ascending order
            orderBy: (string): Sort order of returned entities, one of [NAME, TOPIC, TOPIC_TYPE, POPULARITY]
            topicId: (string): Limit list of entities to those belonging to the specified topic
            topicTypeId: (string): Limit list of entities to those belonging to the specified topic type

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'topicId': {'name': 'topicId', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def restore(self, id):
        """

        Args:
            id: (string): Id of topic entity to restore

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/restore'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of topic entity to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
