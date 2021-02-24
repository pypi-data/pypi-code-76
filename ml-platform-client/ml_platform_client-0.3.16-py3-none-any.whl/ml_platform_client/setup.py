from .field_type import FieldType
from .validation.validator import StringValidator, NotNullValidator, ObjectValidator

train_arg_setup = {
    'algorithm': FieldType.String,
    'model_path': FieldType.String,
    'data': FieldType.Object,
    'parameter': FieldType.Object,
    'extend': FieldType.Object,
}

train_validate_setup = {
    'algorithm': StringValidator(32),
    'model_path': StringValidator(1024),
    'data': [NotNullValidator()],
    'parameter': [NotNullValidator()],
    'extend': [NotNullValidator()],
}

predict_arg_setup = {
    'features': FieldType.Object,
    'model_id': FieldType.String,
    'uuid': FieldType.String,
    'params': FieldType.Object
}

predict_validate_setup = {
    'features': ObjectValidator(),
    'model_id': StringValidator(max_len=64),
}

load_arg_setup = {
    'model_path': FieldType.String,
    'model_id': FieldType.String,
    'algorithm': FieldType.String,
}

load_validate_setup = {
    'model_id': StringValidator(max_len=64),
    'model_path': StringValidator(max_len=1024),
    'algorithm': StringValidator(64),
}

unload_arg_setup = {
    'model_id': FieldType.String,
    'algorithm': FieldType.String,
}

unload_validate_setup = {
    'model_id': StringValidator(max_len=64),
    'algorithm': StringValidator(64),
}

delete_arg_setup = {
    'model_id': FieldType.String,
    'algorithm': FieldType.String,
}

delete_validate_setup = {
    'model_id': StringValidator(max_len=64),
    'algorithm': StringValidator(64),
}

status_arg_setup = {
    'algorithm': FieldType.String,
    'model_id': FieldType.String,
}

status_validate_setup = {
    'model_id': StringValidator(max_len=64),
    'algorithm': StringValidator(64),
}
