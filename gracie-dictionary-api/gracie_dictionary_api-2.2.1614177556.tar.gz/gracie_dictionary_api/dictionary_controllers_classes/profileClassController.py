from gracie_dictionary_api import GracieBaseAPI


class profileClassController(GracieBaseAPI):
    """Profile Class Controller"""

    _controller_name = "profileClassController"

    def add(self, **kwargs):
        """

        Args:
            name: (string): Name of new profile-class
            profileId: (string): Id of existing profile

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'name': {'name': 'name', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFile(self, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            files: (array): List of files to upload to profile
            languageId: (string): Id of this Language to assign this profile, default to user language
            profileId: (string): Profile id of existing profile to assign

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'files': {'name': 'files', 'required': False, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFromSkill(self, **kwargs):
        """

        Args:
            addSkillIdToFeatures: (boolean): Automatically create profile-feature from the skill.
            profileId: (string): Id of existing profile
            skillId: (string): Id of existing skill

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFromSkill'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFromSkillset(self, **kwargs):
        """

        Args:
            addSkillIdToFeatures: (boolean): Automatically create profile-feature from each skill of skillset.
            profileId: (string): Id of existing profile
            skillsetId: (string): Id of existing skillset

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}, 'skillsetId': {'name': 'skillsetId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/addFromSkillset'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkAdd(self, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            addSkillIdToFeatures: (boolean): For skillIds and skillsetIds: Automatically create profile-feature from each skill of skillset.
            files: (array): List of files to upload to profile
            languageId: (string): Id of this Language to assign this profile-class, default to user language
            profileId: (string): Profile id of existing profile to add
            skillIds: (array): Ids of existing skill
            skillsetIds: (array): Ids of existing skillsets

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'addSkillIdToFeatures': {'name': 'addSkillIdToFeatures', 'required': False, 'in': 'query'}, 'files': {'name': 'files', 'required': False, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}, 'skillIds': {'name': 'skillIds', 'required': False, 'in': 'query'}, 'skillsetIds': {'name': 'skillsetIds', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/bulkAdd'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile-class to delete
            removeSkillIdFromFeatures: (boolean): Automatically remove profile-feature that references skill used by this profile-class.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'removeSkillIdFromFeatures': {'name': 'removeSkillIdFromFeatures', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME
            profileId: (string): Id of existing profile

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'profileId': {'name': 'profileId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile-class

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileClass/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
