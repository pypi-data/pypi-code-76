from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration

from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioActivitySingletonFunction(SingletonFunction):
    """
    Custom activity resource Singleton Lambda function.

    Creates activities on stack creation.
    Updates activities on their name changes.
    Deletes activities on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid=f'{name}-uuid',
            function_name=name,
            code=self.__code(),
            layers=[TwilioLayer(scope, f'TwilioLayerFor{name}')],
            timeout=Duration.minutes(1),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
            environment={
                'TWILIO_ACCOUNT_SID': twilio_account_sid,
                'TWILIO_AUTH_TOKEN': twilio_auth_token,
                'TWILIO_WORKSPACE_SID': twilio_workspace_sid
            }
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
