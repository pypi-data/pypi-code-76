from django.conf import settings
from django.contrib.sites.models import Site

from kitchenart import _logger
from kitchenart.log.publisher import LogPublisher
from kitchenart.utils.broker import EventType


def publish_activity_log(sender, user, event, entity, instance_old, instance_new, **kwargs):
    actor = f'{user.get_full_name()} <{user.email}>'
    description = None
    entity_name = entity.replace('_', ' ')
    if event == EventType.created:
        description = f'Create new {entity_name}: {instance_new}'
    elif event == EventType.changed:
        description = f'Update {entity_name}: {instance_new}'
    elif event == EventType.deleted:
        description = f'Delete {entity_name}: {instance_old}'

    try:
        exchange_name = settings.LOG_EXCHANGE
        publisher = LogPublisher(exchange_name, site=Site.objects.get_current())
        publisher.publish(
            actor=actor,
            event=event,
            entity=entity,
            desc=description,
            instance_old=instance_old,
            instance_new=instance_new
        )
    except Exception as exc:
        _logger.exception(f"AMQP error log publish {entity}: {exc}")
