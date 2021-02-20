import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django import forms
from django.db import transaction


class ResizeImageMixin:
    def resize(self, imageField: models.ImageField, size:tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert('RGB')
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format='JPEG') # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.jpeg'

        imageField.save(random_name, file, save=False)


class DeletedModelMixin(models.Model):
    is_mark_as_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_mark_as_delete = True
        self.save()


class SingletonModelMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        pass


class InvalidInputsError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return (
            f'{repr(self.errors)}')


class Service(forms.Form):
    def clean_perform(self):
        if not self.is_valid():
            raise InvalidInputsError(self.errors)

    @classmethod
    def exec(cls, inputs, **kwargs):
        instance = cls(inputs, **kwargs)
        instance.clean_perform()
        with transaction.atomic():
            return instance.go()

    def go(self):
        raise NotImplementedError()
