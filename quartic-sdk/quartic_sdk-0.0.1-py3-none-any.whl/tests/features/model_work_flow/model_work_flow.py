from unittest import mock

from aloe import step, world

from quartic_sdk import APIClient
import pandas as pd

from quartic_sdk.exceptions import InvalidPredictionException
from quartic_sdk.model.tests import SupportedModel, ModelThatReturnsString, SlowModel, ModelThatReturnsList, \
    ModelWithLog, MockLoggingHandler
from quartic_sdk.utilities.test_helpers import APIHelperCallAPI


@step("A Model wrapped in ModelABC and returns predictions output as string")
def step_impl(context):
    world.model = ModelThatReturnsString()


@step("A Model wrapped in ModelABC and sleeps for n seconds before returning the results")
def step_impl(context):
    world.model = SlowModel()


@step("A Quartic SDK APIClient")
def step_impl(context):
    world.client = APIClient("http://test_host", username="username", password="password")


@step("Model save is called with proper parameters")
def step_impl(context):
    try:
        world.raised_exception = None
        world.client.api_helper = mock.Mock()
        world.client.api_helper.call_api = mock.Mock()
        test_df = pd.DataFrame(data={'1': [1], '2': [2], '3': [3]})
        world.model.save(world.client, 'test tag', feature_tags=[1, 2, 3], target_tag=1, test_df=test_df)
    except Exception as e:
        world.raised_exception = e


@step("A Model wrapped in ModelABC and has all proper parameters")
def step_impl(context):
    world.model = SupportedModel()


@step("A Model wrapped in ModelABC and returns prediction output as list")
def step_impl(context):
    world.model = ModelThatReturnsList()


@step("A Model wrapped in ModelABC and returns prediction output as all Null")
def step_impl(context):
    world.model = ModelThatReturnsList()


@step("A Model wrapped in ModelABC with a mock log handler added")
def step_impl(context):
    world.model = ModelWithLog()
    world.handler = MockLoggingHandler()
    world.model.log.addHandler(world.handler)


@step("Model predict is called with logging")
def step_impl(context):
    world.model.predict(pd.DataFrame(data={'1': [1], '2': [2], '3': [3]}))


@step("adds user logs to handler")
def step_impl(context):
    assert len(world.handler.messages['info']) > 0
    assert len(world.handler.messages['error']) > 0
    assert len(world.handler.messages['debug']) == 0  # as default log level is INFO


@step("Raises a InvalidPredictionException")
def step_impl(context):
    assert isinstance(world.raised_exception, InvalidPredictionException)


@step("Returns a None response without exception")
def step_impl(context):
    assert world.raised_exception is None
