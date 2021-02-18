from azureloggerbundle.appInsights.AzureLogWithExtraHandler import AzureLogWithExtraHandler
from loggerbundle.handler.HandlerFactoryInterface import HandlerFactoryInterface

class AppInsightsLogHandlerFactory(HandlerFactoryInterface):

    def __init__(
        self,
        instrumentationKey: str,
    ):
        self.__instrumentationKey = instrumentationKey

    def create(self):
        return AzureLogWithExtraHandler(
            connection_string='InstrumentationKey={}'.format(self.__instrumentationKey)
        )
