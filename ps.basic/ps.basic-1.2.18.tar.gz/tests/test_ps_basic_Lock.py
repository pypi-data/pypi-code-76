"""Test Lock File handling."""
import os

from ps.basic import Config, DEV_STAGES

import pytest


from t_utils import (
    TEST_SERVICE_NAME,
    common_Config_class_attributes_after_initialisation,
    get_data_of_file,
#    reset_singleton,
)
from ps.basic.Config import reset_singleton
os.environ["IS_TESTING"] = "YES"

#
# LOCK FILE THINGS
#


def test_properties_are_set_using_guarded_by_lockfile(
    dev_allowed_stages,
):
    """[summary]

    Lock File does not exist at start.
    :param dev_allowed_stages: [description]
    :type dev_allowed_stages: [type]
    """
    # if dev_allowed_stages == "DEVELOPMENT":
    #     print( f" Skip {dev_allowed_stages}")
    #     return
    # Make sure the lock file is deleted
    lock_filename = os.path.join(os.getcwd(),
                                 "%s_lock%s" %
                                 (TEST_SERVICE_NAME,
                                  DEV_STAGES[dev_allowed_stages]["suffix"]),
                                 )
    print(f"Lockfilename is {lock_filename}")
    if os.path.isfile(lock_filename):
        os.remove(lock_filename)
    reset_singleton()

    Config.Basic(TEST_SERVICE_NAME, guarded_by_lockfile=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    assert "started new lock guarded instance on" in Config.get_logging_data() 
    assert Config.i_have_lock
    assert os.path.isfile(Config.lock_file_name)
    assert str(os.getpid()) in get_data_of_file(Config.lock_file_name)
    # Reset the singleton (but leave the lockfile in the filesystem)
    # The instantiation should raise a
    # Config.LockedInitialisationOfSingleton Exception
    # because the pid is still the same
    assert os.path.isfile(lock_filename)
    reset_singleton()
    assert os.path.isfile(lock_filename)
    # time.sleep(1)
    with pytest.raises(Config.LockedInitialisationOfSingleton):
        Config.Basic(TEST_SERVICE_NAME, guarded_by_lockfile=True)
        print(Config.get_logging_data)
    assert os.getpid() == int(get_data_of_file(Config.lock_file_name))

    # Write a wrong pid into the lock file ==> now the instantiation will
    #  detect, that the service
    # is NOT running:
    #    - remove the lock file
    #    - and  raise a Config.LockedInitialisationOfSingleton exception
    assert os.path.isfile(Config.lock_file_name)
    with open(Config.lock_file_name, "w") as fp:
        fp.write("999999")
        fp.flush()
    reset_singleton(remove_log_file=False)
    with pytest.raises(Config.LockedInitialisationOfSingleton):
        Config.Basic(TEST_SERVICE_NAME, guarded_by_lockfile=True)
    assert "Will Remove the lock fil" in Config.get_logging_data()
    print("The lockFileName is X%sX" % (Config.lock_file_name))
    assert not os.path.isfile(Config.lock_file_name)
    assert not Config.i_have_lock  # ==> False

    # Now the singleton could be used as at the beginning of the test
    reset_singleton(remove_log_file=False)
    Config.Basic(TEST_SERVICE_NAME, guarded_by_lockfile=True)
    common_Config_class_attributes_after_initialisation(dev_allowed_stages)
    print("The 2lockFileName is X%sX" % (Config.lock_file_name))
    assert os.path.isfile(Config.lock_file_name)
    assert str(os.getpid()) in get_data_of_file(Config.lock_file_name)
