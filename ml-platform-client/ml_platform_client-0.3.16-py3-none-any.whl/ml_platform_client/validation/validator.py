from .exceptions import ArgValueError
from .para import check_type, check_length, check_range, check_not_null


class ValidatorBase:
    def __init__(self):
        self.para_name = 'field'

    def validate(self, value):
        raise NotImplementedError()

    def set_para_name(self, name):
        self.para_name = name


class NotNullValidator(ValidatorBase):
    def validate(self, value):
        return check_not_null(self.para_name, value, is_arg=True)


class TypeValidator(ValidatorBase):
    def __init__(self, value_type):
        super().__init__()
        self.value_type = value_type

    def validate(self, value):
        return not value or check_type(self.para_name, value, self.value_type, is_arg=True)


class LengthValidator(ValidatorBase):
    def __init__(self, max_len):
        super().__init__()
        self.max_len = max_len

    def validate(self, value):
        return not value or check_length(self.para_name, value, self.max_len)


class RangeValidator(ValidatorBase):
    def __init__(self, max_value=float('inf'), min_value=float('-inf')):
        super().__init__()
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, value):
        return not value or check_range(self.para_name, value, self.max_value, self.min_value)


class StringValidator(ValidatorBase):
    def __init__(self, max_len=None, nullable=False):
        super().__init__()
        self.validators = [TypeValidator(str)]
        if not nullable:
            self.validators.append(NotNullValidator())
        if max_len:
            self.validators.append(LengthValidator(max_len))

    def validate(self, value):
        for validator in self.validators:
            validator.set_para_name(self.para_name)
            validator.validate(value)


class ObjectValidator(ValidatorBase):
    def __init__(self, primitive_types=(bool, int, float, str), allow_list=True, allow_dict=False):
        super().__init__()
        self.type_validator = TypeValidator(dict)
        self.type_validator.set_para_name(self.para_name)
        self.primitive_types = primitive_types
        self.allow_list = allow_list
        self.allow_dict = allow_dict

    def validate(self, value):
        self.type_validator.validate(value)
        if value:
            for key in value.keys():
                self.validate_value(key, value[key])

    def validate_value(self, key, value):
        if isinstance(value, self.primitive_types):
            return
        if isinstance(value, list):
            if self.allow_list:
                for v in value:
                    self.validate_value(key, v)
                return
            else:
                raise ArgValueError(message='expect [{}] not contain list for key [{}]'.format(self.para_name, key))
        if isinstance(value, dict):
            if self.allow_dict:
                for key in value.keys():
                    self.validate_value(key, value[key])
                return
            else:
                raise ArgValueError(message='expect [{}] not contain dict for key [{}]'.format(self.para_name, key))
        raise ArgValueError(message='unexpect type for key [{}] in [{}]'.format(key, self.para_name))


class StringObjectValidator(ObjectValidator):
    def __init__(self):
        super().__init__(primitive_types=(str,), allow_list=False, allow_dict=False)
