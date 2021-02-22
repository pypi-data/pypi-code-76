"""Base Consumer class for RPA using TOS."""
import warnings

from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from tos.statuses import is_failure, is_skip

from RPALibrary.deco import log_number_of_created_task_objects, handle_errors
from RPALibrary.helpers import (
    get_stage_from_tags,
    handle_dead_selenium,
    handle_signals,
    take_screenshot,
)
from .BaseStage import BaseStage


class Consumer(BaseStage):
    """
    Consumer base definition. Inherit your own consumer stage from this.

    Every inheriting library must have a method
    ``main_action`` which defines the steps to be done for every
    task object in the current stage. To run the actions,
    call ``main_loop`` defined here (override only when necessary).

    Usage example:

    .. code-block:: python

        from RPALibrary.stages import Consumer

        class PDFMerger(Consumer):

            def __init__(self):
                '''
                Remember to call ``super`` in the constructor.
                '''
                super(PDFMerger, self).__init__()
                self.merger = PdfFileMerger()

            @keyword
            def merge_all_pdfs(self, filename):
                '''
                Get every valid task object from the DB
                and do the action defined in ``main_action``.
                Exceptions are handled and logged appropriately.
                '''
                count = self.main_loop(current_stage=4)
                if count:
                    write_merged_pdf_object(filename)

            def main_action(self, to):
                '''Append pdf as bytes to the pdf merger object.'''
                pdf_bytes = io.BytesIO(to["payload"]["pdf_letter"])
                self.merger.append(pdf_bytes)

    And the corresponding Robot Framework script:

    .. code-block:: python

        *** Settings ***
        Library                 PDFMerger

        *** Tasks ***
        Manipulate PDF files
            Merge All PDFs      combined.pdf

    """

    def __init__(self):
        """Remember to super call this constructor if your stage as
        its own ``__init__``: ``super(YourStage, self).__init__()``

        :ivar self.tags: Tags of the current Robot Framework task.
        :ivar self.tos: TOSLibrary instance of the current RF suite.
        :ivar self.error_msg: Library-wide general error message text.
        :ivar self.stop_after_limit: If set, looping will stop after this many task objects.
        :ivar self.should_stop_reason: If set, looping will stop.
        """
        super(Consumer, self).__init__()
        self.stop_after_limit = None
        self.should_stop_reason = None

    @keyword
    @log_number_of_created_task_objects
    def main_loop(self, *args, **kwargs):
        """
        The main loop for processing task objects on a given stage.

        Get task objects ready for processing and do the actions
        as defined in method :meth:`~main_action`. Continue doing this as
        long as valid task objects are returned from the DB. The counter
        value must be returned for logger decorator consumption.

        Using this method/keyword gives you automatic logging and looping
        over valid task objects. You can override this method to suit
        your specific needs.

        Remember to explicitly call this from Robot Framework.

        :param kwargs:

            - **stage** (`int` or `str`) - the current stage where this is called from.
              If this is not given, the stage is inferred from the Robot Framework
              task level tag.

            - **status** (`str`) - the status of the task objects to process
              (default is 'pass')

            - **change_status** (`bool`) - decide if the status should be changed after
              main_action or kept as the original (default is `True`).

            - **error_msg** (`str`) - Custom error message if the action here fails
              (optional).

            - **getter** (`callable`) - the method which is used to get the data to process.
              This might be a custom input data fetcher. By default it is
              ``find_one_task_object_by_status_and_stage``.
              Note that using a custom getter is considered experimental. Custom getter could be, e.g.
              ``collection.find_one_and_update``. Very important to update the object
              state in the same operation- otherwise ``main_loop`` will loop infinitely!
              *This functionality will be deprecated in the future*.

            - **getter_args** (`dict`)- arguments that should be passed to the custom
              getter. By default the arguments are ``{"statuses": status, "stages": previous_stage}``.
              Note that they must be given as a dict, where the keys are the argument names, eg.
              ``{"filter": {"payload.age": "older"}}`` when the getter signature is
              ``find_one_and_update(filter=None, update=None)``.

            - **amend** (`dict`) - additional MongoDB query to be used
              for filtering task objects (optional).

            - **main_keyword** (`str`) - custom method name to use in place of `main_action`
              (optional).

            - **sort_condition** (`str`) - custom condition to be used in sorting
              the task objects, e.g. `sort_condition=[("_id", pymongo.DESCENDING)]`
              (optional).

        :returns: number of task objects processed
        :rtype: int
        :ivar new_status: the new status returned from the :meth:`~RPALibrary.deco.handle_errors`
                          decorator.
        :type new_status: str
        """
        def _get_stages():
            current_stage = kwargs.get("current_stage")
            if current_stage is None:
                current_stage = get_stage_from_tags(self.tags)
            else:  # 0 is a valid case
                current_stage = int(current_stage)
            previous_stage = current_stage - 1
            return current_stage, previous_stage

        def _get_target_status():
            return kwargs.get("status", "pass")

        def _get_getter_and_args(status, previous_stage):
            """
            Be careful when using a custom getter.

            * Its arguments must be passed in as a dict.
            * The objects state should change, otherwise there will be infinite loop!
            """
            default_getter_args = {
                "statuses": status,
                "stages": previous_stage,
                "amend": kwargs.get("amend", ""),
                "sort_condition": kwargs.get("sort_condition", "")
            }
            getter_args = kwargs.get("getter_args", default_getter_args)
            if kwargs.get("getter"):
                # IMPORTANT: make sure this changes the object state!
                warnings.warn("Use a custom getter at your own risk", DeprecationWarning)
                getter = kwargs.get("getter")
            else:
                getter = self.tos.find_one_task_object_by_status_and_stage  # this changes status to processing
            return getter, getter_args

        self.error_msg = kwargs.get("error_msg", self.error_msg)  # Used inside the decorator. Could we scrap this?

        current_stage, previous_stage = _get_stages()
        status = _get_target_status()

        getter, getter_args = _get_getter_and_args(status, previous_stage)

        # TODO: clean this mess of a loop
        counter = 0
        while True:
            to = getter(**getter_args)  # Be very careful when using a custom getter
            if not to:
                break
            counter += 1

            logger.info(f"\n[ INFO ] Handling task object {to['_id']}", also_console=True)

            self.tos.update_stage_object(to["_id"], current_stage)
            self.tos.save_retry_metadata_if_retry(to, current_stage)
            _, new_status, error = self._error_handled_pre_and_main_action(to=to, *args, **kwargs)
            if kwargs.get("change_status", True):
                self.tos.update_status(to["_id"], current_stage, new_status)
            else:
                # change back to the original status from 'processing'
                # FIXME: is this if block ever needed?
                self.tos.update_status(to["_id"], current_stage, status)

            if is_failure(new_status):
                to["last_error"] = error
                to["status"] = new_status
                self.tos.update_exceptions(to["_id"], current_stage, error)
                self._increment_fail_counter()
                if not kwargs.get("no_screenshots"):
                    take_screenshot()
                to = self._predefined_action_on_fail(to)  # TODO: maybe update database here
                self.action_on_fail(to)  # the process might be killed here
            elif is_skip(new_status):
                to["last_error"] = error
                to["status"] = new_status
                self.tos.update_exceptions(to["_id"], current_stage, error)
                self.action_on_skip(to)
            else:
                self._reset_fail_counter()

            to = self.post_action(to, new_status)  # TODO: maybe update database here
            self.tos.set_stage_end_time(to["_id"], current_stage)

            if self.stop_after_limit and counter >= self.stop_after_limit:
                self.should_stop_reason = f"Already processed {counter} task objects."

            if self.should_stop_reason:
                logger.warn(f"Process should stop: {self.should_stop_reason}")
                break

        return counter

    @handle_errors()
    def _error_handled_pre_and_main_action(self, to=None, **kwargs):
        """Wrap the user defined main action with error handling.

        Firstly `pre_action` is called and so it is included in the
        error handling.

        It is important that the task object ``to`` is passed
        as a keyword argument to this method. It allows the decorator
        to consume the task object data.

        :param to: task object
        :type to: dict
        :param kwargs:
            - **main_keyword** (`str`) -  Name of the keyword that should be
              used as the ``main_action``

        :returns: return value of ``main_action`` and status ("pass" or "fail")
         as returned from the decorator ``handle_errors``.
        :rtype: `tuple`
        """
        handle_signals()
        # handle_dead_selenium()  # FIXME: this creates problems, investigate!
        to = self.pre_action(to)
        main_keyword = kwargs.get("main_keyword")

        if main_keyword:
            return BuiltIn().run_keyword(main_keyword, to)

        return self.main_action(to)
