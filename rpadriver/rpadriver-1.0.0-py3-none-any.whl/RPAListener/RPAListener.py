"""class for Robot Framework-driven RPA using TOS."""
import sys
from copy import deepcopy

from packaging.version import Version, parse
from robot.api import logger
from robot.api.deco import keyword
from robot.errors import ExecutionFailed, PassExecution, RobotError
from robot.libraries.BuiltIn import BuiltIn
from robot.running import EXECUTION_CONTEXTS as EC
from robot.running.model import TestCase
from RPALibrary.helpers import get_stage_from_tags
from TOSLibrary import TOSLibrary
from TOSLibrary.dynamic_library import DynamicLibrary

from .exceptions import ExceptionRaisers
from .helpers import (
    get_error_handler_from_tags,
    stage_is_transactional,
)


class RPAListener(DynamicLibrary):  # noqa
    """
    RPAListener class is used for automatic handling of task objects to be worked
    by RPA stage definitions that have been defined in Robot Framework script.
    """

    from robot.version import VERSION

    if parse(VERSION) < Version("3.2"):
        logger.error("RPAListener requires Robot Framework version 3.2 or newer")
        sys.exit(-1)

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(
        self,
        db_server,
        db_name,
        db_user=None,
        db_passw=None,
        db_auth_source=None,
        item_variable_name="ITEM",
        item_identifier_field=None,
    ):
        """
        :param db_server: Mongodb server uri and port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str
        :param item_variable_name: The variable name used to refer to task object payload. Defaults to "ITEM".
        :type item_variable_name: str
        :param item_identifier_field: The payload field name used to identify task object in logs. Defaults to "ITEM".
        :type item_identifier_field: str
        """

        super(RPAListener, self).__init__()
        self.ROBOT_LIBRARY_LISTENER = self

        self.item_variable_name = item_variable_name
        self.item_identifier_field = item_identifier_field

        try:
            self.tos = TOSLibrary(
                db_server=db_server, db_name=db_name, db_user=db_user, db_passw=db_passw, db_auth_source=db_auth_source
            )
        except Exception:
            logger.error("TOS connection failed. Check connection details.")
            sys.exit(-1)

        self.current_item = None
        self.add_component(self)
        self.add_component(self.tos)
        self.add_component(ExceptionRaisers())

        self.current_stage = None
        self.skipped_task_objects = []

    @property
    def current_item(self):
        return self.__current_item

    @current_item.setter
    def current_item(self, task_object):
        """Sets two variables to robot scope:
            ${ITEM} is a copy of the work item's payload (dictionary),
            ${ITEM_ID} is the item's MongoDB ObjectId

        By default, ${ITEM} is used as the name of the dictionary variable,
        but this can be overriden upon library import with the ``item_identifier_field`` argument.
        """
        self.__current_item = task_object
        if task_object:
            BuiltIn().set_suite_variable(f"${self.item_variable_name}", task_object.get("payload"))
            BuiltIn().set_suite_variable("$ITEM_ID", str(task_object["_id"]))

    def _start_suite(self, data, result):
        """Initializes the suite (root-level or process stage)

        For transactional stages (`repeat` in test tags), prepares the initial iteration
        by calling ``_prepare_next_task`` and adds setup and teardown keywords for the stage
        if the stage includes them, or if defaults have been set in the robot Settings-table.

        Non-transactional stages are left untouched.
        """

        if data.parent:
            if not data.source == data.parent.source:
                logger.error(
                    "It looks like you are calling robot to run multiple suites. " "This is not supported. Stopping..."
                )
                sys.exit(-1)

        task_template = data.tests[0]
        self.current_stage = get_stage_from_tags(task_template.tags)

        if not data.parent:
            # only run once, for the root suite
            self._prepare_root_suite(data)
        elif stage_is_transactional(task_template):
            if task_template.keywords.setup:
                try:
                    task_template.keywords.setup.run(EC.top)
                except RobotError as e:
                    logger.error(f"Stage setup failed.")
                    data.tests = []
                    raise e

            if task_template.keywords.teardown:
                data.keywords.teardown = task_template.keywords.teardown

            self._prepare_next_task(data.tests.pop(0))

        return

    def _prepare_root_suite(self, root_suite):
        """Prepares the suite definition into a runnable RPA process

        This method does not return anything, instead the root suite is manipulated in place.
        In the resulting suite, each robot task is wrapped into its own child suite.
        The stages are automatically sorted based on their numbering (``stage_n`` tags).

        In order for the listener methods to be called, the listener has to be registered in child suites.
        Currently, this is achieved by taking a deepcopy of the root suite to use as the basis of child suites.
        """

        suite_template = deepcopy(root_suite)
        suite_template.tests = []
        suite_template.keywords = []

        for test in sorted(root_suite.tests, key=lambda test: get_stage_from_tags(test.tags)):
            # TODO: Any other way of extending the listener to the child suites?
            suite_wrapper = deepcopy(suite_template)
            suite_wrapper.name = test.name
            suite_wrapper.tests = [test.deepcopy()]
            root_suite.suites.append(suite_wrapper)

        root_suite.tests.clear()

    def _get_item_id(self, item):
        """Returns the value of the item's identifying field.

        By default, ObjectId is used as the id-field but this can be overriden
        upon library import with the ``item_identifier_field`` argument.
        """

        return item["payload"].get(self.item_identifier_field, None) or str(self.current_item["_id"])

    def _prepare_next_task(self, data: TestCase):
        """Prepares the task iteration for execution

        Sets a new work item to the robot scope and appends the suite with a copy of the current
        robot task if another workable item for the current stage was found in the database.

        Returns True if a task iteration was added and False otherwise.
        """
        self.current_item = self._get_one_task_object(self.current_stage)
        if self.current_item:
            self.tos.update_stage_object(self.current_item["_id"], self.current_stage)
            data.parent.tests.append(RPATask(name=self._get_item_id(self.current_item), task_template=data))
            return True
        else:
            return None

    def _end_test(self, data, result):

        if stage_is_transactional(data) and self.current_item:
            self._update_task_object_stage_and_status(self.current_item["_id"], self.current_stage, result)

        should_exit_stage = False

        if not result.passed:

            should_exit_stage = True
            # TODO: Will future versions of robotframework allow a better way
            #       for inspecting the exception type?
            explicit_error_handler = get_error_handler_from_tags(data.tags)
            if explicit_error_handler:
                BuiltIn().run_keyword_and_ignore_error(explicit_error_handler)

            if "BusinessException" in result.message:
                should_exit_stage = False

        if not should_exit_stage:
            self._prepare_next_task(data)

    def _update_task_object_stage_and_status(self, to_id, current_stage, result):

        new_status = "pass" if result.passed else "fail"

        if not result.passed:
            self.tos.update_exceptions(to_id, current_stage, result.message)

        if to_id not in self.skipped_task_objects:
            self.tos.update_status(to_id, current_stage, new_status)

        self.tos.set_stage_end_time(to_id, current_stage)

    def _get_one_task_object(self, stage=None):
        """
        Gets one work item to be processed by stage with index ``stage``
        """
        if not stage:
            stage = self.current_stage

        getter_args = {
            "statuses": ["pass", "new"],
            "stages": stage - 1,
        }

        return self.tos.find_one_task_object_by_status_and_stage(**getter_args)

    @keyword
    def update_current_item(self, *key_value_pairs, **items):
        """Update the contents of the currently worked item's payload in the database.

        The database document will be upserted with values from the item's payload dictionary at the time of calling.
        Additional variables can be added with the given ``key_value_pairs`` and ``items``.

        Giving items as ``key_value_pairs`` means giving keys and values
        as separate arguments:

        | Set To Dictionary | ${D1} | key | value | second | ${2} |
        =>
        | ${D1} = {'a': 1, 'key': 'value', 'second': 2}

        | Set To Dictionary | ${D1} | key=value | second=${2} |

        The latter syntax is typically more convenient to use, but it has
        a limitation that keys must be strings.

        If given keys already exist in the dictionary, their values are updated.
        """
        dictionary = self.current_item["payload"]

        def set_to_dict():
            if len(key_value_pairs) % 2 != 0:
                raise ValueError(
                    "Adding data to a dictionary failed. There " "should be even number of key-value-pairs."
                )
            for i in range(0, len(key_value_pairs), 2):
                dictionary[key_value_pairs[i]] = key_value_pairs[i + 1]
            dictionary.update(items)
            return dictionary

        self.update_payload(self.current_item["_id"], set_to_dict())
        logger.info(f"'{self.current_item['_id']}' was updated.")
        logger.debug(f"'{self.current_item['_id']}'payload contents after update: {self.current_item['payload']}")

    @keyword
    def run_keyword_and_skip_on_failure(self, name, *args):
        """Runs the keyword and sets task object status to `skip` if failure occurs.

        The keyword to execute and its arguments are specified using `name` and `*args` exactly like with Run Keyword.

        `Skip Task Object` is called conditionally based on the execution result,
        causing rest of the current keyword and task to be skipped in case of failure.

        The error message from the executed keyword is printed to the console andset to the task object's
        exception field.

        Process execution proceeds with the next task object.

        Example:
        | Run Keyword And Skip On Failure | Should Be True | ${invoice_amount} > 0 |
        ...    msg=Invoice is for a zero amount, no action required
        """
        try:
            return BuiltIn().run_keyword(name, *args)
        except ExecutionFailed as err:
            if err.syntax:
                # Keyword was called with wrong number of arguments etc.
                raise err
            # TODO: Should this be changed to use `Skip Task` once in RF 4.0?
            self.skip_task_object(reason=err.message)

    @keyword
    def skip_task_object(self, reason, to_id=None):
        """Sets the task object status to `skip` and skips rest of the current task.

        By default, targets the current task object.
        Object id is persisted in class attribute `skip_task_objects`.
        """
        if not to_id:
            to_id = self.current_item["_id"]
        self.skipped_task_objects.append(to_id)
        self.tos.update_status(to_id, self.current_stage, "skip")
        # TODO: is `last_error` the right place to persist reason for skipping?
        self.tos.update_exceptions(to_id, self.current_stage, reason)
        logger.warn(f"Skipping {to_id}: {reason}")
        raise PassExecution(reason)  # should this be moved inside `skip_task_object`


class RPATask(TestCase):
    """RPATask object is created for each task iteration in a transactional RPA process stage"""

    def __init__(self, name, task_template):
        super().__init__(
            name=str(name),
            doc=task_template.doc,
            tags=task_template.tags,
            timeout=task_template.timeout,
            lineno=task_template.lineno,
        )
        self.keywords = task_template.keywords.normal
        self.tags = task_template.tags
