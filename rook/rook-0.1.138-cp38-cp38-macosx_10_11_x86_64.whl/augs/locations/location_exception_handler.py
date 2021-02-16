from rook.services.exception_capturing_location_service import ExceptionCapturingLocationService


class LocationExceptionHandler(object):

    NAME = 'exception_handler'

    def __init__(self, arguments, processor_factory):
        pass

    def add_aug(self, trigger_services, output, aug):
        trigger_services.get_service(ExceptionCapturingLocationService.NAME).add_exception_capturing_aug(aug)
