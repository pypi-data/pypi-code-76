from datetime import date, datetime
from decimal import Decimal
from django.db.models import Model


class Serialize:

    def __serialize_qs_instance(self, instance, fields=None):

        ##################################################
        #
        # Initial Data Checks
        #
        ##################################################

        # If the Instance is Empty (None), return an Empty Dictionary
        if instance is None:
            return {}

        # Fields must be included, or None will be returned
        if not fields and hasattr(instance, 'serializable_fields'):
            if len(instance.serializable_fields) > 0:
                fields = instance.serializable_fields
            else:
                return None
        elif not fields:
            return None

        ##################################################
        #
        # Get Model / Instance Information
        #
        ##################################################

        # Create Empty Starting Dictionary
        instance_dict = {}

        # Get The Model & Fields  # These methods are not officially supported
        model = instance._meta.model
        instance_fields = model._meta.get_fields(include_parents=True, include_hidden=True)

        # Get List of Cached Fields
        fields_cache = instance._state.fields_cache

        try:
            objects_cache = instance._prefetched_objects_cache
        except AttributeError:
            objects_cache = {}

        # Create a List to capture "Checked Fields"
        # This List will be checked at the end to confirm all fields in the list were captured
        parsed_fields = []

        ##################################################
        #
        # Get Field Information
        #
        ##################################################

        # Cycle Through the Fields
        for field in instance_fields:

            parsed_fields.append(field.name)

            # Define Names for FK and Parent References
            field_id = f'{field.name}_id'
            field_set = f'{field.name}_set'

            # If field is not in current list of fields, move to the next field
            if field.name not in fields and field_id not in fields and field_set not in fields:
                continue

            # Get the Field Type
            field_type = field.get_internal_type()

            # Convert Date/DateTime to ISO Format
            if field_type in ('DateTimeField', 'DateField'):
                field_value = getattr(instance, field.name, None)
                if field_value is None:
                    instance_dict[field.name] = None
                elif isinstance(field_value, datetime) or field_type == 'DateTimeField':
                    instance_dict[field.name] = datetime.isoformat(field_value)
                elif isinstance(field_value, date):
                    instance_dict[field.name] = date.isoformat(field_value)

            # Convert Decimal to Floats
            elif field_type == 'DecimalField':
                if getattr(instance, field.name, None) is None:
                    instance_dict[field.name] = None
                else:
                    instance_dict[field.name] = float(getattr(instance, field.name))

            # Convert to URL of Fields
            elif field_type in ('ImageField', 'FileField'):
                instance_value = getattr(instance, field.name, '')
                if instance_value == '' or instance_value is None:
                    instance_dict[field.name] = None
                else:
                    instance_dict[field.name] = instance_value.url

            elif field_type in ('ForeignKey', 'OneToOneField'):

                # If Select Related, Add the Related Model Instance
                if field.name in fields_cache:
                    field_instance = self.__serialize_qs_instance(fields_cache[field.name])
                    if field_instance is not None and field_instance != {}:
                        instance_dict[field.name] = field_instance
                    elif getattr(instance, field_id, None) is not None:
                        instance_dict[field_id] = getattr(instance, field_id, None)

                elif field_set in objects_cache:
                    field_value = getattr(instance, field_set, None)
                    if field_value is not None:
                        instance_dict[field_set] = self.__serialize_list(field_value.all())

                elif field.name in objects_cache:
                    field_value = getattr(instance, field.name, None)
                    if field_value is not None:
                        instance_dict[field.name] = self.__serialize_list(field_value.all())

                elif field.name not in fields_cache and getattr(instance, field_id, None) is not None:
                    instance_dict[field_id] = getattr(instance, field_id, None)

            elif field_type == 'ManyToManyField':

                # If Prefetch related, Add Related Model
                try:
                    if field.name in objects_cache:
                        instance_dict[field_set] = self.__serialize_list(getattr(instance, field.name).all())

                except (AttributeError, KeyError):
                    pass

            elif field_type == 'UUIDField':

                if getattr(instance, field.name, None) is None:
                    instance_dict[field.name] = getattr(instance, field.name, None)
                else:
                    instance_dict[field.name] = getattr(instance, field.name).hex

            else:

                field_value = getattr(instance, field.name, None)

                if field_value is None:
                    instance_dict[field.name] = None

                elif isinstance(field_value, datetime):
                    instance_dict[field.name] = datetime.isoformat(field_value)

                elif isinstance(field_value, date):
                    instance_dict[field.name] = date.isoformat(field_value)

                elif type(field_value) is Decimal:
                    instance_dict[field.name] = float(field_value)

                else:
                    instance_dict[field.name] = getattr(instance, field.name, None)

        # Confirm All Fields were Added
        # These are typically @property fields
        for field in fields:
            if field not in parsed_fields:

                field_value = getattr(instance, field, None)

                if type(field_value) is Decimal:
                    instance_dict[field] = float(field_value)

                elif isinstance(field_value, datetime):
                    instance_dict[field] = datetime.isoformat(field_value)

                elif isinstance(field_value, date):
                    instance_dict[field] = date.isoformat(field_value)

                else:
                    instance_dict[field] = field_value

        return instance_dict

    def __serialize_dict_instance(self, instance, fields=None):

        instance_dict = {}

        for field in instance:

            if fields and field not in fields:
                continue

            field_value = instance[field]

            if field_value is None:
                instance_dict[field] = field_value

            elif type(field_value) == bool:
                instance_dict[field] = bool(field_value)

            elif type(field_value) is date:
                instance_dict[field] = date.isoformat(field_value)

            elif type(field_value) is datetime:
                instance_dict[field] = datetime.isoformat(field_value)

            elif type(field_value) is Decimal:
                try:
                    instance_dict[field] = float(field_value)
                except ValueError:
                    instance_dict[field] = field_value

            else:
                instance_dict[field] = field_value

        return instance_dict

    def __serialize_instance(self, instance, fields=None):

        # Determine Specific Function to Run
        if isinstance(instance, Model):
            return self.__serialize_qs_instance(instance, fields=fields)
        elif isinstance(instance, dict):
            return self.__serialize_dict_instance(instance, fields=fields)

    def __serialize_list(self, qs=None, fields=None):

        # Empty List
        serialized_list = []

        # Loop Through QS and Serialize
        for instance in qs:
            serialized_list.append(self.__serialize_instance(instance, fields=fields))

        # Return List
        return serialized_list

    def serialize(self, qs=None, fields=None):

        # Determine the function to run
        if isinstance(qs, Model) or isinstance(qs, dict):
            return self.__serialize_instance(instance=qs, fields=fields)

        return self.__serialize_list(qs=qs, fields=fields)
