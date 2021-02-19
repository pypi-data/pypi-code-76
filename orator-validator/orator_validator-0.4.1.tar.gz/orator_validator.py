import re
import time
import json

class Validator(object):
    _validation_init = True
    __errors__ = {'code':200, 'errors':[]}

    def process(self, key, exist=False, not_exist=False, **args):
        '''
        This function is created to add new functionality, if a model value of a
        nullable filled exist

        param: str key: This is the name of the value that we are looking
        param: exist: this boolean is dedicated to execute a flag if the key exist
        param: not_exist: this boolean is dedicated to execute a flag if the key doesnt exist
        '''
        value = getattr(self, key, None)
        if exist and value:
            exist(self, **args)
        if not_exist and not value:
            not_exist(self, **args)

    def validate(self, key, require=False, data_type=False,
            regex=False, custom_error=False, date_str=False, **args):
        '''
        Function dedicated to validate if a imput has some values

        param: str key: This is the name of the value that we are looking, is just for us to make the error json
        param: bool require: This tell us if we need to abort if the input is undefined
        param: str data_type: Data type tell us if the input has to be a certain data type so we verified
        param: str regex: String that we could check if we need
        param: function custom_error: you can send a function to build a custom error
        param: date_str: This is a string with the format to check the datetime string
        param: *args *args: arguments to go with the function
        return: data response: We can return the value validated or None if the value doest correspont to the statements
        '''
        if self._validation_init:
            self.errors(validation_init = False)
        value = getattr(self, key, None)
        if require and not value:
            self._handle_error('require', key, custom_error=custom_error, **args)
            return self
        if data_type and not isinstance(value, data_type):
            self._handle_error('data type', key, custom_msg='Bad data type on {}'.format(key),
                custom_error=custom_error, **args)
            return self
        if regex:
            if not value: self._handle_error('require', key, custom_error=custom_error, **args)
            elif not re.match(regex, value):
                self._handle_error('regex', key, custom_error=custom_error, **args)
        if date_str:
            try:
                time.strptime(value, date_str)
            except Exception as e:
                self._handle_error('invalid', key, custom_msg='Invalid time value')
        return self

    def validate_update(self, key, guarded=False, data_type=False,
            regex=False, custom_error=False, date_str=False,
            function_callback=False, **args):
        '''
        Funtion dedicated to validate on update that values on updated are the
        ones on the list for you to use this function the update has to be on the
        model side not on the builder

        param: str key: This is the name of the value that we are looking, is just for us to make the error json
        param: bool guarded: This tell us if we need to abort if the input is on the dictionary
        param: str data_type: Data type tell us if the input has to be a certain data type so we verified
        param: str regex: String that we could check if we need
        param: function custom_error: you can send a function to build a custom error
        param: date_str: This is a string with the format to check the datetime string
        param: *args *args: arguments to go with the function
        return: data response: We can return the value validated or None if the value doest correspont to the statements
        '''
        if self._validation_init:
            self.errors(validation_init = False)
        value = self.get_dirty().get(key, None)
        if guarded and value:
            self._handle_error('Cant update', key, custom_error=custom_error, **args)
            return self
        elif value:
            if data_type and not isinstance(value, data_type):
                self._handle_error('data type', key, custom_msg='Bad data type on {}'.format(key),
                    custom_error=custom_error, **args)
                return self
            if regex and not re.match(regex, value):
                if not require: self.validate(key, require=True)
                self._handle_error('regex', key, custom_error=custom_error, **args)
            if date_str:
                try:
                    time.strptime(value, date_str)
                except Exception as e:
                    self._handle_error(
                        'invalid', key, custom_msg='Invalid time value')
            if function_callback:
                try:
                    function_callback(**args)
                except Exception as e:
                    self._handle_error(
                        'Callback error', key, custom_msg=str(e))
        return self

    @classmethod
    def _handle_error(cls, type_error, value_name,
            custom_msg=False, custom_error=False, **args):
        '''
        Funtion dedicated to handle errors on the validation

        param: str type_error: this is use for the default msg
        param: str value_name: this is use for the default msg
        param: str custom_msg: is they want to use a custom_msg
        param: function custom_error: Optional to send a custom error
        param: args **args: Values of the custom error
        return: None
        '''
        if custom_error:
            custom_error(**args)
        cls.add_error(code=400, msg=custom_msg
                if custom_msg else
                'Error of {} on {}'.format(type_error, value_name)
        )

    @classmethod
    def errors(cls, validation_init=True):
        '''
        Function dedicated to delete errors after use

        param: validation_init
        ptype: volean
        return: __errors__
        rtype: dict
        '''
        cls._validation_init = validation_init
        errors = cls.__errors__
        cls.__errors__ = {'code':200, 'errors':[]}
        if errors['code'] != 200:
            raise ValidatorError(errors['code'], json.dumps(errors['errors']))

    @classmethod
    def add_error(cls, code=None, msg=None):
        '''
        Function dedicated to modify errors

        param: int code: The error code that we will return
        param: str msg: the msg to append to error list
        '''
        if code:
            cls.__errors__['code'] = code
        if msg:
            cls.__errors__['errors'].append({
                'msg': msg
            })

class Error(Exception):
    """Base class for other exceptions"""
    pass

class ValidatorError(Error):
    """Raised when the validator find and error"""

    def __init__(self, status_code=None, body=None):
        self.status_code = status_code
        self.body = body
