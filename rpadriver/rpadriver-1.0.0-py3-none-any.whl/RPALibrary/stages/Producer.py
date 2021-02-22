"""Base Producer class for RPA using TOS."""
from typing import (
    Generator,
    Tuple,
    Union
)

from robot.api import logger
from robot.api.deco import keyword

from tos.statuses import is_failure, is_skip

from RPALibrary import messages
from RPALibrary.deco import (
    log_number_of_created_task_objects,
    handle_errors
)
from RPALibrary.helpers import (
    get_stage_from_tags,
    handle_dead_selenium,
    handle_signals,
    take_screenshot,
)

from .BaseStage import BaseStage


# TODO: would it be cool to have uniform naming schema with Consumer?
# What if we had pre_action and main_action here too?


class Producer(BaseStage):

    def __init__(self):
        """Remember to super call this constructor if your stage as
        its own ``__init__``: ``super(YourStage, self).__init__()``

        :ivar self.tags: Tags of the current Robot Framework task.
        :ivar self.tos: TOSLibrary instance of the current RF suite.
        :ivar self.error_msg: Library-wide general error message text.
        """
        super(Producer, self).__init__()
        self.data = None  # this will be an iterator

    def preloop_action(self) -> Union[list, tuple, Generator]:
        """
        Prefetch the data for processing. Optional.

        This can return a sequence or a generator. The return value will be
        turned into an list_iterator anyway inside ``main_loop``.
        The iterator will be assigned to self.data.

        Examples:
        * Read all unread messages from inbox into a list
        * Read excel data into Pandas DataSeries and lazily iterate over it.

        :returns: data as a sequence (can be list, tuple) or a generator.
        """
        raise NotImplementedError("Make your own implementation of this if needed")

    @handle_errors()
    def _error_handled_process_data(self) -> Tuple[dict, str, str]:
        """Wrap the user defined process_data with error handling.

        This should always return only one payload item.

        :returns: return value of ``process_data`` and status ("pass" or "fail"),
         and error text as returned from the decorator ``handle_errors``.

        """
        if self.data:
            # If the data was prefetched
            try:
                return self.process_data(item=next(self.data))
            except StopIteration:
                # when no more data to process (as self.data is always an iterator)
                return None
        else:
            # If getting data one item at a time.
            return self.process_data()

    def process_data(self, item=None) -> dict:
        """
        Define how the data is turned into a task object. Required.

        Task objects will be created from the data this method returns.
        It's important to define this with the ``item`` parameter.

        Example: read raw data of one email message to be put into a task object.

        Two use cases:

        * We read excel or inbox contents into a (list) iterator in ``preloop_action``
          → This method will need to get one item from that iterator at a time.

        * We read something one item at a time *here* and want to process them immediately.
          → This method will do the fetching and processing on its own.
          Nothing is fetched into a list before the loop.

        :param item: data item to parse/process.
        :returns payload: payload contents as a dict. ``main_loop`` will
                          automatically put the contents into TOS as a new object
                          document.
        """
        raise NotImplementedError("Make your own implementation of this")

    @handle_errors()
    def _error_handled_postprocess_data(self, to=None) -> dict:
        """
        Wrap postprocessing in error handler. The decorator likes to have
        the task object passed in as a keyword argument.
        """
        return self.postprocess_data(to)

    def postprocess_data(self, to):
        """
        Postprocess already created task object data. Optional.

        Do some post processing on the data, e.g. parse raw email body.
        If this fails, the task object status will change into the corresponding failure.

        Remember that the task object is already created when this step is run.
        """
        return to

    @keyword
    @log_number_of_created_task_objects
    def main_loop(self, *args, **kwargs):
        """
        The main loop for creating new task objects.
        Call this as a Robot Framework keyword, don't redefine yourself.

        Methods called inside ``main_loop``:

        * :meth:`~preloop_action` (optional) prefetches the data, and is the common
          use case (read excel, inbox, etc.)

        * :meth:`~process_data` (required) does some additional work for every item
          that has been read in preloop_action. Task objects are created from the
          return value of :meth:`~process_data`. Note that task objects are always
          created after this step. If you need to filter out some data items, that
          must be done in :meth:`~preloop_action`.

        * Alternatively :meth:`~process_data` can do things on its own. For example,
          poll inbox as long as there are new messages, and for every message
          do some action.

        Example usage:

        .. code-block:: python

            from RPALibrary.stages.Producer import Producer


            class ExampleStage(Producer):
                def preloop_action(self):
                    return ["one", "two", "five"]

                def process_data(self, item=None):
                    mapping = {"one": 1, "two": 2, "five": 3}
                    return {"magic_number": mapping[item]}


        The result will be three task objects with payload values
        ``{"magic_number": 1}``, ``{"magic_number": 2}``, and
        ``{"magic_number": 3}``.

        """
        current_stage = 0
        counter = 0
        try:
            self.data = iter(self.preloop_action())
            # TODO: should we exit early if preloop_action returns empty (iter is always a thing)?
        except NotImplementedError:
            # When preloop_action was not defined, as it
            # is not necessary to first pre-fetch the data
            pass

        while True:
            payload, status, error = self._error_handled_process_data()
            # TODO: investigate if data items should result in task object
            # not being created inside process_data.
            if status == "pass" and not payload:
                # no more input data to process
                break
            counter += 1

            to = self.tos.create_new_task_object(payload or {})
            self.tos.update_stage_object(to["_id"], current_stage)

            if status == "pass":
                updated_to, status, error = self._error_handled_postprocess_data(to=to)
                if status == "pass":
                    self.tos.update_payload(to["_id"], updated_to["payload"])

            if is_failure(status):
                to["last_error"] = error
                to["status"] = status
                self.tos.update_exceptions(to["_id"], current_stage, error)
                self._increment_fail_counter()
                if not kwargs.get("no_screenshots"):  # TODO: Do business exceptions need screenshotting?
                    take_screenshot()
                self.action_on_fail(to)  # TODO: maybe update database here

            elif is_skip(status):
                to["last_error"] = error
                to["status"] = status
                self.tos.update_exceptions(to["_id"], current_stage, error)
                self.action_on_skip(to)

            else:
                self._reset_fail_counter()
            self.tos.update_status(to["_id"], current_stage, status)
            to = self.post_action(to, status)  # TODO: maybe update database here
            self.tos.set_stage_end_time(to["_id"], current_stage)

        self.log_task_objects_in_queue()
        return counter

    def log_task_objects_in_queue(self):
        """
        Log the number of passed task objects in stage 0.
        """
        nr = self._get_number_of_waiting_task_objects()
        logger.info(
            messages.TASK_OBJECTS_IN_QUEUE.format(nr=nr),
            also_console=True
        )

    def _get_number_of_waiting_task_objects(self):
        """
        Get the number of passed task objects in stage 0.
        """
        return self.tos.tos.tos.count_documents({"stage": 0, "status": "pass"})
