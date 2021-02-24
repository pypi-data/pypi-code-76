# Fenix Library
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/fenix/libraries

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# IMPORTS
from __future__ import annotations
from abc import ABC
import json
import pathlib
import textwrap
from typing import Any, Dict, List, Optional, Union # For specifying particular type hints

class AbstractJSON(ABC):
    """
    Contains basic methods to read and write JSON `dict`s for a single file.

    An instance of this class will point to a single JSON file. All read and write operations will happen with respect to that file. This means that once you point the instance to the JSON filepath, you won't need to send the filepath every time you do read/write operations. 
    WARNING: This class is not meant to create objects directly. Other classes can derive from it and you can create objects from them.

    Properties
    ----------
    filepath: str
        Either relative or absolute path to the JSON file (with forward slashes)
    data: dict
        The Python `dict` form of the data that is supposed to be in the JSON file

    Attributes
    ----------
    _filepath_Path_object: pathlib.Path
        Either relative or absolute path to the JSON file (with forward slashes)
    _data: dict
        The Python `dict` form of the data that is supposed to be in the JSON file
    _differs_from_file: bool
        A switch that remembers whether the data has been modified after the last load from a file or last write to a file

    """

    # CONSTRUCTOR

    def __init__(self, filepath: str, data: Optional[dict] = None) -> None:
        """
        Initializes an 'AbstractJSON' object.

        An attempt is made to load data from the specified filepath. If no such file exists, an error is raised.

        Parameters
        ----------
        filepath: str
            Either relative or absolute path to a JSON file (with forward slashes)
        data: Optional[dict], default None
            The dict data that is to be stored in a JSON file 

        Returns
        -------
        Nothing
        """

        self.filepath = filepath 
        if data is None: # If data is not provided
            self.load_data() # Try to load data from the file
        else:
            self.data = data
        self._differs_from_file: bool = False
           
    # DESTRUCTOR

    def __del__(self) -> None:
        """
        Called when an instance of this class is out of scope and/or being deleted.

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        if self._differs_from_file:
            self.write_data()

    # OVERLOADED OPERATORS

    # Usage example: `some_string = str(settings_object)`
    def __str__(self) -> str:
        """
        Returns the string representation of the current instance

        Returns
        -------
        str
            The string representation of the JSON data
        """

        return str(self.data)

    # Usage examples: 
    # `settings_object3 = settings_object1 + settings_object2`
    # `settings_object5 = settings_object4 + some_dict`
    def __add__(self, other: Union[Dict, AbstractJSON]) -> AbstractJSON:
        """
        Returns the combination of data when two instances are added with a `+` operator
        Usage examples: 
        `settings_object3 = settings_object1 + settings_object2`
        `settings_object5 = settings_object4 + some_dict`

        Parameters:
        -----------
        other: Union[Dict, AbstractJSON]
            The other operand

        Returns
        -------
        AbstractJSON
            The AbstractJSON instance with merged data
        """
       
        if type(other) is AbstractJSON:
            return type(self)(self.filepath, self.data.update(other.data))
        elif type(other) is dict:
            return type(self)(self.filepath, self.data.update(other))
        else:
            raise TypeError("Wrong operand type for addition.")

    # Usage example: `settings_object2 = some_dict + settings_object1`
    def __radd__(self, other: Dict) -> AbstractJSON:
        """
        Returns the combination of data when two instances are added with a `+` operator
        Usage example: `settings_object2 = some_dict + settings_object1`

        Parameters:
        -----------
        other: Union[Dict, AbstractJSON]
            The other operand

        Returns
        -------
        AbstractJSON
            The AbstractJSON instance with merged data
        """
       
        if type(other) is dict:
            return type(self)(self.filepath, self.data.update(other))
        else:
            raise TypeError("Wrong operand type for addition.")

    # Usage example: `value = settings_object["key"]`
    def __getitem__(self, key_name: str) -> Any:
        """
        Overloads the [] operator and functions like `dict` indexing
        Usage Example: `value = settings_object["key"]`

        Parameters
        ----------
        key_name: str
            Name of the key whose value is to be retrieved

        Returns
        -------
        value: Any
            Value associated with the key 'key_name'
        """

        return self.get_item(key_name)

    # Usage example: `settings_object["key"] = value`
    def __setitem__(self, key_name: str, value: Any) -> None:
        """
        Overloads the [] operator and functions like `dict` indexing
        Usage Example: `settings_object["key"] = value`
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        key_name: str
            Name of the key whose value is to be set
        value: Any
            The value to be set

        Returns
        -------
        Nothing
        """

        return self.set_item(key_name, value)

    # Usage example: `del settings_object["key"]`
    def __delitem__(self, key_name: str) -> None:
        """
        Overloads the [] operator and functions like `dict` indexing
        Usage example: `del settings_object["key"]

        Parameters
        ----------
        key_name: str
            Name of the key which is to be deleted

        Returns
        -------
        Nothing
        """

        self.delete_item(key_name)

    # REGULAR METHODS

    def load_data(self) -> None:
        """
        Loads data from the JSON configuration file
       
        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        self.data = AbstractJSON._read_from_file(self.filepath) # Store the `dict` data
        self._differs_from_file = False # Data was newly loaded, so same as the file

    def write_data(self) -> None:
        """
        Writes the data to the JSON configuration file. 
        
        You can generally call this after you are done modifying the data using the 'get' and 'set' methods available to you (which itself can be done after loading the current JSON data using the 'load_data' method).
        You could also call this method if you have your own Python `dict` and you have loaded it by using 'set_data'.

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        AbstractJSON._write_to_file(self.data, self.filepath) # Write the contents of the `dict` data to the JSON file
        self._differs_from_file = False # Data was newly written, so same as the file

    def get_item(self, key_name: str) -> Any:
        """
        Returns the value associated with the key 'key_name'

        Parameters
        ----------
        key_name: str
            Name of the key whose value is to be retrieved

        Returns
        -------
        value: Any
            Value associated with the key 'key_name'
        """

        return self.data[key_name] # Retrieve the value from the key

    def set_item(self, key_name: str, value: Any) -> None:         
        """
        Sets the value associated with the key 'key_name'
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        key_name: str
            Name of the key whose value is to be set
        value: Any
            The value to be set       

        Returns
        -------
        Nothing
        """

        self.data[key_name] = value # Sets the value for the key
        self._differs_from_file = True

    def delete_item(self, key_name: str) -> None:
        """
        Deletes the item specified by the key_name

        Parameters
        ----------
        key_name: str
            Name of the key which is to be deleted

        Returns
        -------
        Nothing
        """

        del self.data[key_name]

    # VALIDATION METHODS

    def _assert_path_is_valid(self) -> None:
        """
        Checks whether '_filepath_Path_object' is a valid file path.
        If not, an error is raised.

        Parameters
        ----------
        None

        Raises
        ------
        UnboundLocalError
            _filepath_Path_object was not assigned
        FileNotFoundError
            _filepath_Path_object is not a valid file
                   
        Returns
        -------
        None
        """

        if self._filepath_Path_object is None:
            raise TypeError("_filepath_Path_object has not been assigned yet. Have you specified a filepath for the JSON file?")
        elif (not self._filepath_Path_object.exists()) or (not self._filepath_Path_object.is_file()):
            raise FileNotFoundError("File not found at given path: ", str(self._filepath_Path_object))

    def _assert_data_is_valid(self) -> None:
        """
        Checks whether _data is a non-null dict.
        If not, an error is raised.

        Parameters
        ----------
        None

        Raises
        ------
        TypeError
            _data was either not assigned or is not of `dict` type
                   
        Returns
        -------
        None
        """

        if self._data is None:
            raise TypeError("_data has not been assigned yet. Have you either loaded data from a file using the method 'load_data' or if you have your own `dict`, set it using the method 'set_data'?")
        elif not isinstance(self._data, dict):
            raise TypeError("_data is not a `dict`, but of type: ", type(self._data), ". Please either call the 'set_data' method using a valid `dict` or verify the format of the JSON file specified.")

    # STATIC METHODS

    @staticmethod
    def _read_from_file(filepath: str) -> dict:
        """
        Retrieves data from a JSON file at 'filepath' as a `dict`.
        WARNING: This method is for internal use. Please use `load_data` instead.

        Parameters
        ----------
        filepath: str
            Path to the JSON configuration file which has the data

        Returns
        -------
        data: dict
            Data contained within the JSON file at 'filepath' as a 'dict'
        """

        with open(filepath, 'r') as configuration_file: # Open the JSON file in 'read' mode
            data = json.load(configuration_file)

        return data

    @staticmethod
    def _write_to_file(data: dict, filepath: str) -> None:
        """
        Writes the dict 'data' to a JSON file at 'filepath'.
        WARNING: This method is for internal use. Please use `write_data` instead.

        Parameters
        ----------
        data: dict
            The dict data to be written to a JSON file.
        filepath: str
            Path to the JSON configuration file to write data to

        Returns
        -------
        Nothing
        """

        with open(filepath, 'w') as configuration_file: # Open the JSON file in 'write' mode
            json.dump(data, configuration_file, indent=4)

    # GETTERS AND SETTERS

    @property
    def filepath(self) -> str:
        """
        Retrieve the filepath in the JSON configuration file

        Parameters
        ----------
        None
                   
        Returns
        -------
        filepath: str
           Path to the JSON configuration file in _filepath_Path_object
        """

        return str(self._filepath_Path_object) # Retrieve the path string from the pathlib.Path object

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        """
        Sets the JSON configuration filepath to read or write data from

        Parameters
        ----------
        filepath: str
            Path to the JSON configuration file whose data is to be read or written
            
        Returns
        -------
        Nothing
        """

        self._filepath_Path_object = pathlib.Path(filepath)
        self._assert_path_is_valid()

    @property
    def data(self) -> dict:
        """
        Retrieve the configuration data as a Python `dict`. 

        Parameters
        ----------
        None
                   
        Returns
        -------
        data: dict
            Configuration data stored internally as a dict in '_data'. 
        """

        return self._data

    @data.setter
    def data(self, data: dict) -> None:
        """
        Sets the data to a given `dict` value        
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        data: dict
            Given `dict` to replace the data stored internally at self._data. 
            WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.
            
        Returns
        -------
        Nothing
        """

        self._data = data
        self._assert_data_is_valid()

class JSONConfiguration(AbstractJSON):
    """
    Contains basic methods to read and write JSON `dict`s for a single file, most of which are implicitly inherited from the parent class 'AbstractJSON'.

    An instance of this class will point to a single JSON file. All read and write operations will happen with respect to that file. This means that once you point the instance to the JSON filepath, you won't need to send the filepath every time you do read/write operations. 
      
    OPTIONAL: In addition to the above basic JSON read and write methods, this class can manage settings that permit choosing from a list. We can refer to this standard form as 'FENIX_CONFIG_CHOICE_FORMAT` whose JSON example is as below
    An entry in the 'FENIX_CONFIG_CHOICE_FORMAT` is at top level (if nested) and strictly looks like 'ui-toolkits' below:
    "ui-toolkits": {
        "available": [
            "gtk",
            "qt",
            "qtquick"
        ],
        "default": "gtk",
        "current": "qt"
    }

    """

    # CONSTRUCTOR

    def __init__(self, filepath: str, data: Optional[dict] = None) -> None:
        """
        Initializes a 'JSONConfiguration' object.

        An attempt is made to load data from the specified filepath. If no such file exists, an error is raised.

        Parameters
        ----------
        filepath: str
            Either relative or absolute path to a JSON file (with forward slashes)
        data: Optional[dict], default None
            The dict data that is to be stored in a JSON file 

        Returns
        -------
        Nothing
        """

        super().__init__(filepath, data) # Call the constructor from the parent class

    # REGULAR METHODS

    def get_available_choices_for_item(self, entry_name: str) -> List[Any]: 
        """
        Returns the list of available "choices" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).

        Parameters
        ----------
        entry_name: str
            The name of the entry that is to be retrieved

        Returns
        -------
        listOfChoices: List[Any]
            The list of choices for the given "selectable" setting in the 'FENIX_CONFIG_CHOICE_FORMAT`
        """

        self._assert_entry_is_selectable(entry_name) # Check if the entry is in the 'FENIX_CONFIG_CHOICE_FORMAT`
        return self.data[entry_name]["available"] # Retrieve the available choices for the entry

    def get_default_choice_for_item(self, entry_name: str) -> Any:
        """
        Returns the default "choice" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).

        Parameters
        ----------
        entry_name: str
            The name of the entry that is to be retrieved

        Returns
        -------
        default_choice: Any
            The default choice for the given "selectable" setting in the 'FENIX_CONFIG_CHOICE_FORMAT`
        """

        self._assert_entry_is_selectable(entry_name) # Check if the entry is in the 'FENIX_CONFIG_CHOICE_FORMAT`
        return self.data[entry_name]["default"] # Retrieve the default choice for the entry

    def get_current_choice_for_item(self, entry_name: str) -> Any:
        """
        Returns the current "choice" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).

        Parameters
        ----------
        entry_name: str
            The name of the entry that is to be retrieved

        Returns
        -------
        current_choice: Any
            The current choice for the given "selectable" setting in the 'FENIX_CONFIG_CHOICE_FORMAT`
        """

        self._assert_entry_is_selectable(entry_name) # Check if the entry is in the 'FENIX_CONFIG_CHOICE_FORMAT`
        return self.data[entry_name]["current"] # Retrieve the current choice for the entry

    def set_available_choices_for_item(self, entry_name: str, available_choices: List[Any]) -> None:         
        """
        Sets the list of available "choices" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        entry_name: str
            The name of the entry that is to be modified
        available_choices: List[Any]
            The list of choices for the given "selectable" setting in the 'FENIX_CONFIG_CHOICE_FORMAT`

        Returns
        -------
        Nothing
        """

        self._assert_data_is_valid() # Validate the data
        self.data[entry_name]["available"] = available_choices # Set the available choices for the entry 'entry_name'

    def set_default_choice_for_item(self, entry_name:str, default_choice: Any) -> None:         
        """
        Sets the default "choice" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        entry_name:str
            The name of the entry that is to be modified
        default_choice: Any
            The default choice for the given selectable setting in the 'FENIX_CONFIG_CHOICE_FORMAT`

        Returns
        -------
        Nothing
        """

        self._assert_data_is_valid() # Validate the data
        self.data[entry_name]["default"] = default_choice # Set the default choice for the entry 'entry_name'

    def set_current_choice_for_item(self, entry_name: str, current_choice: Any) -> None:        
        """
        Sets the current "choice" for the "selectable" setting denoted by "entry_name" in the 'FENIX_CONFIG_CHOICE_FORMAT` (refer to the class documentation above for details on this format).
        WARNING: No actual data would be written to the file until either (1) the method 'write_data()' is called or (2) the current `JSONConfiguration` or `AbstractJSON` instance goes out of scope and/or is deleted.

        Parameters
        ----------
        entry_name: str
            The name of the entry that is to be checked
        current_choice: Any
            The current choice for the given selectable setting in the 'FENIX_CONFIG_CHOICE_FORMAT`

        Returns
        -------
        Nothing
        """

        self._assert_data_is_valid() # Validate the data        
        self.data[entry_name]["current"] = current_choice  # Set the current choice for the entry 'entry_name'

    # VALIDATION METHODS

    def _assert_entry_is_selectable(self, entry_name: str) -> None:
        """
        Tells whether the given entry is in the 'FENIX_CONFIG_CHOICE_FORMAT`. 

        An entry in the 'FENIX_CONFIG_CHOICE_FORMAT` is at top level (if nested) and strictly looks like 'modes' below:        
        "modes": {
            "available": [
                "silent_minimal",
                "silent_basic",
                "silent_full",
                "minimal",
                "basic",
                "full",
                "semi_automatic",
                "customized"
            ],
            "default": "semi_automatic",
            "current": "full"
        }

        Parameters
        ----------
        entry_name: str
            Name of the entry to be checked

        Raises
        -------
        TypeError
            Entry not in the above-defined "selectable" 'FENIX_CONFIG_CHOICE_FORMAT` format
        KeyError
            Entry not found, or is not one of the keys in the dict data

        Returns
        -------
        Nothing
        """

        error_message = \
        """
        The provided entry_name is not a valid "selectable" setting in the 'FENIX_CONFIG_CHOICE_FORMAT` format.
        An entry in the 'FENIX_CONFIG_CHOICE_FORMAT` is at top level (if nested) and strictly looks like the following:
        "modes": {
            "available": [
                "silent_minimal",
                "silent_basic",
                "silent_full",
                "minimal",
                "basic",
                "full",
                "semi_automatic",
                "customized"
            ],
            "default": "semi_automatic",
            "current": "customize"
        }
        """

        error_message = textwrap.dedent(error_message)
        if entry_name in self.data:
            if (
                ("available" not in self.data[entry_name])
                or (not isinstance(self.data[entry_name]["available"], list))
                or ("default" not in self.data[entry_name])
                or ("current" not in self.data[entry_name])
            ):
                raise TypeError(error_message)
            else:
                return
        else:
            raise KeyError("The provided entry_name '", entry_name, "' is not found as a key in the data.")
