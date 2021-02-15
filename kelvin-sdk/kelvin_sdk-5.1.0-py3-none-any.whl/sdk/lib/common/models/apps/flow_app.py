from pydantic import Extra

from kelvin.sdk.lib.common.models.generic import KSDKModel


class FlowAppType(KSDKModel):
    pass

    class Config:
        extra = Extra.allow
