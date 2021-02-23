from typing import List

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio_activity.function import TwilioActivitySingletonFunction
from b_cfn_twilio_activity.twilio_activity import TwilioActivity


class TwilioActivityResource(CustomResource):
    """
    Custom resource used for managing a Twilio workspace for a deployment.

    Creates a workspace on stack creation.
    Updates the workspace on workspace name change.
    Deletes the workspace on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            activity_function: TwilioActivitySingletonFunction,
            activities: List[TwilioActivity]
    ) -> None:
        if len(activities) == 0:
            raise AttributeError('At least one activity must be provided.')

        default_activities_count = len([activity.default for activity in activities if activity.default])
        if default_activities_count != 1:
            raise AttributeError('Exactly one activity must be default in a Workspace.')

        if len(activities) != len(set([activity.friendly_name for activity in activities])):
            raise AttributeError('Two activities can not have the same name.')

        self.__activities = {
            f'{self.__parametrize_name(activity.friendly_name)}Activity': {
                'friendly_name': activity.friendly_name,
                'availability': activity.availability,
                'default': activity.default
            } for activity in activities
        }

        super().__init__(
            scope=scope,
            id=f'CustomResource{activity_function.function_name}',
            service_token=activity_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties=self.__activities
        )

    def get_activity_sid(self, friendly_name: str) -> str:
        return self.get_att_string(f'{self.__parametrize_name(friendly_name)}ActivitySid')

    def __parametrize_name(self, friendly_name: str) -> str:
        return friendly_name.replace(' ', '')
