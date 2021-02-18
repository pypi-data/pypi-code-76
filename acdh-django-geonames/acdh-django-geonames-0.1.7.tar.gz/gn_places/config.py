GN_FTC_SCHEME = {
    "title": "GeoName Feature Codes",
    "title_lang": "eng",
    "creator": "GeoNames"
}

GN_FTC_COLLECTION = {
    "name": "GeoName Feature Codes"
}

GN_HTML_URL = "https://sws.geonames.org/"


def field_mapping(some_class):
    """ returns a dictionary mapping model field names to lookukp values

        :param some_class: Any django model class with extra field properties
        :return: A dict mapping model field names to\
            lookukp values and field types
        :rtype: dict
    """
    field_mapping_dict = {}
    for x in some_class._meta.get_fields():
        try:
            dict_key = x.extra['data_lookup'].lower().strip()
            field_mapping_dict[dict_key] = {
                'field_name': x.name,
                'field_type': type(x)
            }
        except Exception as e:
            print(e)
    return field_mapping_dict
