from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Max, Q
from django.utils import timezone


class Signature(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    news = models.BooleanField()
    added_to_newsletter_list = models.BooleanField(default=False)
    has_captcha_verified = models.BooleanField()
    manually_verified_at = models.DateTimeField(null=True, blank=True)
    email_sent_at = models.DateTimeField(null=True, blank=True, db_index=True)
    email_verified_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return (
            f"{self.first_name} {self.surname} ({'news' if self.news else 'no_news'})"
            f"{'(verified) ' if self.email_verified_at else ''}: {self.email} "
        )

    @staticmethod
    def get_count() -> int:
        """Returns the number of verified signatures."""
        return settings.SIGNATURE_COUNTER_OFFSET + Signature.get_validated().count()

    @staticmethod
    def mark_email_as_verified(email: str, date: datetime):
        """Mark email as verified."""
        try:
            signature = Signature.objects.get(email=email)
        except Signature.DoesNotExist:
            return False

        signature.email_verified_at = date
        signature.save()

        return True

    @staticmethod
    def get_unsent():
        """Returns all the Signature without email_sent_at."""
        return Signature.objects.filter(email_sent_at=None)

    @staticmethod
    def get_validated():
        """Returns the valid signatures."""
        return Signature.objects.filter(email_verified_at__isnull=False).filter(
            Q(has_captcha_verified=True) | Q(manually_verified_at__isnull=False)
        )


class CallOutEmail(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=False)
    subject = models.CharField(max_length=200)
    send_to_government = models.BooleanField()
    circonscription_numbers = models.CharField(max_length=35, null=True, blank=True)
    sender = models.CharField(max_length=100)
    from_email = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=10)
    template_id = models.IntegerField(blank=True, null=True)

    email_sent_at = models.DateTimeField(null=True, blank=True, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True, db_index=True)

    @staticmethod
    def get_count() -> int:
        """Returns the number of verified signatures."""
        return CallOutEmail.objects.filter(verified_at__isnull=False).count()

    @staticmethod
    def get_unsent():
        """Returns all pending emails."""
        return CallOutEmail.objects.filter(email_sent_at=None)


class EmailOffset(models.Model):
    """Stores the last offset of events fetched by get_delivered_emails."""

    created_at = models.DateTimeField(default=timezone.now)
    offset = models.IntegerField(default=0, db_index=True)

    @staticmethod
    def get_max_offset() -> int:
        """Return the maximum offset stored in the table."""
        result = EmailOffset.objects.aggregate(Max('offset'))['offset__max']

        if result is None:
            return 0
        else:
            return result


class BlackListedEmail(models.Model):
    """Just a list of forbidden emails."""

    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(db_index=True, unique=True)

    def __str__(self):
        return self.email

    @staticmethod
    def is_blacklisted(email: str):
        """Return True if the email is forbidden."""
        return BlackListedEmail.objects.filter(email=email).exists()
