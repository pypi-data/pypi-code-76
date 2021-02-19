"""Tests for the Config Module."""
import os
import signal
import sys
from configparser import ParsingError

from ps.basic import Config, DEV_STAGES, Patterns

import pytest

from t_utils import (
    TEST_SERVICE_NAME,
    common_Config_class_attributes_after_initialisation,
    get_data_of_file,
#    reset_singleton,
)
from ps.basic.Config import reset_singleton

os.environ["IS_TESTING"] = "YES"

# The fixtures:
#   - dev_allowed_stages
#   - dev_wrong_stages
# are defined in conftest.py


def test_that_an_reinitialization_of_the_singleton_raises_an_error(
    dev_allowed_stages
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        b = Config.Basic(TEST_SERVICE_NAME)  # Should be  OK
        assert b
        Config.Basic(TEST_SERVICE_NAME)  # Will Raise Error


def test_service_names_with_wrong_stage_name_raise_error(dev_wrong_stages):
    """[summary]

    :param dev_wrong_stages: [description]
    :type dev_wrong_stages: [type]
    """
    reset_singleton()
    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        assert Config.service_name == "not_yet_defined"
        Config.Basic(TEST_SERVICE_NAME)


def test_properties_are_set(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.primary_herald_url == ""


#
# verbose mode
#
def test_verbose_mode_with_uninitialized_singleton_raises_error(
    dev_allowed_stages,
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    with pytest.raises(TypeError):
        assert Config.service_name == "not_yet_defined"
        Config.Basic.verbose()


def test_verbose_mode_with_writes_logging_messages_to_stdout_too(
    dev_allowed_stages, capsys
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    singleton = Config.Basic(TEST_SERVICE_NAME)
    singleton.verbose()
    msg = "This is a message"
    Config.logger.info(msg, extra={"package_version": "__version__"})
    captured = capsys.readouterr()
    assert captured.out == ""
    assert msg in captured.err
    assert msg in Config.get_logging_data()


#
# CONFIG FILE THINGS
#
def test_not_existing_config_file_directory_raises_error(dev_allowed_stages,
                                                         capsys
                                                         ):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/foobar"
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        Config.Basic(TEST_SERVICE_NAME, have_config_file=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.config_file_name == "not_yet_defined"
    assert "BASIC_CONFIGFILE_DIR /foobar not found." in Config.get_logging_data() 


def test_config_file_in_local_directory(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    os.environ["BASIC_CONFIGFILE_DIR"] = ""
    del os.environ["BASIC_CONFIGFILE_DIR"]

    config_file_name = os.path.join(
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg"
    )
    with open(config_file_name, "w") as fp:
        fp.write("[test_section]\n")
        fp.write("    test_name = test_value  \n")

    Config.Basic(TEST_SERVICE_NAME, have_config_file=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.primary_herald_url == ""

    assert Config.config_file_name == os.path.join(os.getcwd(),
                                                   config_file_name)
    assert "test_section" in Config.config_parser.sections()
    assert "test_value" == Config.config_parser["test_section"]["test_name"]


def test_config_file_in_local_directory_not_given(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    os.environ["BASIC_CONFIGFILE_DIR"] = ""
    del os.environ["BASIC_CONFIGFILE_DIR"]

    config_file_name = os.path.join(
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg"
    )
    if os.path.isfile(config_file_name):
        os.remove(config_file_name)

    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        Config.Basic(TEST_SERVICE_NAME, have_config_file=True)


def test_config_file_in_directory(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/tmp"
    config_file_name = os.path.join(
        config_file_directory,
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg",
    )
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with open(config_file_name, "w") as fp:
        fp.write("[test_section]\n")
        fp.write("    test_name = test_value  \n")

    Config.Basic(TEST_SERVICE_NAME, have_config_file=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.primary_herald_url == ""

    assert Config.config_file_name == config_file_name
    assert "test_section" in Config.config_parser.sections()
    assert "test_value" == Config.config_parser["test_section"]["test_name"]


def test_wrong_formated_config_files_in_directory_raise_error(
    dev_allowed_stages, capsys
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/tmp"
    config_file_name = os.path.join(
        config_file_directory,
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg",
    )
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with open(config_file_name, "w") as fp:
        fp.write("[Wrong Section Entry\n")
        fp.write("    test_name = test_value  \n")

    with pytest.raises(ParsingError):
        Config.Basic(TEST_SERVICE_NAME, have_config_file=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.primary_herald_url == ""

    assert Config.config_file_name == config_file_name
    assert "MissingSectionHeaderError" in Config.get_logging_data() 


def test_forced_config_file_raises_error_on_impossible_pattern_language(
    dev_allowed_stages, capsys
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/tmp"
    config_file_name = os.path.join(
        config_file_directory,
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg",
    )
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with open(config_file_name, "w") as fp:
        fp.write("[GLOBAL]\n")
        fp.write("    pattern_language = IMPOSSIBLE\n")

    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        Config.Basic(TEST_SERVICE_NAME, have_config_file=True)

    common_Config_class_attributes_after_initialisation(dev_allowed_stages)


def test_forced_config_file_reads_herald_url_and_pattern_language(
    dev_allowed_stages, capsys
):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/tmp"
    config_file_name = os.path.join(
        config_file_directory,
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg",
    )
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with open(config_file_name, "w") as fp:
        fp.write("[GLOBAL]\n")
        fp.write("    herald_url = localhost\n")
        fp.write("    pattern_language = DE\n")

    Config.Basic(
        TEST_SERVICE_NAME,
        have_config_file=True,
        have_herald_url_in_config_file=True,
    )
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert Config.primary_herald_url == "localhost"

    assert Config.config_file_name == config_file_name
    assert "GLOBAL" in Config.config_parser.sections()
    assert "localhost" == Config.config_parser["GLOBAL"]["herald_url"]
    assert "DE" == Config.config_parser["GLOBAL"]["pattern_language"]
    assert "GLOBAL" in Config.get_logging_data()
    assert "herald_url" in Config.get_logging_data()
    assert "localhost" in Config.get_logging_data()


def test_forced_config_file_but_herald_url_is_not_defined(dev_allowed_stages,
                                                          capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    config_file_directory = "/tmp"
    config_file_name = os.path.join(
        config_file_directory,
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg",
    )
    os.environ["BASIC_CONFIGFILE_DIR"] = config_file_directory
    with open(config_file_name, "w") as fp:
        fp.write("[GLOBAL]\n")
        fp.write("    pattern_language = DE\n")
        fp.write("    LOGGING =  INFO\n")

    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        Config.Basic(
            TEST_SERVICE_NAME,
            have_config_file=True,
            have_herald_url_in_config_file=True,
        )
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)

    assert "Value of herald_url" in Config.get_logging_data()
    assert "not given" in Config.get_logging_data() 


#
# SIGHUP HANDLER THINGS
#
def test_sighup_handler_singleton_uninitialized(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    with pytest.raises(Config.ForbiddenInitialisationOfSingleton):
        os.kill(os.getpid(), signal.SIGHUP)


def test_sighup_handler_singleton_initialized(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    os.environ["BASIC_CONFIGFILE_DIR"] = ""
    del os.environ["BASIC_CONFIGFILE_DIR"]

    config_file_name = os.path.join(
        TEST_SERVICE_NAME + DEV_STAGES[dev_allowed_stages]["suffix"] + ".cfg"
    )
    with open(config_file_name, "w") as fp:
        fp.write("[test_section]\n")
        fp.write("    test_name = test_value  \n")
        fp.write("[GLOBAL]\n")
        fp.write("    LOGGING =  DEBUG\n")

    Config.Basic(TEST_SERVICE_NAME, have_config_file=True)
    os.kill(os.getpid(), signal.SIGHUP)
    assert "SIGHUP Received. Print Configuration." in Config.get_logging_data()
    print(Config.get_logging_data())
    print(get_data_of_file(Config.config_file_name))


#
# ps_shell THINGS
#
def test_ps_shell_ls(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    out, err, exit_code, time_needed = Config.ps_shell("ls -a")
    assert "LOG" in out
    assert err == [""]
    assert exit_code == 0
    assert "ls -a" in Config.get_logging_data()


def test_ps_shell_impossible_cmd(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    out, err, exit_code, time_needed = Config.ps_shell("impossible_command")
    assert out == [""]
    assert "impossible_command" in "".join(err)
    assert exit_code != 0
    assert "impossible_command" in Config.get_logging_data()


#
# exec_interpreter THINGS
#
def test_exec_interpreter_from_string(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    out, err, exit_code, time_needed = Config.exec_interpreter_from_string(
        "print('Hello World')"
    )
    assert "Hello World" in out
    assert err == [""]
    assert exit_code == 0
    assert sys.executable in Config.get_logging_data()


#
# template_writer THINGS
#
def test_template_writer(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    text = Config.template_writer(
        Patterns.SUBJECT_PATTERNS,
        "DE",
        "PROD_LOCKED",
        {"snapshot_name": "tralala"},
    )
    assert text == "tralala LOCKED "


def test_template_writer_(dev_allowed_stages):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)

    with pytest.raises(KeyError):
        Config.template_writer(
            Patterns.SUBJECT_PATTERNS,
            "IMPOSSIBLE_KEY",
            "PROD_LOCKED",
            {"snapshot_name": "tralala"},
        )
    assert "unable to generate strin" in Config.get_logging_data()

#
# sebd_email THINGS
#
def test_send_email(dev_allowed_stages):
    reset_singleton()
    Config.Basic(TEST_SERVICE_NAME)
    sender =  "test_env"
    recipients =  ["test@b.de","test2@b.de"]
    subject = "subject" 
    text = "text"
    files=[]
    res = Config.send_a_mail(sender,recipients,subject,text,files,test_only=True)
    print(res)
    assert Config.curr_mail_sender == sender
    assert Config.curr_mail_recipients == recipients 
    assert Config.curr_mail_subject==subject 
    assert Config.curr_mail_text==text
     







