from gracie_feeds_api import GracieBaseAPI


class processTextsTasksController(GracieBaseAPI):
    """Process Texts Tasks Controller"""

    _controller_name = "processTextsTasksController"

    def submit(self, privacyMode, projectId, text, **kwargs):
        """

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            fileExt: (string): fileExt
            fileName: (string): fileName
            filterFields: (string): CSV of fields to show, default shows all. See https://github.com/bohnman/squiggly for usage
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            mimeType: (string): mimeType
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            stopAfterChunkNum: (integer): Only process the first N number text chunk when the document requires chunking.
            text: (type): text

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'fileExt': {'name': 'fileExt', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}}
        parameters_names_map = {}
        api = '/process-text-tasks/submit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
