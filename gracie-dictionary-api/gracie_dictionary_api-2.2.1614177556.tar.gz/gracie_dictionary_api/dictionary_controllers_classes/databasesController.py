from gracie_dictionary_api import GracieBaseAPI


class databasesController(GracieBaseAPI):
    """Databases Controller"""

    _controller_name = "databasesController"

    def archive(self, **kwargs):
        """

        Args:
            classifierId: (string): Id of existing class (classifierId)
            languageId: (string): Id of class language to backup

        Consumes:
            application/json

        Returns:
            application/json
        """

        all_api_parameters = {'classifierId': {'name': 'classifierId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/archive'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def backup(self, **kwargs):
        """

        Args:
            incremental: (boolean): true - incremental backup to the default backup folder "incremental". false - full backup to the new folder with name "<timestamp>".
            removeFolder: (boolean): true - if backup folder was zipped then remove it not to lose disk space. false - don't remove backup folder.
            zip: (boolean): true - pack backup folder to zip file. false - skip packing.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'incremental': {'name': 'incremental', 'required': False, 'in': 'query'}, 'removeFolder': {'name': 'removeFolder', 'required': False, 'in': 'query'}, 'zip': {'name': 'zip', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/backup'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportDatabases(self, **kwargs):
        """

        Args:
            databaseId: (string): Id is some of { country, topic, skillSet, skill, clusterSet, clusterGroup, cluster, profile }. Or some of { "COUNTRIES", "TOPICS", "SKILLSETS", "CLUSTERSETS", "PROFILES" }. If empty then export all databases.
            password: (string): Protect the zip archive with a password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'databaseId': {'name': 'databaseId', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/exportDatabases'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def importDatabases(self, **kwargs):
        """

        Args:
            conflictsResolving: (string): Method to resolve import conflicts: STOP, OVERWRITE, SKIP
            databaseId: (string): Id is some of { country, topic, skillSet, skill, clusterSet, clusterGroup, cluster, profile }. Or some of { "COUNTRIES", "TOPICS", "SKILLSETS", "CLUSTERSETS", "PROFILES" }. If empty then import all databases.
            file: (file): Name of file of the zip archive database import
            password: (string): Password used when creating the zip archive
            recalculateDocumentsVectors: (boolean): recalculateDocumentsVectors

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'query'}, 'databaseId': {'name': 'databaseId', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': False, 'in': 'formData'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/importDatabases'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateBinaries(self, **kwargs):
        """

        Args:
            forceUpdateUnchanged: (boolean): Force biniaries to update on all clients

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'forceUpdateUnchanged': {'name': 'forceUpdateUnchanged', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateBinaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateDictionaries(self, **kwargs):
        """

        Args:
            id: (string): Id of dictionary to update
            recalculateDocumentsVectors: (boolean): Enables recalculating document vectors for all dictionary documents. Time-consuming.
            testSubclasses: (boolean): Enables document-quality evaluation run that is performed after the dictionary is updated.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}, 'testSubclasses': {'name': 'testSubclasses', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateDictionaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateLanguage(self, **kwargs):
        """

        Args:
            customCorpusFileName: (string): Specify custom file name for language corpus. The file name is relative to `data_sources` dir
            languageId: (string): Language id of the models to update
            updateDoc2vec: (boolean): Enables doc2vec model update for language
            updateIdfModel: (boolean): Enables IDF model update for the language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'customCorpusFileName': {'name': 'customCorpusFileName', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'updateDoc2vec': {'name': 'updateDoc2vec', 'required': False, 'in': 'query'}, 'updateIdfModel': {'name': 'updateIdfModel', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateLanguage'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateProfiles(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile
            updateDocuments: (boolean): Enables reprocessing profile documents to find updated feature vectors. Time-consuming.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'updateDocuments': {'name': 'updateDocuments', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateProfiles'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateSkillsets(self, **kwargs):
        """

        Args:
            enabledContextSensitiveKeywords: (boolean): Enables context-sensitive keywords for the skill. Keywords for the skill get doc2vec vectors, which allows for a disambiguation on per-keyword level. Has noticeable performance toll on entire system.
            recalculateDocumentsVectors: (boolean): Enables recalculating document vectors for all skill documents. Relatively time-consuming.
            skillId: (string): Id of skill to update
            testSubclasses: (boolean): Enables document-quality evaluation run that is performed after the skill is updated.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabledContextSensitiveKeywords': {'name': 'enabledContextSensitiveKeywords', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': False, 'in': 'query'}, 'testSubclasses': {'name': 'testSubclasses', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateSkillsets'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
