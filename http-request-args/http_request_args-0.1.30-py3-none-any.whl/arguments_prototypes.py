from .argument import NumberArgument, FileArgument, StringArgument, ListArgument
from .utilities import OperatorPrototype
from .arguments_params import LocationParams, StringParams, DateTimeParams


class NumberArgumentsPrototype:
    # Unix time
    req_unix_time = lambda field_name, **kwarg: NumberArgument(
        field_name, required=True, arg_type=float,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwarg)

    opt_unix_time = lambda field_name, **kwargs: NumberArgument(
        field_name, required=False, arg_type=float,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwargs)
    
    # Id
    req_sql_id = lambda field_name, **kwargs: NumberArgument(
        field_name, arg_type=int, required=True,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwargs)

    opt_sql_id = lambda field_name, **kwargs: NumberArgument(
        field_name, arg_type=int, required=False,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwargs)

    # Pagination
    req_page_number = lambda field_name, **kwargs: NumberArgument(
        field_name, arg_type=int, required=True,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwargs)

    opt_page_number = lambda field_name, **kwargs: NumberArgument(
        field_name, arg_type=int, required=False,
        comparison_operator=OperatorPrototype.create_greater_than_operator(0), **kwargs)

    # Location
    req_latitude = lambda field_name, **kwargs: NumberArgument(
        field_name, required=True, arg_type=float,
        req_range=LocationParams.latitude_range, **kwargs)

    req_longitude = lambda field_name, **kwargs: NumberArgument(
        field_name, required=True, arg_type=float,
        req_range=LocationParams.longitude_range, **kwargs)

    opt_latitude = lambda field_name, **kwargs: NumberArgument(
        field_name, required=False, arg_type=float,
        req_range=LocationParams.latitude_range, **kwargs)

    opt_longitude = lambda field_name, **kwargs: NumberArgument(
        field_name, required=False, arg_type=float,
        req_range=LocationParams.longitude_range, **kwargs)

    req_file_size = lambda field_name, min_size, max_size: NumberArgument(
        field_name, required=True, arg_type=float, req_range=[min_size, max_size])


class StringArgumentsPrototype:
    # Date
    req_date = lambda field_name, **kwargs: StringArgument(
        field_name, required=True, is_date=True,
        date_format=DateTimeParams.date_format, **kwargs)

    opt_date = lambda field_name, **kwargs: StringArgument(
        field_name, required=False, is_date=True,
        date_format=DateTimeParams.date_format, **kwargs)

    # Email
    req_email = lambda field_name, **kwargs: StringArgument(
        field_name, required=True, is_email=True,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    opt_email = lambda field_name, **kwargs: StringArgument(
        field_name, required=False, is_email=True,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    # Password
    req_password = lambda field_name, **kwargs: StringArgument(
        field_name, required=True, is_password=True,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    opt_password = lambda field_name, **kwargs: StringArgument(
        field_name, required=False, is_password=True,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    # Phone number
    req_phone_number = lambda field_name, **kwargs: StringArgument(
        field_name, required=True, is_phone_number=True, **kwargs)

    opt_phone_number = lambda field_name, **kwargs: StringArgument(
        field_name, required=False, is_phone_number=True, **kwargs)

    # String
    req_tiny_string = lambda field_name, **kwargs: StringArgument(
        field_name, required=True,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    req_long_string = lambda field_name, **kwargs: StringArgument(
        field_name, required=True,
        length_range=[1, StringParams.long_str_len], **kwargs)

    opt_tiny_string = lambda field_name, **kwargs: StringArgument(
        field_name, required=False,
        length_range=[1, StringParams.tiny_str_len], **kwargs)

    opt_long_string = lambda field_name, **kwargs: StringArgument(
        field_name, required=False,
        length_range=[1, StringParams.long_str_len], **kwargs)

    # Id
    req_mongo_id = lambda field_name, **kwargs: StringArgument(
        field_name, required=True,
        length_range=[StringParams.mongo_db_id_len, StringParams.mongo_db_id_len], **kwargs)

    req_uuid = lambda field_name, **kwargs: StringArgument(
        field_name, required=True,
        length_range=[StringParams.uuid_len, StringParams.uuid_len], **kwargs)

    opt_mongo_id = lambda field_name, **kwargs: StringArgument(
        field_name, required=False,
        length_range=[StringParams.mongo_db_id_len, StringParams.mongo_db_id_len], **kwargs)

    opt_uuid = lambda field_name, **kwargs: StringArgument(
        field_name, required=False, **kwargs,
        length_range=[StringParams.uuid_len, StringParams.uuid_len])

    req_country_code_alpha_2 = lambda field_name, **kwargs: StringArgument(
        field_name, required=True, 
        length_range=[StringParams.admin_0_code_alpha_2_len, StringParams.admin_0_code_alpha_2_len], **kwargs)

    opt_country_code_alpha_2 = lambda field_name, **kwargs: StringArgument(
        field_name, required=False,
        length_range=[StringParams.admin_0_code_alpha_2_len, StringParams.admin_0_code_alpha_2_len], **kwargs)

    req_country_code_alpha_3 = lambda field_name, **kwargs: StringArgument(
        field_name, required=True,
        length_range=[StringParams.admin_0_code_alpha_3_len, StringParams.admin_0_code_alpha_3_len], **kwargs)

    opt_country_code_alpha_3 = lambda field_name, **kwargs: StringArgument(
        field_name, required=False,
        length_range=[StringParams.admin_0_code_alpha_3_len, StringParams.admin_0_code_alpha_3_len], **kwargs)


class ListArgumentsPrototype:
    req_list_sql_ids = lambda field_name, **kwargs: ListArgument(
        field_name, required=True, arg_obj=NumberArgumentsPrototype.req_sql_id(field_name), **kwargs)

    req_list_mongo_ids = lambda field_name, **kwargs: ListArgument(
        field_name, required=True, arg_obj=StringArgumentsPrototype.req_mongo_id(field_name), **kwargs)

    req_list_uuids = lambda field_name, **kwargs: ListArgument(
        field_name, required=True, arg_obj=StringArgumentsPrototype.req_uuid(field_name), **kwargs)

    opt_list_sql_ids = lambda field_name, **kwargs: ListArgument(
        field_name, required=False, arg_obj=NumberArgumentsPrototype.opt_sql_id(field_name), **kwargs)

    opt_list_mongo_ids = lambda field_name, **kwargs: ListArgument(
        field_name, required=False, arg_obj=StringArgumentsPrototype.opt_mongo_id(field_name), **kwargs)

    opt_list_uuids = lambda field_name, **kwargs: ListArgument(
        field_name, required=False, arg_obj=StringArgumentsPrototype.opt_uuid(field_name), **kwargs)


class FileArgumentsPrototype:
    # File
    req_file = lambda field_name, min_size, max_size, extensions: FileArgument(
        field_name, required=True,
        file_size=NumberArgumentsPrototype.req_file_size(
            'file_size', min_size, max_size
        ),
        file_extensions=extensions)

    opt_file = lambda field_name, min_size, max_size, extensions: FileArgument(
        field_name, required=False,
        file_size=NumberArgumentsPrototype.req_file_size(
            'file_size', min_size, max_size
        ),
        file_extensions=extensions)
