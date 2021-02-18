import cased
import os

from cguard.publisher.publisher import Publisher


class TrailsPublisher(Publisher):
    """
    Publish an event directly to Cased Trails as a backup option
    """

    def __init__(self):
        pass

    def publish(self, action, username, cmd, hostname, external_ip):
        # Credentials
        publish_key = os.environ.get("CASED_PUBLISH_KEY")
        cased.extra_ua_data = "guard-client"
        cased.publish_key = publish_key

        res = cased.Event.publish(
            {
                "action": action,
                "actor": username,
                "command": cmd,
                "hostname": hostname,
                "location": external_ip,
            }
        )

        if res.status_code == 200:
            pass
        else:
            print("failed to send audit event")
            exit(1)
