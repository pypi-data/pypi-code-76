import os
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Notification:
    """A notification that can be sent to the specified email addresses.  Send the notification using the `send()` method

    :param include_creator[bool]: Should the creator of the batch be emailed
    :param to[List(str)]: An optional list of emails to send the notification to (default=[])
    :param cc[List(str)]: An optional list of users to cc the email to (default=[])
    :param bcc[List(str)]: An optional list of users to bcc the email to (default=[])
    :param subject[str]: The subject of the email
    :param template[str]: An absolute file path or a string that will be rendered with context to form the message of the email
    """

    include_creator: bool = False
    to: List[str] = field(default_factory=list)
    subject: str = ""
    template: str = ""
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)

    def get_context(self, *args):
        """
        Hook for specifying context for a given notification
        """
        return {}

    def validate(self):
        """
        Validates the notification
        :return: True
        :raises: ValidationError
        """
        from qalx_orcaflex.data_models import ValidationError

        if not self.include_creator and not self.to:
            raise ValidationError(
                "Must specify either `include_creator` or `to` parameters"
            )
        return True

    def to_valid_dict(self):
        """
        Ensures the notification is valid before returning the notification as a dict
        """
        if self.validate():
            return asdict(self)

    def _get_template(self):
        """
        Constructs the template string, will first attempt to load the template from a file, and will
        then fall back to returning the template string directly
        """
        if os.path.exists(self.template):
            with open(self.template, "r") as f:
                template = f.read()
            return template
        return self.template

    def _render_message(self, context):
        """
        Takes the template and attempts to replace all instances of `{<context key}` with the context value
        :param context: A dict of context to populate the template with
        :type context: dict
        """
        template = self._get_template()
        for key, value in context.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template

    def _valid_to_address(self, entity):
        """
        Validates the `to` address and raises an exception if not valid.  The `to` address can be a combination
        of the `to` address given at init and also the `email` of the creating user if `self.include_creator` is True
        """
        # Safety net to make sure a user can't send without specifying a to address
        self.validate()
        created_by = entity["info"]["created"]["by"].get("email")
        if self.include_creator is True:
            if created_by:
                # A user created this entity
                self.to.append(created_by)
            else:
                # A bot created this entity.  Try and fall back to cc, then bcc if possible
                self.to = self.cc or self.bcc
        return self.to

    def send(self, entity, session, extra_context=None):
        """
        Sends the notification to the API.
        :param entity:The entity that should be used when building the template
        :type entity: QalxEntity
        :param session:An instance of QalxOrcaFlex
        :type session: QalxOrcaFlex
        :param extra_context:An optional dict of extra context to use in the
        notification
        :type extra_context: dict
        """
        context = self.get_context(entity)
        if extra_context is not None:
            context.update(extra_context)
        message = self._render_message(context)

        to = self._valid_to_address(entity)
        if to:
            session.notification.add(
                subject=self.subject, message=message, to=to, cc=self.cc, bcc=self.bcc
            )
        else:
            # We tried our best to figure out a `to` address, but we couldn't.  This could be because
            # include_creator was True, there was no cc and bcc and the entity was created by a bot
            session.log.warning(
                f"Attempted to send email but couldn't due"
                f" to no `to` address. Entity guid `{entity.guid}`. Notification `{self.__class__.__name__}`"
            )


@dataclass
class NotificationSubmitted(Notification):
    """A notification that can be sent when a batch has been submitted.  Send the notification using the `send()` method

    :param include_creator[bool]: Should the creator of the batch be emailed
    :param to[List(str)]: An optional list of emails to send the notification to (default=[])
    :param cc[List(str)]: An optional list of users to cc the email to (default=[])
    :param bcc[List(str)]: An optional list of users to bcc the email to (default=[])
    :param subject[str]: The subject of the email
    :param template[str]: An absolute file path or a string that will be rendered with context to form the message of the email
    """

    subject: str = "submitted notification subject"
    template: str = os.path.join(
        os.path.dirname(__file__), "templates", "notification_submitted.html"
    )

    def get_context(self, entity):
        """
        Constructs the context to be used for sending the notification for the given entity
        :param entity: The entity that will be used to construct the context
        """
        context = super(NotificationSubmitted, self).get_context(entity)
        created_by = entity["info"]["created"]["by"]
        context.update(
            {
                "batch_name": entity.meta.name,
                "batch_queue_name": entity.meta.options.batch_queue,
                "batch_guid": entity.guid,
                "number_of_jobs": len(entity["sets"]),
                "created_by": created_by.get("email", str(created_by["guid"])),
            }
        )
        return context


@dataclass
class NotificationCompleted(Notification):
    """A notification that can be sent when a batch has been completed.  Send the notification using the `send()` method

    :param include_creator[bool]: Should the creator of the batch be emailed
    :param to[List(str)]: An optional list of emails to send the notification to (default=[])
    :param cc[List(str)]: An optional list of users to cc the email to (default=[])
    :param bcc[List(str)]: An optional list of users to bcc the email to (default=[])
    :param subject[str]: The subject of the email
    :param template[str]: An absolute file path or a string that will be rendered with context to form the message of the email
    """

    subject: str = "completion notification subject"
    template: str = os.path.join(
        os.path.dirname(__file__), "templates", "notification_completed.html"
    )

    def get_context(self, entity):
        """
        Constructs the context to be used for sending the notification for the given entity
        :param entity: The entity that will be used to construct the context
        """
        context = super(NotificationCompleted, self).get_context(entity)
        created_by = entity["info"]["created"]["by"]
        context.update(
            {
                "batch_name": entity.meta.name,
                "batch_guid": entity.guid,
                "number_of_jobs": len(entity["sets"]),
                "created_by": created_by.get("email", str(created_by["guid"])),
            }
        )
        return context


@dataclass
class NotificationTimedOut(Notification):
    """A notification that can be sent when a batch has timed out.  Send the notification using the `send()` method

    :param include_creator[bool]: Should the creator of the batch be emailed
    :param to[List(str)]: An optional list of emails to send the notification to (default=[])
    :param cc[List(str)]: An optional list of users to cc the email to (default=[])
    :param bcc[List(str)]: An optional list of users to bcc the email to (default=[])
    :param subject[str]: The subject of the email
    :param template[str]: An absolute file path or a string that will be rendered with context to form the message of the email
    """

    subject: str = "timed out subject"
    template: str = os.path.join(
        os.path.dirname(__file__), "templates", "notification_timed_out.html"
    )

    def get_context(self, entity):
        """
        Constructs the context to be used for sending the notification for the given entity
        :param entity: The entity that will be used to construct the context
        """
        context = super(NotificationTimedOut, self).get_context(entity)
        created_by = entity["info"]["created"]["by"]
        context.update(
            {
                "batch_name": entity.meta.name,
                "batch_guid": entity.guid,
                "number_of_jobs": len(entity["sets"]),
                "created_by": created_by.get("email", str(created_by["guid"])),
            }
        )
        return context


@dataclass
class Notifications:
    """A wrapper for notifications.  qalx-orcaflex can send notifications to users at certain points during processing.

    :param notify_submitted[NotificationSubmitted]: The details for the notification that should be sent when
     a batch has been submitted (default=None)
    :param notify_completed[NotificationCompleted]: The details for the notification that should be sent when a batch
    has completed processing
    :param notify_timed_out[NotificationTimedOut]: The details for the notification that should be sent when a batch has
    timed out
    """

    notify_submitted: NotificationSubmitted = None
    notify_completed: NotificationCompleted = None
    notify_timed_out: NotificationTimedOut = None

    def validate(self):
        """
        Ensures that all notifications that are specified are valid
        :raises: ValidationError
        :return: True
        """
        for key in self.__dataclass_fields__.keys():
            notification = getattr(self, key)
            if notification:
                notification.validate()
        return True

    def to_valid_dict(self):
        """
        Ensures the notifications are valid before returning the notifications as a dict
        """
        if self.validate():
            return asdict(self)
