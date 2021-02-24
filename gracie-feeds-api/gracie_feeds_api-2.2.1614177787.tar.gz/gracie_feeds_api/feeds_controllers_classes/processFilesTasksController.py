from gracie_feeds_api import GracieBaseAPI


class processFilesTasksController(GracieBaseAPI):
    """Process Files Tasks Controller"""

    _controller_name = "processFilesTasksController"

    def submit(self, file, privacyMode, projectId, **kwargs):
        """Process the text from file. Supported file formats:  - https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            file: (file): file
            filterFields: (string): CSV of fields to show, default shows all. See https://github.com/bohnman/squiggly for usage
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            minRelevancy: (number): minRelevancy
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            stopAfterChunkNum: (integer): Only process the first N number of text chunks when the document requires chunking.

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'minRelevancy': {'name': 'minRelevancy', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/process-file-tasks/submit'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
