
from django.db.models import Model, CharField

class TestObject(Model):
    name = CharField(max_length=32)

    def __str__(self):
        return self.name
