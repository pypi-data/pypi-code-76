from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Report


@receiver(pre_delete, sender=Report)
def auto_delete_report_file(sender, instance, **kwargs):
    if instance.report_file:
        instance.report_file.delete(save=False)
