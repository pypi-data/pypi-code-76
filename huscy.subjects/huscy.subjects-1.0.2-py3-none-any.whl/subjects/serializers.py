from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import exceptions, serializers

from huscy.subjects import models, services


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(initial='DE')

    class Meta:
        model = models.Address
        fields = (
            'city',
            'country',
            'street',
            'zip_code',
        )

    def create(self, validated_data):
        return services.create_address(**validated_data)

    def update(self, address, validated_data):
        return services.update_address(address, **validated_data)


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    phone_emergency = PhoneNumberField(allow_blank=True)
    phone_home = PhoneNumberField(allow_blank=True)
    phone_mobile = PhoneNumberField(allow_blank=True)
    phone_work = PhoneNumberField(allow_blank=True)

    class Meta:
        model = models.Contact
        fields = (
            'address',
            'date_of_birth',
            'display_name',
            'email',
            'first_name',
            'gender',
            'gender_display',
            'last_name',
            'phone_emergency',
            'phone_home',
            'phone_mobile',
            'phone_work',
        )

    def create(self, validated_data):
        address_serializer = AddressSerializer(data=validated_data.pop('address'))
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()

        return services.create_contact(address=address, **validated_data)

    def update(self, contact, validated_data):
        address_serializer = AddressSerializer(contact.address, data=validated_data.pop('address'))
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()

        return services.update_contact(contact, **validated_data)


class GuardianSerializer(ContactSerializer):

    def create(self, validated_data):
        subject = self.context['subject']
        contact = super().create(validated_data)
        return services.add_guardian(subject, contact)


class NoteSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    option_display = serializers.CharField(source='get_option_display', read_only=True)

    class Meta:
        model = models.Note
        fields = (
            'created_at',
            'creator',
            'creator_username',
            'id',
            'option',
            'option_display',
            'text',
        )
        extra_kwargs = {
            'option': {'write_only': True},
        }

    def create(self, validated_data):
        subject = self.context['subject']
        return services.create_note(subject=subject, **validated_data)


class SubjectSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    guardians = GuardianSerializer(many=True, read_only=True)
    is_patient = serializers.BooleanField()
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = models.Subject
        fields = (
            'age_in_months',
            'age_in_years',
            'contact',
            'guardians',
            'id',
            'is_active',
            'is_child',
            'is_patient',
            'notes',
        )

    def create(self, validated_data):
        contact_serializer = ContactSerializer(data=validated_data.pop('contact'))
        contact_serializer.is_valid(raise_exception=True)
        contact = contact_serializer.save()

        return services.create_subject(contact, **validated_data)

    def update(self, subject, validated_data):
        contact_serializer = ContactSerializer(subject.contact, data=validated_data.pop('contact'))
        contact_serializer.is_valid(raise_exception=True)
        contact_serializer.save()

        return services.update_subject(subject, **validated_data)


class InactivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inactivity
        fields = (
            'subject',
            'until',
        )

    def create(self, validated_data):
        try:
            return services.set_inactivity(**validated_data)
        except ValueError:
            raise exceptions.ValidationError
