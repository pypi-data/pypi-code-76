from configparser import ConfigParser
import os
from .exceptions import MessageError


class ConfigError(MessageError):
    message = 'Invalid configuration'


class InvalidConfigError(ConfigError):
    pass


class ConversionFailure(MessageError):
    message = 'Invalid type conversion requested'


def ConvertBoolean(value):
    """
    Attempt to convert value to a boolean. If the value is not a possible boolean
    string the result will return None instead of True or False.

    :param value: Value which should be checked as a boolean.
    :return: True or False if the value is recognized, or None if it is not a valid
            boolean string.
    """
    value = str(value).lower()
    if value in ['yes', '1', 'true']:
        return True
    if value in ['no', '0', 'false']:
        return False
    return None


def ConvertHashType(value):
    """
    Attempt to convert a space separated series of key=value pairs into a dictionary
    of pairs. If any value fails to split successfully an error will be raised.

    :param value: Space delimited string of key-value pairs
    :return: Dictionary of key-value pairs.
    """
    collection = dict()
    for option in value.split():
        try:
            k, v = option.split('=')
        except ValueError:
            raise ConversionFailure("Invalid option '{}' for key-value pair: {}"
                .format(option, value))
        collection[k] = v.strip()
    return collection


def ConvertValue(value, hint=None):
    """
    Attempt to convert value to a supported type. Hint can be used to influence
    how the value is coerced. In the event of a failure an error will be raised.

    Supported hints are:
    - Array
    - Hash
    - Integer
    - Float
    - Boolean
    - String

    :param value: Value to be coerced.
    :param hint: Optional hint to indicate desired type.
    :return: Value coerced to type.
    """
    if isinstance(value, str):
        value = value.strip()
    try:
        if hint is not None:
            if hint == Config.ARRAY_TYPE:
                return value.split()
            elif hint == Config.HASH_TYPE:
                return ConvertHashType(value)
            elif hint == Config.INT_TYPE:
                if isinstance(value, str) and '.' in value:
                    return int(float(value))
                return int(value)
            elif hint == Config.BOOL_TYPE:
                return ConvertBoolean(value)
            elif hint == Config.FLOAT_TYPE:
                return float(value)
            elif hint == Config.STRING_TYPE:
                return value
            raise ConversionFailure
        else:
            b = ConvertBoolean(value)
            if b is not None:
                return b
            v = float(value)
            if isinstance(value, str) and '.' in value:
                return v
            return int(v)
    except (TypeError, ValueError):
        if hint is not None:
            raise ConversionFailure('Failed to convert the given value to the requested type')
        else:
            if ConvertBoolean(value) is None:
                return value
            return ConvertBoolean(value)


class Config(object):
    ARRAY_TYPE = 'array'
    BOOL_TYPE = 'bool'
    FLOAT_TYPE = 'float'
    HASH_TYPE = 'hash'
    INT_TYPE = 'int'
    STRING_TYPE = 'string'

    GLOBAL_SECTION = 'global'
    INFLUXDB_SECTION = 'influxdb'
    SUPPORTED_DATABASES = [INFLUXDB_SECTION]
    DATABASE_FIELDS = {
        INFLUXDB_SECTION: [
            ('database', STRING_TYPE),
            ('port', INT_TYPE),
            ('server', STRING_TYPE),
            ('ssl', BOOL_TYPE),
            ('verify', BOOL_TYPE)
        ]}
    ENTRY_FIELDS = [
        ('fields', ARRAY_TYPE),
        ('tags', HASH_TYPE)
    ]

    def __init__(self, path, root):
        """
        Constructor for the config object. The path value should represent an
        existing config file that the parser should read in. The root corresponds
        to the application defined root element indicating which config elements
        should be parsed form the config file.

        :param path: Path o the config file.
        :param root: Root element in the global section indicating all entries
                     to parse.
        """
        self.path = path
        self.root = root
        self.config = {}
        self.database = None

    def GetDatabase(self):
        """
        Retrieve the database configuration from the underlying config.

        :return: A tuple consisting of the database type and the respective configuration.
        """
        if not self.IsLoaded():
            self.Load()
        return self.database, self.config[self.database]

    def GetField(self, field):
        """
        Query the main fields list and return the type hint for the given field if it
        exists. The function will throw a KeyError in the event the field does not
        exist or is an invalid submission.

        :param field: String field to lookup in the config.
        :return: Type hint if the field is known.
        """
        if field is None:
            raise KeyError('Unknown field')
        if not self.IsLoaded():
            self.Load()
        return self.config['fields'][field]

    def GetRoot(self):
        """
        Returns the application root of the configuration file.

        :return: Application data from the root element.
        """
        if not self.IsLoaded():
            self.Load()
        if self.path is None:
            return {}
        return self.config[self.root]

    def GetTags(self, entity):
        """
        Lookup the tags for an entity if it is known. I fthe entity is not known a
        key error is returned. If the entity has no tags an empty list will be
        returned.

        :param entity: An entity to lookup in the config.
        :return: Tag list if the entity is known or an empty list if no tags are given.
        """
        if entity is None:
            raise KeyError('Unknown entity')
        if not self.IsLoaded():
            self.Load()
        if self.path is None:
            return {}
        return self.config[self.root][entity].get('tags', [])

    def IsLoaded(self):
        """
        Predicate checking if the cofnig has already been loaded.

        :return: True or False if the config has been loaded.
        """
        if self.path is None:
            return True
        return len(self.config) > 0

    def Load(self):
        """
        Load the configuration for the given file.

        On an error, this function will raise an error indicating what the failure
        was when it occurred.

        :return: None
        """
        if self.IsLoaded():
            return

        if not os.path.isfile(self.path):
            raise ConfigError('Config file does not exist')

        parser = ConfigParser()
        try:
            parser.read(self.path)
        except IOError:
            raise ConfigError('Failed to parse configuration')

        if not parser.has_section(self.GLOBAL_SECTION):
            raise InvalidConfigError('No global section')

        self.RequiredFields(parser, self.GLOBAL_SECTION, ['database', self.root])
        self.database = parser.get(self.GLOBAL_SECTION, 'database')

        if not self.database or self.database not in self.SUPPORTED_DATABASES:
            raise InvalidConfigError('Invalid or unsupported database value')

        self.config[self.database] = {}
        for field, hint in self.DATABASE_FIELDS[self.database]:
            if parser.has_option(self.database, field):
                try:
                    self.config[self.database][field] = ConvertValue(
                        parser.get(self.database, field),
                        hint=hint)
                except ConversionFailure:
                    raise InvalidConfigError("Invalid field '{}' expected type '{}'"
                        .format(field, hint))

        root = parser.get(self.GLOBAL_SECTION, self.root)
        if not root:
            raise InvalidConfigError("Missing config for root '{}".format(self.root))

        self.config['fields'] = {}
        self.config[self.root] = {}
        for field in root.split():
            self.config[self.root][field] = {}

        if len(self.config[self.root]) == 0:
            raise InvalidConfigError("Root element '{}' has no entries".format(self.root))

        fields = {}
        for entry in self.config[self.root].keys():
            self.RequiredFields(parser, entry, [k for k, v in self.ENTRY_FIELDS])
            self.config[self.root][entry] = {}

            for field, hint in self.ENTRY_FIELDS:
                if parser.has_option(entry, field):
                    try:
                        self.config[self.root][entry][field] = ConvertValue(
                            parser.get(entry, field),
                            hint=hint)
                    except ConversionFailure:
                        raise InvalidConfigError("Invalid field '{}' expected type '{}'"
                            .format(field, hint))

            for option in parser.options(entry):
                if option in self.config[self.root][entry]:
                    continue
                try:
                    self.config[self.root][entry][option] = ConvertValue(
                        parser.get(entry, option))
                except ConversionFailure:
                    raise InvalidConfigError("Invalid field '{}' unable to determine type"
                        .format(option))

            for field in self.config[self.root][entry]['fields']:
                if field not in fields:
                    fields[field] = []

        for field in fields.keys():
            if not parser.has_section(field):
                raise InvalidConfigError("Unknown field '{}' in config")
            for option in parser.options(field):
                if field not in self.config['fields']:
                    self.config['fields'][option] = self.ParseOption(parser, field, option)
                    fields[field].append(option)
                else:
                    raise InvalidConfigError("Duplicate field definition for '{}' in section '{}'"
                        .format(option, field))

        for entry, values in self.config[self.root].items():
            fieldList = []
            for field in values['fields']:
                if field in fields:
                    fieldList.extend(fields[field])
                else:
                    raise InvalidConfigError("Unknown field '{}' in entry '{}'".format(field, entry))
            values['fields'] = fieldList

    @staticmethod
    def ParseOption(parser, section, option):
        """
        Parse a given option as a defined type. This attempts to match the value of an option
        to a known type which can be coerced into a native value.

        :param parser: ConfigParser instance
        :param section: Section containing fields
        :param option: Option with a value representing a known coerseable type.
        :return:
        """
        if not parser.has_option(section, option):
            raise ConfigError("Option '{}' does not exist in section '{}'"
                .format(option, section))
        value = parser.get(section, option)
        if value in [Config.BOOL_TYPE, Config.FLOAT_TYPE,
                     Config.INT_TYPE, Config.STRING_TYPE]:
            return value
        raise InvalidConfigError("Invalid type '{}' for option '{}'".format(value, option))

    @staticmethod
    def RequiredFields(parser, section, fields):
        """
        Check a section for required fields. This function will raise an error if all
        required fields are not present within the given section.

        :param parser: ConfigParser instance
        :param section: Section containing fields
        :param fields: Array of fields (strings) which should be validated for existence.
        :return: None
        """
        for field in fields:
            if not parser.has_option(section, field):
                raise InvalidConfigError("Section '{}' missing required field '{}'"
                    .format(section, field))

    def Reload(self):
        """
        Clean the config state and reload the config from disk.

        :return: None
        """
        self.config = {}
        self.database = None
        self.Load()
