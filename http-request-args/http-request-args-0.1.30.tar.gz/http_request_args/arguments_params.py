
class DateTimeParams:
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    date_time_format = date_format + ' ' + time_format

class StringParams:
    long_str_len = 10000  # [char]
    tiny_str_len = 150  # [char]
    uuid_len = 36  # [char]
    mongo_db_id_len = 24  # [char]
    admin_0_code_alpha_2_len = 2  # [char]
    admin_0_code_alpha_3_len = 3  # [char]

class LocationParams:
    longitude_range = [-180.0, 180.0]
    latitude_range = [-90.0, 90.0]