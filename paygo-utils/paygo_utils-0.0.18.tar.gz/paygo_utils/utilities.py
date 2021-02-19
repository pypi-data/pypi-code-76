import decimal
import json
import logging
import re
import sys
import uuid


def default_search_form_input_styles(width: float = 25):
    """
    This function is used to compose the default input field css styles that are applied on the search input.

    :param width: float: Maximum size of the input fields
    :return: dict: Returns a dictionary containing input field css styles
    """
    return {"placeholder": 'ENTER SEARCH TERM', "class": "form-control input-widget-size",
            'style': f'width:{width}%; margin-left:0.5em; margin-right:0.2em; height: calc(2.2rem + 2px); margin-top: 0.3em;'}


def generate_uuid():
    """
    This function is used to generate a uuid string.

    :return: str: uuid string
    """
    return uuid.uuid4().hex


def default_input_widget_styles(place_holder):
    """
    These are the default css classes used when creating input field user interface forms.

    :param place_holder: str: Input field placeholder
    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"placeholder": place_holder, "class": "form-control input-widget-size"}


def default_datetime_widget_styles(place_holder):
    """
    This function contains the default css classes used when creating input field user interface forms.

    :param place_holder: str: Input field placeholder
    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"placeholder": place_holder, "class": "form-control datetimepicker input-widget-size"}


def default_date_widget_styles(place_holder):
    """
    This function contains the default css classes used when creating a date field user interface forms.

    :param place_holder: str: Input field placeholder
    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"placeholder": place_holder, "class": "form-control datepicker input-widget-size"}


def default_drop_down_widget_styles(place_holder):
    """
    This function contains the default css classes used when creating a drop down select field user interface forms.

    :param place_holder: str: Input field placeholder
    :return: dict: Returns a dictionary containing field's css styles
    """
    return {'data-size': 7, 'title': place_holder, "class": "selectpicker"}


def default_checkbox_input_widget_styles():
    """
    This function contains the default css classes used when creating a checkbox input field user interface forms.

    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"class": "form-check-input"}


def default_multiple_checkbox_input_widget_styles():
    """
    This function contains the default css classes used when creating a checkbox input field user interface forms.

    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"class": "checkbox-style"}


def default_bootstrap_checkbox_input_widget_styles():
    """
    This function contains the default css classes used when creating a checkbox input field user interface forms.

    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"class": "bootstrap-switch",
            "data-on-label": "<i class='tim-icons icon-check-2'></i>",
            "data-off-label": "<i class='tim-icons icon-simple-remove'></i>"}


def default_text_area_widget_styles(place_holder: str, size_in_pixels: int = 300):
    """
    This function contains the default css classes used when creating a text area user interface forms.

    :param place_holder: str: Input field placeholder
    :param size_in_pixels: int: Represents the text-area vertical height in pixels
    :return: dict: Returns a dictionary containing field's css styles
    """
    return {"placeholder": place_holder, "class": "form-control",
            'style': f'max-height: {size_in_pixels}px; border: 1px solid rgba(34, 42, 66, 0.7);'}


def extract_numeric_values(input_value):
    """
    This function is used to extract numeric values from the provided input and put in an array.

    :param input_value:
    :return:
    """
    if not input_value:
        return []
    input_value = str(input_value)
    return [int(s) for s in re.findall(r'\b\d+\b', input_value)]


def set_paginated_data_to_content(request, context: dict, paginator, show_paginator_summary: bool = True,
                                  record_per_page: int = 100):
    """
   This function is used to set paginated data together with the search form to the request context

    :param context: dict: Dictionary holding request details
    :param paginator: Paginator: Django paginator object
    :param request: request: HTTP request object
    :param show_paginator_summary: bool: Boolean flag used on the UI to show/hide the paginator summary
    :param record_per_page: int: Maximum number records per query set
    :return:
    """
    current_page = None
    if 'page' in request.GET:
        current_page = int(request.GET["page"])
    if current_page is None:
        current_page = 1
    page_object = paginator.get_page(current_page)
    page = paginator.page(current_page)
    start_index = page.start_index()
    end_index = page.end_index()
    if current_page != paginator.num_pages:
        end_index = (int(start_index) + record_per_page) - 1  # Subtract 1 because of the last index overflow

    context['records'] = page_object
    context['paginator'] = paginator
    context['current_page'] = current_page
    if show_paginator_summary:
        context['paginator_label'] = f'Showing {start_index} to {end_index} of {paginator.count} entries'


def add_search_term(search_term: str):
    """
    This function is used to construct a search by like query string that  is used by SQLAlchemy.

    :param search_term: str: Represents a search term to which the like operator is to be applied
    :return:
    """
    return '%{}%'.format(search_term)


def remove_all_white_space_and_new_line(data: str):
    """
    This function is used to remove all whitespaces, tabs and new lines from the received data string.

    :param data: str: Represents a string that this operation is to be applied on.
    :return: str: Returns a string
    """
    return re.sub(r"[\n\t\s]*", "", data)


def clean_multiple_spaces(value: str):
    """
    This function is used to remove all multiple white spaces and replace them with a single space

    :param value: str: Represents a data source that is to be cleaned
    :return: str: Returns a string without multiple spaces
    """
    return " ".join(value.split())


def remove_multiple_spaces(value: str):
    """
    This function is used to remove multiple white spaces from the search term
    and split the resultant value by a single space

    :param value: str: Represents a string to be cleaned up
    :return: str: Returns a string without multiple spaces
    """
    return clean_multiple_spaces(value).split(' ')


def is_place_holder_exists(place_holder: str, text: str):
    """
    This function is used to check if a place holder exists in the provided template

    :param place_holder:
    :param text:
    :return:
    """
    clean_data = clean_multiple_spaces(text)
    patterns = '(?i)%\\s*{}\\s*%'.format(place_holder)
    if re.search(patterns, clean_data):
        return True
    return False


def replace_placeholders(data_source: str, key_names_list: list, values_dictionary: dict):
    """
    This function is used to replace placeholders within % placeholder % with a value from the replacements.

    Note:
        replacement values should be placed in the values_dictionary
        for example if key_names_list = ['username','password']
        then values_dictionary = {'username':'some username', 'password':'some password'}

    :param data_source: str: Represents a data set on which value replacement is to be performed.
    :param key_names_list: list: Represents a list of keys expected to be present in the datasource
    :param values_dictionary: dict: Represents a key to value pair of dats that is to be replaced with placeholders
    :return: str: Returns a string with all specified placeholders replaced with actual values
    """
    try:
        if not data_source:
            return data_source
        pattern = r'\%(.+?)\%'
        placeholders = re.findall(pattern, data_source)

        for n, i in enumerate(placeholders):
            for key in key_names_list:
                if i == key and key in values_dictionary:
                    placeholders[n] = values_dictionary[key]

        items = iter(str(el) for el in placeholders)
        return re.sub(pattern, lambda L: next(items), data_source)
    except Exception as ex:
        logging.error(msg=ex)
        pass


def get_image_full_path(request, image):
    """
    This function is used to obtain an image url using the provided image object.

    :param request: request: HTTP request object
    :param image: ImageField: Represents the image from which an image url can be obtained
    :return:
    """
    if image and request:
        domain_root = request._current_scheme_host
        image_url = image.url
        return str(domain_root) + str(image_url)
    return None


class DecimalEncoder(json.JSONEncoder):
    """
    This class is used to encode decimal values into acceptable python json objects that are to be sent through an API.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def get_processed_json_object(data: str):
    """
    Serialize data into an acceptable python json object

    :param data: str: Represents a string to be converted to json
    :return: json: Returns a json object
    """
    return json.dumps(data, cls=DecimalEncoder)


def get_class_and_method_name():
    """
    This function is used to get the class and method name from the context in which this function is called.

    :return:
    """
    frame = sys._getframe(1)
    try:
        class_name = frame.f_locals['self'].__class__.__name__
    except KeyError:
        class_name = None
    method_name = frame.f_code.co_name
    return class_name, method_name


def get_client_ip_address(request):
    """
    This function is used to get the client's ip address from an HTTP request.

    :param request:
    :return:
    """
    # The X-Forwarded-For (XFF) HTTP header field is a common method for identifying the originating IP address
    # of a client connecting to a web server through an HTTP proxy or load balancer.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[-1].strip()
    else:
        # Client's ip address
        ip_address = request.META.get('REMOTE_ADDR', None)
    return ip_address


def get_util_logger(file_name):
    filename = f'_{file_name}.log'
    open(filename, 'a+')
    logging.basicConfig(filename=filename, level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s [%(funcName)s:%(lineno)d] %(message)s')
    return logging.getLogger(f'{file_name}')
