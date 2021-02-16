import circle
from circle.circle_object import CircleObject
import json
from sns_message_validator2 import (
    InvalidCertURLException,
    InvalidSignatureVersionException,
    SignatureVerificationFailureException,
    SNSMessageValidator,
)


class Notification(CircleObject):
    OBJECT_NAME = "notification"

    # https://developers.circle.com/docs/notifications-on-payments-status-quickstart
    ARN_REGEX = (
        r"arn:aws:sns:us-east-1:908968368384:sandbox_platform-notifications-topic"
    )

    @classmethod
    def construct_from(cls, values, api_key):
        if isinstance(values, str):
            try:
                values = json.loads(values)
            except json.decoder.JSONDecodeError as jde:
                # TODO: logging
                raise jde
            except Exception as e:
                raise e
        elif isinstance(values, dict):
            pass
        else:
            raise Exception(f"Invalid type for values, {type(values)}")

        # SNS Validation
        sns_message_validator = SNSMessageValidator()
        try:
            sns_message_validator.validate_message(values)

        # TODO: Exception wrapping and logging
        except InvalidCertURLException as e:
            raise e
        except InvalidSignatureVersionException as e:
            raise e
        except SignatureVerificationFailureException as e:
            raise e
        except Exception as e:
            raise e

        # Execute the super construct_from
        return super().construct_from(values, api_key)

    def construct_message(self, api_key=None):
        return circle.Message.construct_from(json.loads(self.Message), api_key)
