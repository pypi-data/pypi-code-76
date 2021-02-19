from django.db import models
from djangoldp.models import Model

SIZE_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
]

class Dashboard(Model):
    target = models.CharField(max_length=20, default='default')
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='1')
    background = models.BooleanField(default=True)
    content = models.TextField()
