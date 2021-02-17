import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone

from .signals import payment_received


class Payment(models.Model):
    class StatusType(models.IntegerChoices):
        PENDING = 0, "Ожидает оплаты"
        SUCCESS = 1, "Успешно"
        REJECTED = 2, "Отклонен"

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    amount = models.DecimalField("Сумма", max_digits=20, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        "Статус", choices=StatusType.choices, default=StatusType.PENDING
    )
    created = models.DateTimeField("Дата создания", default=timezone.now)

    object_id = models.UUIDField()
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    receiver = GenericForeignKey()

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created"]

    def __str__(self):
        return str(self.id.hex)

    def accept(self):
        self.status = self.StatusType.SUCCESS
        self.save()
        payment_received.send(self.content_type.model_class(), receiver=self.receiver)

    def reject(self):
        self.status = self.StatusType.REJECTED
        self.save()
