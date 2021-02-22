import pytest
from unittest import TestCase

from symbiotic.devices import LightBulb
from symbiotic.services import BaseService, ServiceResponse

SERVICE_CALL_SUCCESS = 'mock-success-call'
SERVICE_CALL_FAIL = 'mock-fail-call'


###########################################
#  ______ _      _
# |  ____(_)    | |
# | |__   ___  _| |_ _   _ _ __ ___  ___
# |  __| | \ \/ / __| | | | '__/ _ \/ __|
# | |    | |>  <| |_| |_| | | |  __/\__ \
# |_|    |_/_/\_\\__|\__,_|_|  \___||___/
###########################################


@pytest.fixture(scope='function')
def service_success(request) -> BaseService:
    class ServiceSuccess(BaseService):
        def trigger(self, *args, **kwargs):
            return ServiceResponse(
                success=True,
                message=SERVICE_CALL_SUCCESS,
            )

    request.cls.service = ServiceSuccess()


@pytest.fixture(scope='function')
def service_fail(request) -> BaseService:
    class ServiceFail(BaseService):
        def trigger(self, *args, **kwargs):
            return ServiceResponse(
                success=False,
                message=SERVICE_CALL_FAIL,
            )

    request.cls.service = ServiceFail()


#############################
#   _______        _
#  |__   __|      | |
#     | | ___  ___| |_ ___
#     | |/ _ \/ __| __/ __|
#     | |  __/\__ \ |_\__ \
#     |_|\___||___/\__|___/
#############################


@pytest.mark.usefixtures('service_success')
class Test_Unit_LightBulb(TestCase):
    def test_create_light_bulb(self) -> None:
        light_bulb = LightBulb('room', service=self.service)
        self.assertIsNotNone(light_bulb)
        self.assertEqual(type(light_bulb), LightBulb)


@pytest.mark.usefixtures('service_success')
class Test_Integration_LightBulb_Success(TestCase):

    def test_light_bulb_turn_on_success(self) -> None:
        light_bulb = LightBulb('room', service=self.service)
        response = light_bulb.turn_on()
        self.assertTrue(response.success)
        self.assertEqual(response.message, SERVICE_CALL_SUCCESS)

    def test_light_bulb_turn_off_success(self) -> None:
        light_bulb = LightBulb('room', service=self.service)
        response = light_bulb.turn_off()
        self.assertTrue(response.success)
        self.assertEqual(response.message, SERVICE_CALL_SUCCESS)


@pytest.mark.usefixtures('service_fail')
class Test_Integration_LightBulb_Fail(TestCase):

    def test_light_bulb_turn_off_fail(self) -> None:
        light_bulb = LightBulb('room', service=self.service)
        response = light_bulb.turn_off()
        self.assertFalse(response.success)
        self.assertEqual(response.message, SERVICE_CALL_FAIL)

    def test_light_bulb_turn_on_fail(self) -> None:
        light_bulb = LightBulb('room', service=self.service)
        response = light_bulb.turn_on()
        self.assertFalse(response.success)
        self.assertEqual(response.message, SERVICE_CALL_FAIL)
