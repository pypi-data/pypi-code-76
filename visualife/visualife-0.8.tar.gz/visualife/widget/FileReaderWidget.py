import json
from browser import html, window, ajax, document


class ProcessData:
    """Interface for classes that are used by FileReaderWidget to process files that are loaded"""

    def __call__(self, *args, **kwargs):
        """abstract method that will be called for every piece of data obtained by a receiver"""
        pass


class AjaxCommunication(ProcessData):
    """Class that sends data with AJAX
    """

    def __init__(self, url, on_complete=None, req_type="POST"):
        """Constructor creates a sender object

        :param url: where the data is to be sent
        :param on_complete: callback method called when transfer is completed
            if None, a default callback will be used that just prints a log message on the console
        :param req_type: request type: "POST" or "GET"
        """
        self.__req_type = req_type
        self.__on_complete = on_complete if on_complete else AjaxCommunication.__default_on_complete
        self.__url = url

    def on_complete(self,on_complete_func):
        """Sets new callback function that will be called when server returns from AJAX call

        :param on_complete_func: a function name
        :return: None
        """
        self.__on_complete = on_complete_func

    def __call__(self, *args, **kwargs):
        """Sends the given data with AJAX

        :param args: data to be sent:
            - if ``args`` contain a single element which is a Python dictionary: the dictionary is sent 'as it is'
            - if ``args`` contain a single element: it will be stored in a JSON dictionary under 'data' key
            - if ``args`` contain more than one element: all elements will be stored in a JSON dictionary  under 'data' key
        :param kwargs: see below
        :return: None

        :Keyword Arguments:
            * *key* (``string``) --
              key string will be added to JSON dictionary sent by this method
            * *file_name* (``string``) --
              file_name will be added to JSON dictionary sent by this method
            * *response_type* (``string``) -- only one of the following: *arraybuffer*, *blob*, *document*, *json*
                or *text*; default is *text*
        """
        req = ajax.ajax()
        if self.__on_complete: req.bind('complete', self.__on_complete)
        req.open(self.__req_type, self.__url, True)
        if 'response_type' in kwargs:
            req.responseType = kwargs['response_type']
            print(req.responseType)
        if self.__req_type == "POST":
            content = "application/x-www-form-urlencoded;charset=UTF-8"
            req.set_header('content-type', content)

        if len(args) == 1: # --- if there is only one argument
            if isinstance(args[0],dict): # --- if its already a dictionary, send 'as it is'
                req.send(args[0])
            else:
                to_send = {'data': args[0]}
                if "file_name" in kwargs: to_send["file_name"] = kwargs["file_name"]
                if "key" in kwargs: to_send["key"] = kwargs["key"]
                req.send(to_send)
        else:
            to_send = {'data': args}
            if "file_name" in kwargs: to_send["file_name"] = kwargs["file_name"]
            if "key" in kwargs: to_send["key"] = kwargs["key"]
            req.send(to_send)

    @staticmethod
    def __default_on_complete(evt):
        try:
            print(json.loads(evt.text))
        except:
            print(evt.text)


class DataStorageMap(ProcessData):
    """Class that stores content in a Python dictionary
    """

    def __init__(self):
        """Bare constructor"""
        self.__files = {}

    def __call__(self, *args, **kwargs):
        """stores content in a Python dictionary

        :param args: data to be stored
        :param kwargs: see below

        :Keyword Arguments:
            * *key* (``string``) --
              key used to store the data in this directory, e.g. the name of the file the data come from
        """
        self.__files[kwargs["key"]] = args[0]
        print(kwargs["key"], "stored")


class FileReaderWidget:
    """Reads a file that has been dropped in a browser window

    """
    def __init__(self, drop_zone_id, extensions=[], hint_message="Drop a file"):
        self.__drop_zone = drop_zone_id
        self.__actions = []
        self.__names = []
        self.__hint_message = hint_message
        self.__extensions = extensions
        self.__text_area = """
        <p class="p-2 m-3" id="%s_text" style="display:block;"></p>
        """ % drop_zone_id
        document[self.__drop_zone].innerHTML += self.__text_area
        document[drop_zone_id + "_text"].text = hint_message
        document[self.__drop_zone].bind('dragover', self.__handle_file_dragged_over)
        document[self.__drop_zone].bind('drop', self.__handle_file_dropped)

    def add_action(self, action):
        """Adds a function to an actions list
        """
        self.__actions.append(action)

    @property
    def actions(self): 
        """List of functions which will be run after reading a file

        This function takes whole file text as an argument. File name can be accesed 
        inside this function by kwargs["key"]
        """
        return self.__actions

    @actions.setter
    def actions(self, actions):
        self.__actions = actions

    @property
    def hint_message(self): 
        """Message that is displayed in the drop_zone
        """
        return self.__hint_message

    @hint_message.setter
    def hint_message(self, new_hint):
        self.__hint_message = new_hint
        document[self.__drop_zone + "_text"].text = new_hint

    @property
    def extensions(self): 
        """Extensions allowed for a FileReader to read
        """
        return self.__extensions

    @extensions.setter
    def extensions(self, new_extensions_list):
        self.__extensions = new_extensions_list


    def __handle_file_dragged_over(self, evt):
        """Sets dropEffect to dataTransfer of drop event
        """
        evt.stopPropagation()
        evt.preventDefault()
        evt.dataTransfer.dropEffect = 'copy'

    def __handle_file_dropped(self, evt):
        """Reads files and runs functions from actions list
        """

        def setup_reader(f):

            def load_file(evt):
                text = evt.target.result
                for actn in self.__actions: actn(text, key=f.name)

            if f.name.split(".")[-1] in self.__extensions or len(self.__extensions) == 0:
                self.__names.append(f.name)
                reader = window.FileReader.new()
                reader.onload = load_file
                reader.readAsText(f)

        evt.stopPropagation()
        evt.preventDefault()
        files = evt.dataTransfer.files  # FileList object.
        for f in files:
            print("processing", f.name)
            setup_reader(f)



