import logging

import django
from django.conf import settings
from django.db.models import Exists, OuterRef
from django.utils import timezone

from huscy.subjects.models import Address, Child, Contact, Inactivity, Patient, Subject, Note

logger = logging.getLogger('huscy.subjects')

ADULT_AGE = getattr(settings, 'HUSCY_SUBJECTS_ADULT_AGE', 18)


def create_address(country, city, zip_code, street):
    return Address.objects.create(country=country, city=city, zip_code=zip_code, street=street)


def update_address(address, country, city, zip_code, street):
    address.country = country
    address.city = city
    address.zip_code = zip_code
    address.street = street
    address.save()
    return address


def create_contact(first_name, last_name, display_name, gender, date_of_birth, address, email='',
                   phone_emergency='', phone_home='', phone_mobile='', phone_work=''):
    contact = Contact.objects.create(
        address=address,
        date_of_birth=date_of_birth,
        display_name=display_name,
        email=email,
        first_name=first_name,
        gender=gender,
        last_name=last_name,
        phone_emergency=phone_emergency,
        phone_home=phone_home,
        phone_mobile=phone_mobile,
        phone_work=phone_work,
    )
    return contact


def update_contact(contact, first_name, last_name, display_name, gender, date_of_birth, email='',
                   phone_emergency='', phone_home='', phone_mobile='', phone_work=''):
    contact.date_of_birth = date_of_birth
    contact.display_name = display_name
    contact.email = email
    contact.first_name = first_name
    contact.gender = gender
    contact.last_name = last_name
    contact.phone_emergency = phone_emergency
    contact.phone_home = phone_home
    contact.phone_mobile = phone_mobile
    contact.phone_work = phone_work
    contact.save()
    return contact


def create_subject(contact, is_patient=False):
    subject = Subject.objects.create(contact=contact)

    logger.info('Subject id:%d has been created', subject.id)

    if subject.age_in_years < ADULT_AGE:
        Child.objects.create(subject=subject)

    if is_patient:
        Patient.objects.create(subject=subject)

    return subject


def get_subjects(include_children=False, include_patients=False):
    queryset = Subject.objects

    if django.VERSION >= (3, 0):
        if include_children is False:
            queryset = queryset.exclude(Exists(Child.objects.filter(subject=OuterRef('pk'))))

        if include_patients is False:
            queryset = queryset.exclude(Exists(Patient.objects.filter(subject=OuterRef('pk'))))

    else:  # django version < 3
        queryset = queryset.annotate(
            _is_child=Exists(Child.objects.filter(subject=OuterRef('pk'))),
            _is_patient=Exists(Patient.objects.filter(subject=OuterRef('pk')))
        )

        if include_children is False:
            queryset = queryset.exclude(_is_child=True)

        if include_patients is False:
            queryset = queryset.exclude(_is_patient=True)

    return (queryset.select_related('contact__address')
                    .prefetch_related('child_set', 'inactivity_set', 'patient_set')
                    .prefetch_related('guardians__address')
                    .prefetch_related('notes')
                    .order_by('contact__last_name', 'contact__first_name'))


def update_subject(subject, is_patient):
    if subject.age_in_years < ADULT_AGE and subject.is_child is False:
        Child.objects.create(subject=subject)

    if is_patient is True and subject.is_patient is False:
        Patient.objects.create(subject=subject)
    elif is_patient is False and subject.is_patient is True:
        subject.patient_set.get().delete()

    return subject


def set_inactivity(subject, until=None):
    if until and until < timezone.now().date():
        raise ValueError(f'Until ({until}) cannot be in the past.')

    inactivity, created = Inactivity.objects.get_or_create(subject=subject,
                                                           defaults={'until': until})
    if not created:
        inactivity.until = until
        inactivity.save()

    return inactivity


def unset_inactivity(subject):
    subject.inactivity_set.all().delete()


def add_guardian(subject, contact):
    if subject.contact == contact:
        raise ValueError('Cannot add contact as guardian because it\'s the subject itself!')

    subject.guardians.add(contact)
    return contact


def remove_guardian(subject, guardian):
    subject.guardians.remove(guardian)
    if not guardian.subjects.exists():
        guardian.delete()


def create_note(subject, creator, option, text):
    if option == Note.OPTIONS.get_value('other'):
        return Note.objects.create(subject=subject, creator=creator, option=option, text=text)
    return Note.objects.create(subject=subject, creator=creator, option=option)


def get_notes(subject):
    return Note.objects.filter(subject=subject)
