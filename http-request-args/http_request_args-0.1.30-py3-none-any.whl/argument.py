import re
from copy import deepcopy
from abc import ABCMeta, abstractmethod
from .utilities import FunctionArgsAssertion
import os
from datetime import datetime, timedelta
from flask import request
import inspect


class ArgumentTypeValidator:
    is_float = lambda req_type, arg_val_type: req_type is float and arg_val_type in [int, float]

    """ To check the argument type """

    @staticmethod
    def has_type(arg_val, req_type):
        arg_val_type = type(arg_val)
        FunctionArgsAssertion.assert_type(req_type)
        return True if (arg_val_type is req_type) or ArgumentTypeValidator.is_float(req_type, arg_val_type) \
            else False


class IterableArgumentValidator:
    """ This class has some useful function for Iterable arguments """

    @staticmethod
    def in_collection(arg_val, req_collection):
        """ Check if an element is inside a collection """
        FunctionArgsAssertion.assert_iterable(req_collection)
        return True if arg_val in req_collection else False

    @staticmethod
    def in_collection_for_list_argument(arg_val, req_collection):
        """ Check if an element is inside a collection """
        FunctionArgsAssertion.assert_iterable(req_collection)
        arg_status = [True for arg in arg_val if arg in req_collection]

        return True if False not in arg_status else False

    @staticmethod
    def has_length(arg_val, req_length_range):
        """ Make sure the collection length is within the selected range """
        FunctionArgsAssertion.assert_iterable(arg_val)
        FunctionArgsAssertion.assert_range(req_length_range)

        if req_length_range[0] < 0 or req_length_range[1] < 0:
            raise Exception('Both numbers in the req_range should be positive')

        col_len = len(arg_val)
        return True if col_len >= req_length_range[0] and col_len <= req_length_range[1] else False


class Argument(metaclass=ABCMeta):
    """ An abstract class to represent the argument """

    def __init__(self, name, required, arg_type):
        self.name = name
        self.required = required
        self.arg_type = arg_type
        self.functions_list_arg = None
        self.invalid = False
        self.validation_report = {self.name: ''}
        self.help_report = {self.name: ''}
        self.length_range_arg = None
        self.req_options_arg = None

    @property
    def functions_list(self):
        try:
            return self.functions_list_arg()
        except:
            return self.functions_list_arg

    @property
    def length_range(self):
        try:
            return self.length_range_arg()
        except:
            return self.length_range_arg

    @property
    def req_options(self):
        try:
            return self.req_options_arg()
        except:
            return self.req_options_arg

    def update_name(self, name):
        self.validation_report[name] = self.validation_report[self.name]
        self.validation_report.pop(self.name)
        self.name = name

    def set_invalid_arg(self):
        self.invalid = True

    def update_validation_report(self, new_info):
        self.set_invalid_arg()
        self.validation_report[self.name] += f'{new_info}\n'

    @abstractmethod
    def assert_arg(self, args_dict):
        """ Compulsory check of existence and the data type """
        self.reset_arg()
        if not self.assert_existence(args_dict):
            return

        arg_val = args_dict[self.name]

        if not self.assert_type(arg_val):
            return

        return args_dict[self.name]  # The argument value

    def reset_arg(self):
        self.invalid = False
        self.validation_report = {self.name: ''}
        self.help_report = {self.name: ''}

    def assert_existence(self, args_dict):
        """ Check if the argument is available or not """
        arg_available = IterableArgumentValidator.in_collection(self.name, args_dict)

        if self.required and \
                (not arg_available or (
                        arg_available and type(args_dict[self.name]) is list and len(args_dict[self.name]) == 0)):
            self.update_validation_report('missing')

        return arg_available

    def assert_type(self, arg_val):
        """ Check the argument type """
        type_status = ArgumentTypeValidator.has_type(arg_val, self.arg_type)
        type_status = type_status or (not self.required and arg_val is None)

        if not type_status:
            current_type = type(arg_val)
            self.update_validation_report('data type is {} but it should be {}'.format(
                current_type.__name__, self.arg_type.__name__))

        return type_status

    def assert_req_options(self, arg_val):
        """ Check if the argument value belongs to the required options """
        if type(self) not in [NumberArgument, StringArgument, ListArgument]:
            raise Exception('Valid only for NumberArgument, StringArgument, and ListArgument types')

        if type(self) in [ListArgument]:
            if self.req_options and not IterableArgumentValidator.in_collection_for_list_argument(arg_val,
                                                                                                  self.req_options):
                self.update_validation_report(
                    'should be one of the following options {} but the passed value is {}'.format(
                        self.req_options, arg_val))

        if self.req_options and not IterableArgumentValidator.in_collection(arg_val, self.req_options):
            self.update_validation_report('should be one of the following options {} but the passed value is {}'.format(
                self.req_options, arg_val))
            return False
        return True

    def assert_length(self, arg_val):
        """ Check if the argument length is within the allowed range """
        if type(self) not in [ListArgument, StringArgument]:
            raise Exception('Valid only for ListArgument and StringArgument types')

        if self.length_range and not NumberArgument.in_range(len(arg_val), self.length_range):
            self.update_validation_report('length should be in the range {} but the current length is {}'.format(
                self.length_range, len(arg_val)))
            return False
        return True

    def assert_functions_list(self, arg_val):
        """ Useful to check other functions that are not implemented in this class """
        if not self.functions_list:
            return

        for func in self.functions_list:
            if not func(arg_val):
                self.update_validation_report('should satisfy {} function but the passed value is {}'.format(
                    func.__name__, arg_val))

    def arg_help(self):
        self.reset_arg()
        help_report_template = {
            'arg_type': 'This argument should be {} \n',
            'req_options': 'This argument should be one of the following options {} \n',
            'length_range': 'This argument length should be in the range {} \n',
            'functions_list': 'This argument should satisfy {} functions \n'}

        if self.required:
            msg = 'This argument is required \n'

        else:
            msg = 'This argument is optional \n'

        # Iterate over all class attributes
        for attr in help_report_template:
            attr_value = eval(f'self.{attr}')
            # If attribute has value (not None)
            if attr_value:
                if attr == 'arg_type':
                    attr_value = attr_value.__name__

                if attr == 'functions_list':
                    # Update attribute value to have list of functions names
                    attr_value = self.functions_list_as_str()

                msg += help_report_template[attr].format(str(attr_value))

        # Add attributes values to the report 
        self.help_report[self.name] += msg

    def functions_list_as_str(self):
        func_names = ''
        for func in self.functions_list:
            func_names += f'{func.__name__}, '

        return f'[{func_names[:-2]}]'

    def extract_attributes(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        attributes = [attr[0] for attr in attributes if not (attr[0].startswith('_'))]
        irrelevent_attributes = ['name', 'required', 'arg_type', 'help_report', 'req_options',
                                 'file_extensions', 'email_regex_pattern', 'password_regex_pattern',
                                 'phone_regex_pattern', 'length_range',
                                 'date_regex_pattern', 'date_format', 'invalid', 'missing', 'validation_report',
                                 'functions_list_arg', 'functions_list', 'req_range_arg', 'comparison_operator_arg',
                                 'req_options_arg', 'date_comparison_operator_arg', 'date_range_arg', 'length_range_arg'
                                 ]

        return [attr for attr in attributes if attr not in irrelevent_attributes]

    def __repr__(self):
        if self.invalid:
            return f'This argument is invalid\nReport:\n{str(self.validation_report)}'
        else:
            return 'This argument is valid'


class NumberArgument(Argument):
    """ A class to represent the number argument which could be int or float """

    def __init__(self, name, required, arg_type, req_range=None, req_options=None,
                 comparison_operator=None, functions_list=None):
        FunctionArgsAssertion.assert_number_type(arg_type)
        super().__init__(name, required, arg_type)
        self.req_range_arg = req_range
        self.req_options_arg = req_options
        self.comparison_operator_arg = comparison_operator
        self.functions_list_arg = functions_list

    @property
    def req_range(self):
        try:
            return self.req_range_arg()
        except:
            return self.req_range_arg

    @property
    def comparison_operator(self):
        try:
            return self.comparison_operator_arg()
        except:
            return self.comparison_operator_arg

    def arg_help(self):
        help_report_template = {
            'req_range': 'This argument should be in the range {} \n',
            'comparison_operator': 'This argument should be {} \n'
        }

        super().arg_help()

        msg = ''
        # Iterate over all class attributes
        for attr in self.extract_attributes():
            attr_value = eval(f'self.{attr}')
            # If attribute has value (not None)
            if attr_value:
                # Add attribute value to the report  
                msg += help_report_template[attr].format(str(attr_value))

        self.help_report[self.name] += msg

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_req_range(arg_val)
        self.assert_req_options(arg_val)
        self.assert_comparison(arg_val)
        self.assert_functions_list(arg_val)

    def assert_req_range(self, arg_val):
        """ To check if the argument value in the required range """
        if self.req_range and not NumberArgument.in_range(arg_val, self.req_range):
            self.update_validation_report('should be in the range {} but the passed value is : {}'.format(
                self.req_range, arg_val))
            return False
        return True

    def assert_comparison(self, arg_val):
        """ To check if the argument value satisfies the comparison operator """
        if self.comparison_operator and not self.comparison_operator.compare(arg_val):
            self.update_validation_report('should be {} {} but the passed value is : {}'.format(
                self.comparison_operator.operator_name.replace('_', ' '),
                self.comparison_operator.operand, arg_val))
            return False
        return True

    @staticmethod
    def in_range(arg_val, req_range):
        FunctionArgsAssertion.assert_range(req_range)
        return True if arg_val >= req_range[0] and arg_val <= req_range[-1] else False


class StringArgument(Argument):

    def __init__(self, name, required, is_email=False,
                 email_regex_pattern='(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[' \
                                     '\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[' \
                                     'a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][' \
                                     '0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[' \
                                     'a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[' \
                                     '\x01-\x09\x0b\x0c\x0e-\x7f])+)\])',
                 is_date=False, date_regex_pattern='^\d{4}-\d{1,2}-\d{1,2}$', date_format='%Y-%m-%d',
                 is_password=False,
                 password_regex_pattern='^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[~#$*])[A-Za-z\d~#$*]{8,}$',
                 is_phone_number=False, phone_regex_pattern='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',
                 req_options=None, length_range=None, regex_pattern=None, in_past=False, date_comparison_operator=None,
                 date_range=None, functions_list=None):

        if (is_email + is_date + is_password + is_phone_number) > 1:
            raise Exception('Only one of is_email, is_date, is_password, is_phone_number, could be True at a time')

        super().__init__(name, required, str)

        self.req_options_arg = req_options
        self.length_range_arg = length_range
        self.is_email = is_email
        self.email_regex_pattern = email_regex_pattern
        self.is_password = is_password
        self.password_regex_pattern = password_regex_pattern
        self.regex_pattern_arg = regex_pattern
        self.is_phone_number = is_phone_number
        self.phone_regex_pattern = phone_regex_pattern
        self.functions_list_arg = functions_list
        self.is_date = is_date
        self.date_regex_pattern = date_regex_pattern
        self.date_format = date_format
        self.date_comparison_operator_arg = date_comparison_operator
        self.date_range_arg = date_range
        self.in_past = in_past

    @property
    def regex_pattern(self):
        try:
            return self.regex_pattern_arg()
        except:
            return self.regex_pattern_arg

    @property
    def date_comparison_operator(self):
        try:
            return self.date_comparison_operator_arg()
        except:
            return self.date_comparison_operator_arg

    @property
    def date_range(self):
        try:
            return self.date_range_arg()
        except:
            return self.date_range_arg

    def arg_help(self):
        help_report_template = {
            'is_email': 'This argument should be a valid email address \n',
            'is_password': f'This argument should represent a valid password that satisfy the following pattern {self.password_regex_pattern} \n',
            'is_phone_number': 'This argument should be a valid phone number \n',
            'is_date': f'This argument should represent a date with the following pattern {self.date_regex_pattern}, and format {self.date_format} \n',
            'in_past': 'This argument should be less than {} \n',
            'date_comparison_operator': 'This argument should be {} \n',
            'date_range': 'This argument should be in the range {} \n',
            'regex_pattern': 'This argument should match the pattern {} \n'
        }
        super().arg_help()

        msg = ''
        # Iterate over all class attributes
        for attr in self.extract_attributes():
            attr_value = eval(f'self.{attr}')

            # If attribute has value (not None) 
            if attr_value:
                # If the attribute in the following list, no need to add it's value to the report
                if attr in ['is_password', 'is_email', 'is_date']:
                    self.help_report[self.name] += help_report_template[attr]
                    continue

                if attr == 'in_past':
                    # Update attribute value to have the current date
                    attr_value = str((datetime.now() + timedelta(days=1)).date())

                # Add attribute value to the report
                msg += help_report_template[attr].format(str(attr_value))
        self.help_report[self.name] += msg

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_req_options(arg_val)
        self.assert_length(arg_val)
        self.assert_email(arg_val)
        self.assert_password(arg_val)
        self.assert_phone(arg_val)
        self.assert_date(arg_val)
        self.assert_regex_pattern(arg_val)
        self.assert_white_spaces(arg_val)
        self.assert_functions_list(arg_val)

    def assert_email(self, arg_val):
        """ To check if argument match the email pattern """
        if self.is_email and not self.is_email_func(arg_val.lower()):
            self.update_validation_report('should be a valid email address')
            return False
        return True

    def is_email_func(self, arg_val):
        """ To check if argument match the email pattern """
        return StringArgument.match_pattern(arg_val, self.email_regex_pattern)

    def assert_password(self, arg_val):
        """ To check if argument match the password pattern """
        if self.is_password:
            is_valid_pass, report = self.is_password_func(arg_val)
            if not is_valid_pass:
                self.update_validation_report(report)
                return False
        return True

    def is_password_func(self, arg_val):
        """
        To check if argument match the password pattern
        The default pattern:
        ^   The password string will start this way
        (?=.*[a-z]) The string must contain at least 1 lowercase alphabetical character
        (?=.*[A-Z]) The string must contain at least 1 uppercase alphabetical character
        (?=.*[0-9]) The string must contain at least 1 numeric character
        (?=.*[!@#$%^&*])    The string must contain at least one special character, but we are escaping reserved RegEx characters to avoid conflict
        (?=.{8,})   The string must be eight characters or longer
        """
        default_password_pattern = '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[~#$*])[A-Za-z\d~#$*]{8,}$'

        if StringArgument.match_pattern(arg_val, self.password_regex_pattern):
            return True, ''

        else:
            if self.password_regex_pattern != default_password_pattern:
                return False, 'should be a valid password'

            else:
                return False, StringArgument.invalid_password_report(arg_val)

    @staticmethod
    def invalid_password_report(password):
        min_len = 8
        white_space = '\s'
        rules = {
            'upper case': '[A-Z]',
            'lower case': '[a-z]',
            'numeric digit': '(\d)',
            'special character from ~#$*': '[~#$*]'
        }
        report = ''

        if len(password) < min_len:
            report = report + f'The password should be at least {min_len} charachters long.\n'
        if re.search(white_space, password) is not None:
            report = report + 'The password should not contain spaces.\n'
        for k, v in rules.items():
            if re.search(v, password) is None:
                report = report + f'The password should contain at least one {k}\n'

        return report

    def assert_phone(self, arg_val):
        """ To check if argument match the phone number pattern """
        if self.is_phone_number and not self.is_phone_func(arg_val):
            self.update_validation_report('should be a valid phone number')
            return False
        return True

    def is_phone_func(self, arg_val):
        """ To check if argument match the phone number pattern """
        return StringArgument.match_pattern(arg_val, self.phone_regex_pattern)

    def assert_date(self, arg_val):
        """ To check if argument match the date pattern """
        valid_date = True
        if self.is_date:
            if not self.is_date_func(arg_val):
                self.update_validation_report('should be a valid date')
                valid_date = False

            else:
                # Test date comparison operator
                arg_val_date = datetime.strptime(arg_val, self.date_format)
                valid_date = self.check_date_comparison(arg_val_date)
                valid_date = valid_date and self.check_date_range(arg_val_date)
                valid_date = valid_date and self.check_in_past(arg_val_date)

        return valid_date

    def check_date_comparison(self, arg_val):
        """ To check if the argument value satisfies the comparison operator """
        if self.date_comparison_operator:
            # Convert operand to datetime
            if not isinstance(self.date_comparison_operator.operand, datetime):
                self.date_comparison_operator.operand = \
                    datetime.strptime(self.date_comparison_operator.operand,
                                      self.date_format)

            if not self.date_comparison_operator.compare(arg_val):
                self.update_validation_report('should be {} {} but the passed value is : {}'.format(
                    self.date_comparison_operator.operator_name.replace('_', ' '),
                    self.date_comparison_operator.operand, arg_val))
                return False
        return True

    def check_date_range(self, arg_val):
        if self.date_range:
            since_date = self.date_range[0]
            if not isinstance(since_date, datetime):
                since_date = datetime.strptime(since_date, self.date_format)

            to_date = self.date_range[1]
            if not isinstance(to_date, datetime):
                to_date = datetime.strptime(to_date, self.date_format)

            if since_date <= arg_val <= to_date:
                return True
            else:
                self.update_validation_report('should be between {} and {} but the passed value is : {}'.format(
                    since_date, to_date, arg_val))
                return False

        return True

    def check_in_past(self, arg_val):
        if self.in_past:
            current_date = datetime.now() + timedelta(days=1)
            if arg_val > current_date:
                self.update_validation_report('should be less than {} but the passed value is : {}'.format(
                    current_date.date(), arg_val.date()))
                return False
        return True

    def is_date_func(self, arg_val):
        """
        To check if argument match the date pattern
        The default pattern matches 4/1/2001 | 12/12/2001 | 55/5/3434
        """
        return StringArgument.match_pattern(arg_val, self.date_regex_pattern)

    def assert_regex_pattern(self, arg_val):
        """ To check if argument match the passed regex pattern """
        if self.regex_pattern and not StringArgument.match_pattern(arg_val, self.regex_pattern):
            self.update_validation_report('should match the pattern {}'.format(self.regex_pattern))
            return False
        return True

    @staticmethod
    def match_pattern(arg_val, pattern):
        """ To check if argument match the passed regex pattern """
        status = re.match(pattern, arg_val)
        if status:
            return True
        return False

    def assert_white_spaces(self, arg_val):
        """ To check that not all characters in the argument are white spaces """
        if arg_val.isspace():
            self.update_validation_report('should not have only white spaces')
            return False
        return True


class ListArgument(Argument):
    def __init__(self, name, required, arg_obj, length_range=None, all_items_unique=False, req_options=None):
        super().__init__(name, required, list)
        self.length_range_arg = length_range
        self.arg_obj = arg_obj
        self.all_items_unique = all_items_unique
        self.req_options_arg = req_options

    def arg_help(self):
        super().arg_help()

        # Help report should contain both list conditions and it's element (argument) conditions
        self.help_report[self.name] = {
            'list_item': dict(),
            'conditions': self.help_report[self.name]
        }

        if self.all_items_unique:
            self.help_report[self.name]['conditions'] += 'This argument items should be unique \n'

            # Add list argument conditions to the report
        self.arg_obj.arg_help()
        self.help_report[self.name]['list_item'] = self.arg_obj.help_report[self.arg_obj.name]

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None or not self.assert_length(arg_val):
            return

        self.assert_req_options(arg_val)
        self.assert_items_unique(arg_val)
        self.assert_items_val(arg_val)

    def assert_items_unique(self, arg_val):
        """ To check if all items in the list are unique """
        if self.all_items_unique and len(arg_val) != len(set(arg_val)):
            self.update_validation_report(
                'All the items inside the list {} should be unique but some items are repeated'.format(
                    self.name))
            return False
        return True

    def assert_items_val(self, arg_val):
        # Convert list into dict to fit assert_arg function
        items_dict = {'{}[{}]'.format(self.name, ind): item for ind, item in enumerate(arg_val)}

        for ind in items_dict:
            arg_obj = deepcopy(self.arg_obj)
            arg_obj.update_name(ind)
            arg_obj.assert_arg(items_dict)

            if arg_obj.invalid:
                self.update_validation_report(arg_obj.validation_report)


class FileArgument(Argument):
    def __init__(self, name, required, file_size=None,
                 file_extensions=['.jpg', '.jpeg', '.png', '.tiff', '.tif',  # Image
                                  '.gif', '.mp4', '.17',  # Video
                                  '.mp3',  # Audio
                                  '.pdf', '.txt', '.docx', '.xlsx', '.csv']  # Documents
                 ):
        super().__init__(name, required, dict)
        self.file_size = file_size
        self.file_extensions_arg = file_extensions

    @property
    def file_extensions(self):
        try:
            return self.file_extensions_arg()
        except:
            return self.file_extensions_arg

    def arg_help(self):
        self.reset_arg()
        self.help_report = {'file': dict()}

        if self.required:
            msg = 'File is required \n'

        else:
            msg = 'File is optional \n'

        msg += f'File extension should be one of the following extensions {self.file_extensions}'
        self.help_report['file']['file_conditions'] = msg

        if self.file_size:
            update_file_size_report = lambda report: report + ' MB' if (
                    report.endswith(']') or str.isdigit(report[-1])) else report
            self.file_size.arg_help()

            report_details = self.file_size.help_report[self.file_size.name].split(' \n')
            file_size_report = {self.file_size.name: ' \n'.join([
                update_file_size_report(rep) for rep in report_details if rep
            ])
            }
            self.help_report['file'].update(file_size_report)

    def assert_arg(self):
        self.reset_arg()
        if not self.assert_existence(request.files):
            return

        file_size = request.content_length / 1024 / 1024  # MB
        arg_val = {'file_name': request.files['file'].filename, 'file_size': file_size}

        self.assert_file_name(arg_val)
        self.assert_file_size(arg_val)

    def assert_existence(self, files):
        """ Check if the argument is available or not """
        arg_available = 'file' in files and files['file']
        if self.required and not arg_available:
            self.update_validation_report('missing')

        return arg_available

    def assert_file_name(self, arg_val):
        """To check if file name match the required extensions"""
        if not self.has_valid_extension(arg_val['file_name']):
            _, ext = os.path.splitext(arg_val['file_name'])
            self.update_validation_report(
                'the extension should be one of the following extensions {}  but the passed value is {} '.format(
                    self.file_extensions, ext))
            return False

        return True

    def has_valid_extension(self, arg_val):
        _, ext = os.path.splitext(arg_val)
        return ext.lower() in self.file_extensions

    def assert_file_size(self, arg_val):
        if self.file_size:
            file_size = deepcopy(self.file_size)
            file_size.update_name('file_size')
            file_size.assert_arg(arg_val)

            if file_size.invalid:
                update_file_size_report = lambda report: report + ' MB' if (
                        report.endswith(']') or str.isdigit(report[-1])) else report
                updated_report = file_size.validation_report[file_size.name].replace('\n', '')
                report_details = updated_report.split()

                file_size.validation_report[file_size.name] = ' '.join([
                    update_file_size_report(rep) for rep in report_details if rep
                ]) + ' \n'

                self.update_validation_report(file_size.validation_report)
                return False

        return True


class JsonArgument(Argument):
    """ A class to represent the number argument which could be int or float """

    def __init__(self, name, required, fields=None):
        super().__init__(name, required, dict)
        self.fields = fields

    def arg_help(self):
        super().arg_help()

        if self.fields:
            self.help_report[self.name] += f'This argument should have the following fields {self.fields} \n'

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_fields(arg_val)

    def assert_fields(self, arg_val):
        if self.fields:
            recieved_fields = list(arg_val.keys())
            recieved_fields.sort()
            self.fields.sort()

            if self.fields != recieved_fields:
                self.update_validation_report(f'fields should be {self.fields} but the passed are {recieved_fields}')
                return False

        return True


class AdvancedJsonArgument(Argument):

    def __init__(self, name, required, arguments, fields=None):
        super().__init__(name, required, dict)
        self.fields = fields
        self.arguments = arguments

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_fields(arg_val)
        for argument in self.arguments:
            arg_obj = deepcopy(argument)
            arg_obj.update_name(argument.name)

            arg_obj.assert_arg(args_dict[self.name])

            if arg_obj.invalid:
                self.update_validation_report(arg_obj.validation_report)

    def assert_fields(self, arg_val):
        if self.fields:
            recieved_fields = list(arg_val.keys())
            recieved_fields.sort()
            self.fields.sort()

            if self.fields != recieved_fields:
                self.update_validation_report(f'fields should be {self.fields} but the passed are {recieved_fields}')
                return False

        return True
