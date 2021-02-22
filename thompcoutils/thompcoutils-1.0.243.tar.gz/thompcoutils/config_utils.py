from thompcoutils.log_utils import get_logger
from thompcoutils.cron_time import CronTime
import thompcoutils.file_utils as file_utils
from shutil import copyfile
import datetime
import sys
from builtins import staticmethod
import ast
from configparser import ConfigParser, NoOptionError, NoSectionError, DuplicateSectionError
import os
from dateutil import parser


class ConfigException(Exception):
    pass


class EmailConnectionConfig:
    def __init__(self, cfg_mgr, username='myname@google.com', password='mySecretPassword',
                 from_user='Where the email will come from', smtp_host='smtp.gmail.com',
                 smtp_port=587, section_heading='email connection',
                 username_tag='username', password_tag='password', from_tag='from', smtp_host_tag='smtp_host',
                 smtp_port_tag='smtp_port'):
        """
        This class represents data in a configuration file that represents an email configuration
        :param cfg_mgr: the configuration manager for this file
        :param username: email username
        :param password: email password
        :param from_user: user sending the email (could be an application)
        :param smtp_host: smtp host of the mail server
        :param smtp_port: smtp port of the mail server
        :param section_heading: heading of the email (for deprecated configuration files)
        :param username_tag: specialized username tag (for deprecated configuration files)
        :param password_tag: specialized password tag (for deprecated configuration files)
        :param from_tag: specialized from tag (for deprecated configuration files)
        :param smtp_host_tag: specialized smtp host tag (for deprecated configuration files)
        :param smtp_port_tag: specialzed smtp port tag (for deprecated configuration files)
        """
        self.username = cfg_mgr.read_entry(section=section_heading, entry=username_tag, default_value=username)
        self.password = cfg_mgr.read_entry(section=section_heading, entry=password_tag, default_value=password)
        self.from_user = cfg_mgr.read_entry(section=section_heading, entry=from_tag, default_value=from_user,
                                            notes='the user/application sending the email')
        self.smtp_host = cfg_mgr.read_entry(section=section_heading, entry=smtp_host_tag, default_value=smtp_host)
        self.smtp_port = cfg_mgr.read_entry(section=section_heading, entry=smtp_port_tag, default_value=smtp_port)


class HiLow:
    """
    HiLow class provides a config file to store low and hi values.  If a low value for a tag/entry is lower than the
    existing value, it will be updated.  Similarly, if a hi value for is higher than the existing hi value, it will be
    updated.
    """
    smallest = -sys.maxsize-2
    biggest = sys.maxsize-2
    hi_tag = 'hi'
    low_tag = 'low'
    last_tag = 'last'
    low_changed_tag = 'low_changed'
    hi_changed_tag = 'hi_changed'
    last_changed_tag = 'last_changed'
    direction_tag = 'direction'
    change_amount_tag = 'change_amount'

    class Direction(enumerate):
        Up = 'up'
        Down = 'down'
        NoChange = 'no change'

        @staticmethod
        def validate(string):
            if string == str(HiLow.Direction.Up):
                return HiLow.Direction.Up
            elif string == str(HiLow.Direction.Down):
                return HiLow.Direction.Down
            elif string == str(HiLow.Direction.NoChange):
                return HiLow.Direction.NoChange
            else:
                raise ConfigException('{} not recognized as a HiLow.Direction'.format(string))

    def __init__(self, file_name, value_type=float):
        """
        :param file_name: name of the file to store values
        """
        self.file_name = file_name
        if not os.path.exists(file_name):
            file_utils.touch(file_name)
        self.cfg_mgr = ConfigManager(file_name)
        self.value_type = value_type

    def read_values(self, entry):
        """
        gets the current values for a tag/entry
        :param entry: tag/entry`
        :return: a dictionary of values (i.e. {'hi': 10, 'low': 2} )
        """
        try:
            hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, value_type=self.value_type,
                                         default_value=self.smallest)
        except ValueError:
            hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, value_type=self.value_type,
                                         default_value=self.smallest + .01)
        try:
            low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, value_type=self.value_type,
                                          default_value=self.biggest)
        except ValueError:
            low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, value_type=self.value_type,
                                          default_value=self.biggest - .01)
        hi_changed_time = self.cfg_mgr.read_entry(section=entry, entry=self.hi_changed_tag,
                                                  default_value=datetime.datetime.now())
        low_changed_time = self.cfg_mgr.read_entry(section=entry, entry=self.low_changed_tag,
                                                   default_value=datetime.datetime.now())

        direction = self.cfg_mgr.read_entry(section=entry, entry=self.direction_tag,
                                            default_value=str(self.Direction.NoChange))
        direction = self.Direction.validate(direction)

        try:
            last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, value_type=self.value_type,
                                           default_value=0)
        except ValueError:
            last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, value_type=self.value_type,
                                           default_value=0.01)
        try:
            changed_amount = self.cfg_mgr.read_entry(section=entry, entry=self.change_amount_tag,
                                                     value_type=self.value_type, default_value=0)
        except ValueError:
            changed_amount = self.cfg_mgr.read_entry(section=entry, entry=self.change_amount_tag,
                                                     value_type=self.value_type, default_value=0.01)
        last_changed = self.cfg_mgr.read_entry(section=entry, entry=self.last_changed_tag,
                                               default_value=datetime.datetime.now())
        return {self.hi_tag: hi, self.low_tag: low,
                self.low_changed_tag: low_changed_time, self.hi_changed_tag: hi_changed_time,
                self.last_tag: last, self.last_changed_tag: last_changed, self.direction_tag: direction,
                self.change_amount_tag: changed_amount}

    def write_value(self, entry, value):
        try:
            self.cfg_mgr.config.add_section(entry)
        except DuplicateSectionError:
            pass

        try:
            cfg_last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, value_type=self.value_type,
                                               default_value=0)
        except ValueError:
            cfg_last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, value_type=self.value_type,
                                               default_value=.01)
        if value < cfg_last:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=cfg_last-value)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.Down)
            try:
                cfg_low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, value_type=self.value_type,
                                                  default_value=self.biggest)
            except ValueError:
                cfg_low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, value_type=self.value_type,
                                                  default_value=self.biggest - .01)
            if value < cfg_low:
                self.cfg_mgr.write_entry(section=entry, entry=self.low_changed_tag, value=datetime.datetime.now())
                self.cfg_mgr.write_entry(section=entry, entry=self.low_tag, value=value)
        elif value > cfg_last:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=value-cfg_last)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.Up)
            try:
                cfg_hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, value_type=self.value_type,
                                                 default_value=self.smallest)
            except ValueError:
                cfg_hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, value_type=self.value_type,
                                                 default_value=self.smallest + .01)
            if value > cfg_hi:
                self.cfg_mgr.write_entry(section=entry, entry=self.hi_changed_tag, value=datetime.datetime.now())
                self.cfg_mgr.write_entry(section=entry, entry=self.hi_tag, value=value)
        else:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=0)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.NoChange)
        self.cfg_mgr.write_entry(section=entry, entry=self.last_tag, value=value)
        self.cfg_mgr.write_entry(section=entry, entry=self.last_changed_tag, value=datetime.datetime.now())
        self.cfg_mgr.write(out_file=self.file_name, stop=False, overwrite=True)
        return self.read_values(entry)


class ConfigManager:
    def __init__(self, file_name, title=None, create=False):
        """
        ConfigManager allows for reading and writing a configuration file
        :param file_name: name of the config file
        :param title: information to put at the top of the file when writing it out
        :param create: if True, creates the file
        """
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.create = create
        if not create:
            if os.path.exists(file_name):
                self.config.read(file_name)
            else:
                raise FileNotFoundError('File {} does not exist!'.format(file_name))
        self.notes = []
        self.title = title
        self.values = {}

    @staticmethod
    def missing_entry(section, entry, file_name, default_value=None):
        """
        this method logs a message about an entry that is missing from the config file
        :param section: section of the config file
        :param entry: entry in the section of the config file
        :param file_name: name of the file
        :param default_value: default value for the entry
        :return: None
        """
        logger = get_logger()
        logger.debug('starting')
        if default_value is None:
            log_fn = logger.critical
            message = 'Required entry'
            default_value = ''
        else:
            log_fn = logger.debug
            message = 'Entry'
            if default_value == '':
                default_value = 'Ignoring.'
            else:
                default_value = 'Using default value of (' + str(default_value) + ')'
        log_fn(message + ' \"' + entry + '\" in section [' + section + '] in file: ' + file_name
               + ' is malformed or missing.  ' + str(default_value))
        if default_value == '':
            log_fn('Exiting now')
            sys.exit()

    @staticmethod
    def _insert_note(lines, line_number, note):
        """
        This method inserts a note at a particular line in an array of lines that will ultimately be written to the
        config file
        :param lines: array of strings
        :param line_number: the line number to insert the note at
        :param note: the note to be inserted
        :return:
        """
        if '\n' in note:
            message = note.split('\n')
        else:
            message = note
        if message is None:
            pass
        elif type(message) == str:
            lines.insert(line_number, '# ' + message + ':\n')
        else:
            for line in message[:-1]:
                lines.insert(line_number, '# ' + line + '\n')
                line_number += 1
            lines.insert(line_number, '# ' + message[-1] + ':\n')
        lines[line_number + 1] += "\n"

    def add_note(self, section, entry, notes):
        """
        Adds a note to an entry or a section (if entry is None)
        :param section: Section to add the note to
        :param notes: note to add (long lines will be broken up)
        :param entry: entry to add the note to.  If this is None, the note is added to the section itself.
        :return: None
        """
        self.notes.append({'section': section,
                           'entry': entry,
                           'notes': notes})

    def read_entry(self, section, entry, default_value, notes=None, value_type=None,
                   use_default_if_missing=True, allowed_values=None):
        """
        This method reads an entry in the config file
        :param section: section of the config file
        :param entry: entry in the section of the config file
        :param default_value: default value to use if the entry is missing
        :param notes: notes about the entry
        :param value_type: the type of data the entry represents
        :param use_default_if_missing: if True, the default value is used if the entry is missing
        :param allowed_values: only allow one of the entries in this list
        :return: the value in the entry
        """
        logger = get_logger()
        value = default_value
        wrong_type = None
        if self.create:
            try:
                self.config.add_section(section)
            except DuplicateSectionError:
                pass
            if notes:
                if allowed_values:
                    notes += " (must be one of " + str(allowed_values) + ")"
                self.add_note(section, entry, notes)
            self.config.set(section, entry, str(default_value))
        else:
            if value_type is None:
                if default_value is None:
                    raise ConfigException('if default_value=None, value_type must be set')
                value_type = type(default_value)
            try:
                if value_type == str:
                    value = self.config.get(section, entry)
                    if not isinstance(value, str):
                        wrong_type = str
                elif value_type == bool:
                    value = self.config.getboolean(section, entry)
                    if not isinstance(value, bool):
                        wrong_type = bool
                elif value_type == int:
                    value = self.config.getint(section, entry)
                    if not isinstance(value, int):
                        wrong_type = int
                elif value_type == float:
                    value = self.config.getfloat(section, entry)
                    if not isinstance(value, float):
                        wrong_type = float
                elif value_type == dict:
                    value = ast.literal_eval(self.config.get(section, entry))
                    if not isinstance(value, dict):
                        wrong_type = dict
                elif value_type == list:
                    value = ast.literal_eval(self.config.get(section, entry))
                    if not isinstance(value, list):
                        wrong_type = list
                elif value_type == datetime.datetime:
                    value = parser.parse(self.config.get(section, entry))
                    if not isinstance(value, datetime.datetime):
                        wrong_type = datetime.datetime
                elif value_type == CronTime:
                    format_entry = '{}_format'.format(entry)
                    time_entry = '{}_time'.format(entry)
                    try:
                        time_format = self.config.get(section, format_entry)
                    except NoOptionError:
                        raise ConfigException('{} missing for entry {} under section {}', format_entry, entry, section)
                    try:
                        value = self.config.get(section, time_entry)
                    except NoOptionError:
                        raise ConfigException('{} missing for entry {} under section {}', time_entry, entry, section)
                    value = CronTime.strfpcrontime(value, time_format)
                    if not isinstance(value, CronTime):
                        wrong_type = CronTime

                else:
                    raise ConfigException('type {} not handled for ()'.format(type(default_value), default_value))
            except NoOptionError:
                logger.debug('Entry {} in section [{}] is missing.  Using default value of {}'.format(entry, section,
                                                                                                      default_value))
                if not use_default_if_missing:
                    value = None
            except NoSectionError:
                logger.debug('section [{}] is missing.  Using default value of {}'.format(section, default_value))
                if not use_default_if_missing:
                    value = None
            except ValueError as e:
                raise ConfigException("Invalid value of {} ({}) for entry {} under section {}".
                                      format(value, str(e), entry, section))

        if wrong_type is not None:
            raise ConfigException("{} is not a {} for entry {} under section {}".
                                  format(value, str(wrong_type), entry, section))

        if allowed_values and value not in allowed_values:
            raise ConfigException("{} is not one of the allowed values: {} for entry {} under section {}".
                                  format(value, allowed_values, entry, section))
        return value

    def add_section_notes(self, section, notes):
        self.notes.append({'section': section,
                           'entry': None,
                           'notes': notes})

    def write_entry(self, section, entry, value, note=None, format_string=None):
        """
        This method writes the information into a member array that will be written to the file later
        :param section: section of the config file
        :param entry: entry in the section of the config file
        :param value: value for the entry
        :param note: any notes for this entry
        :param format_string: special formatting to converty the value to a string representation
        :return:
        """
        try:
            if isinstance(value, CronTime):
                self.config.set(section, '{}_format'.format(entry), format_string.replace('%', '%%'))
                self.config.set(section, '{}_time'.format(entry), value.strfcrontime(format_string))
            else:
                self.config.set(section, str(entry), str(value))
        except DuplicateSectionError:
            self.config.add_section(section)
            self.config.set(section, str(entry), str(value))

        if note is not None:
            self.add_note(section, entry, note)

    def write(self, *args, **kwargs):
        overwrite = kwargs.get('overwrite', False)
        out_file = kwargs.get('out_file', True)  # stop=True, overwrite=False):
        stop = kwargs.get('stop', True)  # stop=True, overwrite=False):
        if os.path.isfile(out_file) and not overwrite:
            raise ConfigException('File {} exists!  You must remove it before running this'.format(out_file))
        f = open(out_file, 'w')
        self.config.write(f)
        f.close()
        f = open(out_file)
        lines = f.readlines()
        f.close()
        if self.title is not None:
            ConfigManager._insert_note(lines, 0, self.title)
        for note in self.notes:
            in_section = False
            line_number = 0
            for line in lines:
                if line.startswith("[" + note["section"] + "]"):
                    in_section = True
                elif in_section and line.startswith(note['entry']):
                    ConfigManager._insert_note(lines, line_number, note['notes'])
                    break
                line_number += 1
        f = open(out_file, 'w')
        contents = ''.join(lines)
        f.write(contents)
        f.close()
        if stop:
            print('Done writing {} configuration file.  Stopping execution, please re-run'.format(out_file))
            sys.exit()


class PiConfig(ConfigManager):
    _boot_folder = '/boot'
    _wpa_supplicant_file = '/etc/wpa_supplicant/wpa_supplicant.conf'
    _host_name_file = '/etc/hostname'
    _hosts_file = '/etc/hosts'
    _default_file_extension = '.default'

    class WiFi:
        section = 'wifi'
        ssid_tag = 'ssid'
        key_tag = 'key'
        hidden_tag = 'hidden'
        priority_tag = 'priority'

        def __init__(self, cfg_mgr, ssid='my wifi ap', wifi_key='my wifi key', hidden=False, section=section,
                     priority=1):
            """
            WifiConfig defines the data for the wpa_suplicant file
            :param cfg_mgr: the ConfigManager
            :param ssid: SSID for this wifi
            :param wifi_key: password key for this wifi
            :param hidden: indicates if this wifi is hidden
            :param section: normally this would be 'wifi', but if there are multiple wifi sections, they must start
            with 'wifi'
            """
            self.section = section
            cfg_mgr.add_note(section, 'More than one ssid can be specified by adding sections that begin '
                             'with "{}"'.format(PiConfig.WiFi.section))

            self.ssid = cfg_mgr.read_entry(section, PiConfig.WiFi.ssid_tag, ssid)
            self.wifi_key = cfg_mgr.read_entry(section, PiConfig.WiFi.key_tag, wifi_key)
            self.hidden = cfg_mgr.read_entry(section, PiConfig.WiFi.hidden_tag, hidden)
            self.priority = cfg_mgr.read_entry(section, PiConfig.WiFi.priority_tag, priority,
                                               notes='useful if more than one ssid is specified')

    class Miscellaneous:
        section = 'misc'
        host_name_tag = 'host_name'
        location_tag = 'location'
        wifi_country_code_tag = 'wifi_country_code'

        def __init__(self, cfg_mgr, host_name='Pi', wifi_country_code='US', location='Office'):
            """
            WifiConfig defines the data for the wpa_suplicant file
            :param cfg_mgr: the ConfigManager
            :param host_name: name for this host
            :param wifi_country_code: country code for the wifi networks
            :param location: location of this host.  This is a place-holder for other applications to access
            """
            self.host_name = cfg_mgr.read_entry(PiConfig.Miscellaneous.section,
                                                PiConfig.Miscellaneous.host_name_tag, host_name)
            self.wifi_country_code = cfg_mgr.read_entry(PiConfig.Miscellaneous.section,
                                                        PiConfig.Miscellaneous.wifi_country_code_tag,
                                                        wifi_country_code)
            self.location = cfg_mgr.read_entry(PiConfig.Miscellaneous.section,
                                               PiConfig.Miscellaneous.location_tag,
                                               location)

    def __init__(self,
                 file_name='configuration.ini',
                 title=None,
                 default_filename='configuration.ini{}'.format(_default_file_extension)):
        """
        PiConfig extends ThompCoUtils.config_utils.ConfigManager.  It reads the specified file in the root directory
        (when viewed from another OS as an SD card or in the /boot folder when viewed from the pi).  It will create the
        specified default_filename in the boot_folder.  If file_name exists, it will read it and delete it.
        NOTE that this class can only be used on a raspberry pi!
        :param file_name: name of the file to read
        :param title:
        :param default_filename: filename to create if it is not already there
        """
        if not os.path.isdir(PiConfig._boot_folder):
            raise RuntimeError('This can only be used on a Raspberry Pi')
        self.default_filename = os.path.join(PiConfig._boot_folder, default_filename)
        file_name = os.path.join(PiConfig._boot_folder, file_name)
        self.wifi_sections = []
        self.misc = None
        self.read_config = False
        # try to open the actual file first
        if os.path.exists(file_name):
            super().__init__(file_name=file_name, title=title, create=False)
            for section in self.config.sections():
                if section.startswith(PiConfig.WiFi.section):
                    self.wifi_sections.append(PiConfig.WiFi(self, section=section))
            self.misc = PiConfig.Miscellaneous(self)
            # read the file, now delete it
            os.unlink(self.file_name)
            self.read_config = True
        if not os.path.exists(self.default_filename):
            # now write out the sample one
            super().__init__(file_name=self.default_filename, title=title, create=True)
            self.wifi_sections.append(PiConfig.WiFi(self, section='{}_first'.format(PiConfig.WiFi.section),
                                                    ssid='ssid 1', wifi_key='password 1',
                                                    priority=1))
            self.wifi_sections.append(PiConfig.WiFi(self, section='{}_second'.format(PiConfig.WiFi.section),
                                                    ssid='ssid 2', wifi_key='password 2',
                                                    priority=2))
            PiConfig.Miscellaneous(self)

    @staticmethod
    def backup_original_file(file_name):
        original_backup = "{}.original".format(file_name)
        if not os.path.exists(original_backup):
            copyfile(file_name, original_backup)

    def write_wpa_supplicant(self):
        if self.read_config:
            PiConfig.backup_original_file(PiConfig._wpa_supplicant_file)
            f = open(PiConfig._wpa_supplicant_file, 'w')
            f.write('Country={}\n'.format(self.misc.wifi_country_code))
            f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
            f.write('update_config=1\n')
            f.write('\n')
            for section in self.wifi_sections:
                f.write('network = {\n')
                f.write('\tssid = "{}"\n'.format(section.ssid))
                f.write('\tpsk = "{}"\n'.format(section.wifi_key))
                if section.hidden:
                    f.write('\tscan_ssid = 1\n')
                f.write('}\n')
                f.write('\n')
            f.close()

    def write_host_files(self):
        host_ip = '127.0.0.1'
        if self.read_config:
            PiConfig.backup_original_file(PiConfig._host_name_file)
            f = open(PiConfig._host_name_file, 'w')
            f.write('{}\n'.format(self.misc.host_name))
            f.close()
            PiConfig.backup_original_file(PiConfig._hosts_file)
            with open(PiConfig._hosts_file, 'r') as file:
                lines = file.readlines()
            for i in range(0, len(lines)-1):
                if host_ip in lines[i]:
                    lines[i] = '{}\t{}'.format(host_ip, self.misc.host_name)
            with open(PiConfig._hosts_file, 'w') as file:
                file.writelines(lines)

    def write(self, *args, **kwargs):
        """
        This method writes out the default file.
        :param args:
        :param kwargs:
        :return:
        """
        super(PiConfig, self).write(out_file=self.default_filename, stop=False, overwrite=True)
