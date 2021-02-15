import uuid
from datetime import date
from enum import Enum

from django.conf import settings
from django.db import models

from dateutil import relativedelta
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    city = models.CharField(max_length=128)
    country = CountryField(default='DE')
    zip_code = models.CharField(max_length=16)  # c.f. http://en.wikipedia.org/wiki/Postal_codes
    street = models.CharField(max_length=255)  # street name & number + additional info

    def __str__(self):
        return f'{self.street}, {self.zip_code}, {self.city}, {self.country}'


class Contact(models.Model):
    class GENDER(Enum):
        female = (0, 'female')
        male = (1, 'male')
        diverse = (2, 'diverse')

    first_name = models.CharField(max_length=128)  # without middle names
    last_name = models.CharField(max_length=128)  # without middle names
    display_name = models.CharField(max_length=255)  # full name with prefixes (titles) and suffixes

    gender = models.PositiveSmallIntegerField(choices=[x.value for x in GENDER])

    date_of_birth = models.DateField()

    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, default='')
    phone_mobile = PhoneNumberField(blank=True, default='')
    phone_home = PhoneNumberField(blank=True, default='')
    phone_work = PhoneNumberField(blank=True, default='')
    phone_emergency = PhoneNumberField(blank=True, default='')

    def __str__(self):
        return f'{self.display_name}'


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='+')
    guardians = models.ManyToManyField(Contact, blank=True, related_name='subjects')

    @property
    def age_in_months(self):
        delta = relativedelta.relativedelta(date.today(), self.contact.date_of_birth)
        return delta.years * 12 + delta.months

    @property
    def age_in_years(self):
        return relativedelta.relativedelta(date.today(), self.contact.date_of_birth).years

    @property
    def is_active(self):
        return not self.inactivity_set.exists()

    @property
    def is_child(self):
        return self.child_set.exists()

    @property
    def is_patient(self):
        return self.patient_set.exists()


class Note(models.Model):
    class OPTIONS(Enum):
        hard_of_hearing = (0, 'hard of hearing')
        hard_to_understand = (1, 'hard to understand')
        other = (255, 'other')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    option = models.PositiveSmallIntegerField(choices=[x.value for x in OPTIONS])
    text = models.TextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class Child(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Patient(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Inactivity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    until = models.DateField(null=True)  # until = null means inactive with open end
