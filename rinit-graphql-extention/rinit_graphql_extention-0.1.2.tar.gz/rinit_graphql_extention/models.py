from django.db import models
from django.contrib.auth.models import User


class MutationCommit(models.Model):
    mutation_name = models.CharField(max_length=100)
    arguments = models.TextField()
    error = models.TextField(default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
