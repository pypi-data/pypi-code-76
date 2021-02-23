import msgpack
from django.utils.timezone import now

from kitchenart.utils.broker import BasicPublisher, EventType


class LogPublisher(BasicPublisher):
    def construct_message(self,
                          actor: str,
                          entity: str,
                          event: EventType,
                          desc: str,
                          data_old: dict =None,
                          data_new: dict =None) -> bytes:
        """ Construct the message to be sent.
        """
        message = {
            "event_time": now().isoformat(),
            "actor": actor,
            "event": event.value,
            "entity": entity,
            "description": desc,
            "data_old": data_old,
            "data_new": data_new
        }
        return msgpack.packb(message, use_bin_type=True)

    def publish(self,
                actor: str,
                event: EventType,
                entity: str,
                desc: str,
                instance_old: any =None,
                instance_new: any =None) -> None:

        body = self.construct_message(
            actor=actor,
            entity=entity,
            event=event,
            desc=desc,
            data_old=instance_old,
            data_new=instance_new
        )

        routing_key = f'log.{entity}.{event.value}'
        self._publish(body, routing_key)
