import sys
import os
import unittest
import logging
import datetime
from shutil import copyfile
from thompcoutils.cron_time import CronTime
from thompcoutils.test_utils import assert_test
from thompcoutils.config_utils import ConfigManager, EmailConnectionConfig, HiLow, PiConfig

test_path = 'test_ini_files'
if not os.path.exists(test_path):
    os.mkdir(test_path)
log_configuration_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_configuration_file)


def test_replace(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    try:
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        # Safely write the changed content, if found in the file
        with open(filename, 'w') as f:
            print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)
    except Exception as e:
        raise e


def test_hi_low_vals(file_name, section, value):
    hi_low = HiLow(file_name=file_name, value_type=float)
    hi_value = value
    places = 10
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(values[HiLow.change_amount_tag] > 1, "value should be large")

    diff = 1
    value -= diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Down, "Should be moving Down")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.hi_tag] == hi_value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.NoChange, "Should not be moving")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.hi_tag] == hi_value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(values[HiLow.change_amount_tag] == 0, "value has not changed")

    diff = 2
    value += diff
    values = hi_low.write_value(entry=section, value=value)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    diff = 1.1
    value += diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    diff = 10.1
    value -= diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Down, "Should be moving Down")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    value = 14
    vals = hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(vals == values, "values should match")


class TestConfigUtils(unittest.TestCase):
    def test_config_mgr(self):
        file_name = os.path.join(test_path, "test_config.ini")
        for write in [True, False]:
            if write:
                if os.path.isfile(file_name):
                    os.remove(file_name)
            else:
                test_replace(file_name, "Rover", "Baily")
            cfg_mgr = ConfigManager(file_name,
                                    "This is the title of the ini file\n"
                                    "You can have multiple lines if you use line breaks", write)
            first = cfg_mgr.read_entry("User 1", "date_time", datetime.datetime.now())
            second = cfg_mgr.read_entry("User 1", "first name", "Joe", "This is the first name")
            last = cfg_mgr.read_entry("User 1", "last name", "Brown", "This is the last name")
            age = cfg_mgr.read_entry("User 1", "age", 12)
            is_male = cfg_mgr.read_entry("User 1", "male", True)
            weight = cfg_mgr.read_entry("User 1", "weight", 23.5)
            values = cfg_mgr.read_entry("User 1", "values", {"height": 7.5, "weight": 10, "name": "Fred"})
            weights = cfg_mgr.read_entry("User 1", "weights", [23.5, 22])
            names = cfg_mgr.read_entry("User 1", "names", ["Joe", "Fred"])
            cfg_mgr.write_entry("User 1", "male", False)
            cfg_mgr.write_entry("User 1", "parent", "Fred")
            cfg_mgr.write_entry("User 1", "date_time", datetime.datetime.now())
            cfg_mgr.write_entry("User 1", "cron_time", CronTime(day_of_month=1, hour=2, minute=3),
                                format_string='%d %H %M')
            # section = cfg_mgr.read_section("user 2", {"first name": "Sally",
            #                                           "last name": "Jones",
            #                                           "age": 15,
            #                                           "is_male": False,
            #                                           "weight": 41.3},
            #                                "You only get to add notes at the top of the section using this method")
            if write:
                test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
                assert_test(test1 == "Rover", "value should be Rover")
            else:
                test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
                assert_test(test1 == "Baily", "value should be Rover")
                test2 = cfg_mgr.read_entry("User 1", "cat name", "Tinkerbell", use_default_if_missing=False)
                assert_test(test2 is None, "missing value should be none")
                val = cfg_mgr.read_entry("User 1", "cron_time", CronTime(day_of_month=1, hour=2, minute=3))
                assert_test(val.day_of_month == 1)
                assert_test(val.day_of_week == 0)
                assert_test(val.month == 0)
                assert_test(val.hour == 2)
                assert_test(val.minute == 3)

            print(first)
            print(second)
            print(last)
            print(age)
            print(is_male)
            print(weight)
            print(values)
            print(weights)
            print(names)
            # print(section)
            if write:
                test_file = file_name
                cfg_mgr.write(out_file=test_file, overwrite=False, stop=False)
                contents = open(test_file, "r")
                print("File contents are:")
                print("====================================================")
                print(contents.read())
                print("====================================================")
                contents.close()

    def test_email_connection_config(self):
        file_name = os.path.join(test_path, "test_email.ini")
        for write in [True, False]:
            if write:
                if os.path.isfile(file_name):
                    os.remove(file_name)
            else:
                pass
            cfg_mgr = ConfigManager(file_name,
                                    "This is the title of the ini file\n"
                                    "You can have multiple lines if you use line breaks", write)
            email_connection = EmailConnectionConfig(cfg_mgr)
            print(email_connection.username)
            print(email_connection.password)
            print(email_connection.from_user)
            print(email_connection.smtp_host)
            print(email_connection.smtp_port)
            if write:
                test_file = file_name
                cfg_mgr.write(out_file=test_file, overwrite=True, stop=False)
                contents = open(test_file, "r")
                print("File contents are:")
                print("====================================================")
                print(contents.read())
                print("====================================================")
                contents.close()

    def test_hi_low(self):
        file_name = os.path.join(test_path, "test_hi_low.ini")
        if os.path.isfile(file_name):
            os.remove(file_name)
        value = 50
        test_hi_low_vals(file_name, "first", value)
        value = 60
        test_hi_low_vals(file_name, "second", value)
        value = 40
        test_hi_low_vals(file_name, "third", value)

    @staticmethod
    def remove_file(f):
        if os.path.exists(f):
            os.unlink(f)

    def test_pi_config(self):
        if sys.platform == 'linux' and os.uname()[4][:3] == 'arm':
            # prep the files
            config_filename = '/tmp/configuration.ini'
            default_config_filename = '{}{}'.format(config_filename, PiConfig._default_file_extension)
            # set the "/boot" folder and wpa_supplicant file for testing on any machine
            PiConfig._boot_folder = "/tmp"
            PiConfig._wpa_supplicant_file = '/tmp/wpa_supplicant.config'
            PiConfig._host_name_file = '/tmp/host'
            PiConfig._hosts_file = '/tmp/hosts'
            # First remove any files from previous testing
            self.remove_file(config_filename)
            self.remove_file(default_config_filename)
            self.remove_file(PiConfig._wpa_supplicant_file)
            self.remove_file(PiConfig._host_name_file)
            self.remove_file(PiConfig._hosts_file)
            copyfile('/etc/hosts', PiConfig._hosts_file)
            f = open(PiConfig._host_name_file, 'w')
            f.write('old_hostname\n')
            f.close()
            f = open(PiConfig._wpa_supplicant_file, 'w')
            f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
            f.write('update_config=1\n')
            f.write('country=US\n')
            f.write('network={\n')
            f.write('\tssid="Your network name/SSID"\n')
            f.write('\tpsk="Your WPA/WPA2 security key"\n')
            f.write('\tkey_mgmt=WPA-PSK\n')
            f.write('}\n')
            f.close()
            # test default values
            assert_test(value=not os.path.exists(default_config_filename), message='{} should not exist'.format(default_config_filename),
                        error='{} should not exist'.format(default_config_filename))
            assert_test(value=not os.path.exists(config_filename), message='{} should not exist'.format(config_filename),
                        error='{} should not exist'.format(config_filename))
            pi_config = PiConfig()
            email_config = EmailConnectionConfig(pi_config)
            for wifi in pi_config.wifi_sections:
                print(wifi.section)
                print(wifi.ssid)
                print(wifi.wifi_key)
                print(wifi.hidden)
            print(email_config.username)
            print(email_config.password)
            # save the default file
            pi_config.write()
            assert_test(value=os.path.exists(default_config_filename), message='testing creation of {}'.format(default_config_filename),
                        error='{} should exist'.format(default_config_filename))
            assert_test(value=not os.path.exists(config_filename), message='testing removal of {}'.format(config_filename),
                        error='{} should not exist'.format(config_filename))
            # fill the test config file
            new_host_name = 'new_host_name'
            new_country_code = 'CA'
            wifi_ssid = 'testing wifi'
            wifi_key = 'testing wifi key'
            f = open(config_filename, 'w')
            f.write('[misc]\n')
            f.write('host_name = {}\n'.format(new_host_name))
            f.write('wifi_country_code = {}\n\n'.format(new_country_code))
            for i in range(1, 3):
                f.write('[wifi_{}]\n'.format(i))
                f.write('ssid = {} {}\n'.format(wifi_ssid, i))
                f.write('key = {} {}\n'.format(wifi_key, i))
                f.write('hidden = {}\n'.format(True if i == 1 else False))
                f.write('priority = {}\n\n'.format(i))
            f.close()
            # read the test config file
            assert_test(value=os.path.exists(default_config_filename), message='{} should exist'.format(default_config_filename),
                        error='{} should exist'.format(default_config_filename))
            pi_config = PiConfig()
            assert_test(pi_config.misc.host_name==new_host_name)
            assert_test(pi_config.misc.wifi_country_code==new_country_code)
            assert_test(value=os.path.exists(default_config_filename), message='testing creation of {}'.format(default_config_filename),
                        error='{} should exist'.format(default_config_filename))
            assert_test(value=not os.path.exists(config_filename), message='testing removal of {}'.format(config_filename),
                        error='{} should not exist'.format(config_filename))
            assert_test(pi_config.misc.host_name == new_host_name)
            for i in range(0, len(pi_config.wifi_sections)):
                section = pi_config.wifi_sections[i]
                if '1' in section.section:
                    section_id = 1
                elif '2' in section.section:
                    section_id = 2
                else:
                    section_id = 3
                assert_test(section.ssid.startswith(wifi_ssid))
                assert_test(section.wifi_key.startswith(wifi_key))
                assert_test(section.hidden == (True if section_id == 1 else False))
                assert_test(section.priority == section_id)
            pi_config.write_wpa_supplicant()
            pi_config.write_host_files()
            # test no actual file but default file exists
            assert_test(value=os.path.exists(default_config_filename), message='{} should exist'.format(default_config_filename),
                        error='{} should exist'.format(default_config_filename))
            assert_test(value=not os.path.exists(config_filename), message='{} should not exist'.format(config_filename),
                        error='{} should not exist'.format(config_filename))
            PiConfig()
            assert_test(value=os.path.exists(default_config_filename), message='testing creation of {}'.format(default_config_filename),
                        error='{} should exist'.format(default_config_filename))
            assert_test(value=not os.path.exists(config_filename), message='testing removal of {}'.format(config_filename),
                        error='{} should not exist'.format(config_filename))
            print('Done')

