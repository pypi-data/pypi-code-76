from typing import List
from box import Box
from injecta.dtype.DType import DType
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias
from injecta.service.argument.PrimitiveArgument import PrimitiveArgument
from pyfonybundles.Bundle import Bundle

class AzureLoggerBundle(Bundle):

    def modifyServices(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box): # pylint: disable = unused-argument
        if parameters.azureloggerbundle.enabled:
            service = Service(
                'azureloggerbundle.appInsights.AppInsightsLogHandlerFactory',
                DType('azureloggerbundle.appInsights.AppInsightsLogHandlerFactory', 'AppInsightsLogHandlerFactory'),
                [
                    PrimitiveArgument('%azureloggerbundle.appInsights.instrumentationKey%')
                ],
                ['loghandler.factory']
            )

            services.append(service)

        return services, aliases
