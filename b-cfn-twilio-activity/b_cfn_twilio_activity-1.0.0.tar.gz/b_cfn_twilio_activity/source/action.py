import base64
import json
import logging
import os
from typing import Dict, Any, Optional, Tuple, List

from twilio.base.exceptions import TwilioException
from twilio.rest import Client
from twilio.rest.taskrouter.v1.workspace import WorkspaceContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Action:
    def __init__(self, invocation_event: Dict[str, Any]):
        self.__invocation_event: Dict[str, Any] = invocation_event
        self.__parameters: Dict[str, Any] = invocation_event['ResourceProperties']
        self.__resource_id: Optional[str] = invocation_event.get('PhysicalResourceId')

        try:
            self.TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
            self.TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
            self.TWILIO_WORKSPACE_SID = os.environ['TWILIO_WORKSPACE_SID']
        except KeyError as ex:
            logger.error(f'Missing environment: {repr(ex)}.')
            raise

        self.__activities = {
            key: value
            for key, value in self.__parameters.items()
            if key.endswith('Activity')
        }

        self.client = self.__get_twilio_client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)

    def create(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Creates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource creation with these parameters: {json.dumps(self.__parameters)}.')

        workspace = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID)

        # Find activities created by default.
        created_activities = {
            'OfflineActivity': workspace.activities.list(friendly_name='Offline')[0],
            'AvailableActivity': workspace.activities.list(friendly_name='Available')[0],
            'UnavailableActivity': workspace.activities.list(friendly_name='Unavailable')[0],
        }

        # It is safe to assume that this value will always be set in the following loop, since the resource requires exactly one activity to be default.
        default_activity_sid = None

        # Create new activities.
        for key, activity in self.__activities.items():
            if not created_activities.get(key):
                created_activities[key] = workspace.activities.create(
                    friendly_name=activity['friendly_name'],
                    available=activity['availability'],
                )

            if activity['default']:
                default_activity_sid = created_activities[key].sid

        # Set the default activity.
        workspace.update(
            default_activity_sid=default_activity_sid,
            timeout_activity_sid=default_activity_sid
        )

        # Prepare unused default activities for deletion.
        delete_keys: List[Tuple[str, str]] = []
        for key, activity in created_activities.items():
            if not self.__activities.get(key):
                delete_keys.append((key, activity.sid))

        # Delete unused default activities.
        for key, activity_sid in delete_keys:
            created_activities.pop(key)
            self.__force_delete_activity(workspace, activity_sid, default_activity_sid)

        activity_sids = {
            f'{parameter_name}Sid': activity.sid for parameter_name, activity in created_activities.items()
        }

        return activity_sids, base64.b64encode(json.dumps(activity_sids).encode('utf-8')).decode('utf-8')

    def update(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Updates a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource update with these parameters: {json.dumps(self.__parameters)}.')

        activity_sids: Dict[str, str] = json.loads(base64.b64decode(self.__resource_id))
        workspace = self.client.taskrouter.workspaces.get(self.TWILIO_WORKSPACE_SID)

        # It is safe to assume that this value will always be set in the following loop, since the resource requires exactly one activity to be default.
        default_activity_sid = None

        # Create newly added activities.
        for activity_key, activity in self.__activities.items():
            activity_sid_key = f'{activity_key}Sid'
            if not activity_sids.get(activity_sid_key):
                activity_sids[activity_sid_key] = workspace.activities.create(
                    friendly_name=activity['friendly_name'],
                    available=activity['availability'],
                ).sid

            if activity['default']:
                default_activity_sid = activity_sids[activity_sid_key]

        # Update default activity.
        workspace.update(
            default_activity_sid=default_activity_sid,
            timeout_activity_sid=default_activity_sid
        )

        # Prepare removed activities for deletion.
        delete_keys: List[Tuple[str, str]] = []
        for activity_sid_key, activity_sid in activity_sids.items():
            activity_key = activity_sid_key[0:-3]  # Remove Sid prefix from the key, to access locally stored activities.
            if not self.__activities.get(activity_key):
                delete_keys.append((activity_sid_key, activity_sid))

        # Delete removed activities.
        for key, activity_sid in delete_keys:
            activity_sids.pop(key)
            self.__force_delete_activity(workspace, activity_sid, default_activity_sid)

        return activity_sids, base64.b64encode(json.dumps(activity_sids).encode('utf-8')).decode('utf-8')

    def delete(self) -> Tuple[Optional[Dict[Any, Any]], Optional[str]]:
        """
        Deletes a resource.

        :return: A tuple containing two items:
            1. Custom data to return back to CloudFormation service.
            2. Physical resource id (can be empty).
        """
        logger.info(f'Initiating resource deletion with these parameters: {json.dumps(self.__parameters)}.')

        activity_sids: Dict[str, str] = json.loads(base64.b64decode(self.__resource_id))

        # It is not worth deleting activities, since destroying a workspace will delete them anyways.

        return activity_sids, base64.b64encode(json.dumps(activity_sids).encode('utf-8')).decode('utf-8')

    def __force_delete_activity(self, workspace: WorkspaceContext, activity_sid: str, default_activity_sid: str) -> None:
        for worker in workspace.workers.list(activity_sid=activity_sid):
            worker.update(activity_sid=default_activity_sid)

        workspace.activities(sid=activity_sid).delete()

    @staticmethod
    def __get_twilio_client(account_sid: str, auth_token: str) -> Client:
        """
        Creates a Twilio Client.

        :return: Twilio Client.
        """
        try:
            return Client(username=account_sid, password=auth_token)
        except TwilioException as ex:
            logger.error(f'Could not create Twilio client. Reason: {repr(ex)}.')
            raise
