"""Base stage class for RPA using TOS."""
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class BaseStage:
    """
    RPA Library base class to be used for writing Robot Framework / Python
    stage definitions using TOSLibrary.

    This class is inherited by Consumer and Producer. These classes contain
    error handling, logging, and TOS interaction,
    so users don't have to write them manually every time they write
    new stages.
    """

    def __init__(self):
        """Remember to call this constructor when inheriting.

        See the example in the :class:`~TOSLibrary.RPALibrary.RPALibrary`
        class docstring above.

        :ivar self.tags: Tags of the current Robot Framework task.
        :ivar self.tos: TOSLibrary instance of the current RF suite.
        :ivar self.error_msg: Library-wide general error message text.
        """
        super(BaseStage, self).__init__()
        self.tags = BuiltIn().get_variable_value("@{TEST TAGS}")
        self.tos = BuiltIn().get_library_instance("TOSLibrary")
        self.consecutive_failures = 0
        self.error_msg = ""

    def main_action(self, to):
        """
        The main action to do.

        You should make the implementation yourself.
        This will be called in the ``main_loop`` and should
        contain all the steps that should be done with the
        data stored in one task object.

        Don't call this from Robot Framework, call ``main_loop`` instead.

        :param to: task object
        :type to: dict
        """
        raise NotImplementedError("Make your own implementation of this method")

    def post_action(self, to, status, *args, **kwargs):
        """Teardown steps.

        Action to do for every task object after
        the main action has completed succesfully or failed.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        :param status: status returned from running ``handle_errors`` decorated
                       ``main_action``.
        :type status: str
        """
        return to

    def _predefined_action_on_fail(self, to):
        """Call error handler plugins here automatically."""
        logger.debug("Predefined action on fail not yet implemented")
        # TODO: reimplemenet error handler plugin system
        return to

    def action_on_fail(self, to):
        """Custom action to do when an error is encountered.

        This is always called after automatic error handlers
        have done their job. You can define here some custom
        action or some steps that should be always run after
        every error handler.

        E.g. fail the robot immediately with keyword "Fail".

        Note that these actions are not error handled, all exceptions
        will be propagated until Robot Framework stops execution with
        failure.
        """
        pass

    def action_on_skip(self, to):
        """Custom action to do when special skip exception
        is encountered.

        Note that this functionality is identical to the
        action_on_fail except that this handler will be called
        instead when SkipProcessing exception is raised. Use
        this method to differentiate handling if needed.
        """
        pass

    def pre_action(self, to):
        """Setup steps.

        Action to do for every task object before the error
        handled main action.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        """
        return to

    def _increment_fail_counter(self):
        self.consecutive_failures += 1

    def _reset_fail_counter(self):
        """Call this when the whole workflow has completed succesfully
        for one task object.

        This resets the consecutive failure counter.
        """
        self.consecutive_failures = 0
