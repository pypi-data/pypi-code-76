import enum


class RecordStatus(enum.Enum):
    ACTIVE = "Active"
    DELETED = "Delete"
    ACTIVE_LOCKED = "Active Locked"

    def describe(self):
        """
        This function is used to get detailed information about an enum object.

        For example;
            when RecordStatus.ACTIVE.describe() is called, it's name and value will be returned i.e. ACTIVE, Active
        :return:
        """
        return self.name, self.value

    def __str__(self):
        """
        This function is used to get the object name when an object is called.

        :return: str
        """
        return self.name


class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"

    def describe(self):
        """
        This function is used to get detailed information about an enum object.

        For example;
            when Gender.MALE.describe() is called, it's name and value will be returned i.e. MALE, Male
        :return:
        """
        return self.name, self.value

    def __str__(self):
        """
        This function is used to get the object name when an object is called.

        :return: str
        """
        return self.name


class FileAttribute(enum.Enum):
    """
    This class contains operations that can be done on a file.

    For example;
        1. Create a new file
        2. Read from an existing file
        3. Append data to an existing file
    """
    CREATE = ('Write to file', 'w+')
    READ = ('Read from file', 'r+')
    APPEND = ('Append data to a file', 'a+')

    def __init__(self, display_name, code_name):
        self.display_name = display_name  # Display name
        self.code_name = code_name  # Attribute of a file object tells you which mode a file was opened in

    def describe(self):
        """
        This function is used to get detailed information about an enum object.

        For example;
            when FileAttribute.CREATE.describe() is called, it's name and value will be returned i.e. CREATE, Write to file
        :return:
        """
        return self.name, self.display_name

    def __str__(self):
        """
        This function is used to get the object name when an object is called.

        :return: str
        """
        return self.name


class SeverityLevel(enum.Enum):
    """
    This class represents the severity of the log message that is being logged to the logging microservice
    """
    DEBUG = "Debug"
    INFO = "Info"
    CRITICAL = "Critical"
    FATAL = "Fatal"
    ERROR = "Error"
    WARNING = "Warning"

    def describe(self):
        """
        This function is used to get detailed information about an enum object.

        For example;
            when SeverityLevel.DEBUG.describe() is called, it's name and value will be returned i.e. DEBUG, Debug
        :return: tuple
        """
        return self.name, self.value

    def __str__(self):
        """
        This function is used to get the object name when an object is called.

        :return: str
        """
        return self.name


class LogStatus(enum.Enum):
    """
    This class represents the validity of data that is being sent to the logging microservice
    """
    VALID = "Valid"
    INVALID = "Invalid"

    def describe(self):
        """
        This function is used to get detailed information about an enum object.

        For example;
            when LogStatus.VALID.describe() is called, it's name and value will be returned i.e. VALID, Valid
        :return:
        """
        return self.name, self.value

    def __str__(self):
        """
        This function is used to get the object name when an object is called.

        :return: str
        """
        return self.name
