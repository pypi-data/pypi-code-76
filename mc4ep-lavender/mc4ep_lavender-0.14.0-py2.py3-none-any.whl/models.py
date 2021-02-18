from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now

from lavender.utils import texture_path_handler


class Player(AbstractUser):
    packages = models.ManyToManyField('Package', blank=True)


class LogHistory(models.Model):
    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)

    date = models.DateTimeField(default=now)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.player.username} at {self.date} from {self.source}"


class Token(models.Model):
    player: Player = models.OneToOneField(Player, on_delete=models.CASCADE)

    access = models.UUIDField(null=True)
    client = models.UUIDField(null=True)
    uuid = models.UUIDField(default=uuid4)
    server_id = models.CharField(max_length=48, null=True)
    created = models.DateTimeField(default=now)

    def __repr__(self):
        return f"{self.player.username} (access: {self.access} client: {self.client}"


class GameLog(models.Model):
    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)

    date = models.DateTimeField(default=now)
    kind = models.CharField(max_length=16)
    payload = models.TextField(default="")

    def __str__(self):
        return f"{self.player.username} at {self.date}: {self.kind}"


class Package(models.Model):
    name = models.CharField(max_length=16)
    version = models.CharField(max_length=16)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Quenta(models.Model):
    player: Player = models.OneToOneField(Player, on_delete=models.CASCADE, null=True)

    text = models.TextField()
    comments = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        status = "approved" if self.approved else "declined"
        return f"{self.__class__.__name__} for {self.player.username}: {status}"


class Texture(models.Model):
    token: Token = models.ForeignKey(Token, on_delete=models.CASCADE)  # To avoid redundant joins
    created = models.DateTimeField(default=now)
    kind = models.CharField(max_length=6)
    deleted = models.BooleanField(default=False)

    height = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    image = models.ImageField(
        null=True,
        blank=True,
        height_field='height',
        width_field='width',
        upload_to=texture_path_handler
    )

    class Meta:
        indexes = [
            models.Index(fields=['kind', 'deleted', '-created']),
        ]

    def __str__(self):
        return f"{self.__class__.__name__} of type {self.kind} for {self.token.player.username}"


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    record = LogHistory(player=user, source='site')
    record.save()
