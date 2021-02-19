"""Tests for the ps_shell_log."""
import sys

from ps.basic import ps_shell_log

from t_utils import (
    common_Config_class_attributes_after_initialisation,
#    reset_singleton
)
from ps.basic.Config import reset_singleton
SERVICE_NAME = "A_SERVICE_NAME"


def test_ps_1(dev_allowed_stages, capsys):
    """[summary]

    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    sys.argv = [
        "ps_shell_log",
        "-v",
        "--service_name",
        SERVICE_NAME,
        "--level",
        "info",
        "THE MESSAGE",
    ]
    ps_shell_log.main()
    common_Config_class_attributes_after_initialisation(
        dev_allowed_stages, test_service_name=SERVICE_NAME
    )
    captured = capsys.readouterr()
    assert "THE MESSAGE" in captured.err


def test_ps_shell_log_forced_configfile_not_given(dev_allowed_stages, capsys):
    """[summary]

    have_config_file is set to True BUT a config_file is not provided.
    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    :param capsys: [description]
    :type capsys: [type]
    """
    reset_singleton()
    sys.argv = [
        "ps_shell_log",
        "-v",
        "--service_name",
        SERVICE_NAME,
        "--have_config_file",
        "True",
        "THE MESSAGE",
    ]
    ps_shell_log.main()
    common_Config_class_attributes_after_initialisation(
        dev_allowed_stages, test_service_name=SERVICE_NAME
    )
    captured = capsys.readouterr()
    assert "Exception while calling ps_shell_log" in captured.err
