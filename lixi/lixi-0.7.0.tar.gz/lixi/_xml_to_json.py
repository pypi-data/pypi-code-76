import os, glob, re, isodate, datetime, pkg_resources, io, json
from decimal import *
from lxml import etree as elemTree
from xmljson import BadgerFish
from collections import OrderedDict
from operator import attrgetter

ns = {
    "xs": "http://www.w3.org/2001/XMLSchema",
    "lx": "lixi.org.au/schema/appinfo_elements",
    "li": "lixi.org.au/schema/appinfo_instructions",
}


def to_json(xml_etree, xsd_annotated_schema):
    """ Converts a Python XML etree to JSON etree and arranges the result per schema.
    
    Args:
        xml_etree (:obj:`lxml.etree`, required): XML Message to convert to JSON message.
        xsd_annotated_schema (:obj:`lxml.etree`, required): A LIXI XML Schema.
    
    Returns:
        A python JSON dict object.
    
    Raises:
        LIXIResouceNotFoundError: If the schema is not found at the schema path.
        LIXIInvalidSyntax: If the schema file is not well formed.
    """

    json_object = {}

    def json_verify_types(json_data, xsd_element):
        elementsandatt_mappings = {}
        complex_mappings = []
        simpletype_mappings = {}
        xml_to_json_message = """{
                "anyType":  "string",
                    "anySimpleType":  "string",
                    "string":  "string",
                    "normalizedString":  "string",
                    "token":  "string",
                    "language":  "string",
                    "Name":  "string",
                    "NCName":  "string",
                    "ID":  "id",
                    "IDREF":  "idref",
                    "IDREFS":  "idref",
                    "ENTITY":  "string",
                    "ENTITIES":  "string",
                    "NMTOKEN":  "string",
                    "NMTOKENS": "string",
                    "boolean": "boolean",
                    "base64Binary": "base64",
                    "hexBinary": "string",
                    "float": "number",
                    "decimal": "number",
                    "integer": "integer",
                    "nonPositiveInteger": "integer",
                    "negativeInteger": "integer",
                    "long": "integer",
                    "int": "integer",
                    "short": "integer",
                    "byte": "integer",
                    "nonNegativeInteger": "integer",
                    "unsignedLong": "integer",
                    "unsignedInt": "integer",
                    "unsignedShort": "integer",
                    "unsignedByte": "integer",
                    "positiveInteger": "integer",
                    "double": "number",
                    "anyURI": "string",
                    "QName": "string",
                    "NOTATION": "string",
                    "duration": "string",
                    "dateTime": "datetime",
                    "date": "date",
                    "time": "string",
                    "gYearMonth": "string",
                    "gYear": "year",
                    "gMonthDay": "string",
                    "gDay": "string",
                    "gMonth": "string"
    }"""

        # reading and storing the native XMLtypes to their equivalent json types
        type_mappings = json.loads(xml_to_json_message)

        # reading and storing the simpleTypes to their specified base XMLtypes
        for simple_type in xsd_element.findall("./xs:simpleType", namespaces=ns):
            element_name = simple_type.attrib.get("name")
            element_type = simple_type.find("xs:restriction", ns).attrib["base"]
            if "xs:" in element_type:
                element_type = element_type[3:]

            simpletype_mappings[element_name] = element_type

        # reading and storing the attributes and info containing elements to their simpletypes
        for every_element in xsd_element.iter():
            if "www.w3.org" in every_element.tag:
                try:
                    if (
                        "attribute" in every_element.tag
                        and every_element.attrib["type"] is not None
                    ):
                        element_name = "@" + every_element.attrib.get("name")
                        element_type = every_element.attrib["type"]
                        elementsandatt_mappings[element_name] = element_type
                    elif (
                        "element" in every_element.tag
                        and every_element.attrib["type"] is not None
                        and every_element.attrib.get("name") is not None
                    ):
                        element_name = "$" + every_element.attrib.get("name")
                        element_type = every_element.attrib["type"]
                        elementsandatt_mappings[element_name] = element_type
                except Exception as e:
                    pass

        # reading and removing the referance to the complexType as they will be meaningless in a json message file
        for complex_type in xsd_element.findall("./xs:complexType", namespaces=ns):
            element_name = complex_type.attrib.get("name")
            complex_mappings.append(element_name)

        for del_elementname in complex_mappings:
            elementsandatt_mappings = {
                k: v for k, v in elementsandatt_mappings.items() if v != del_elementname
            }

        # now we read and replace the values in elementsandatt_mappings with values of simpletype_mappings
        for k, v in elementsandatt_mappings.items():
            elementsandatt_mappings[k] = simpletype_mappings[v]

        # now we read and replace the values in elementsandatt_mappings with values of type_mappings
        for k, v in elementsandatt_mappings.items():
            elementsandatt_mappings[k] = type_mappings[v]

        # Voila! - now we have a list which has a type attached with a element and attribute name
        json_change_type(json_data, elementsandatt_mappings)

    def json_change_type(json_dict, elementsandatt_mappings):
        for k, v in json_dict.items():
            if isinstance(v, dict):
                json_change_type(v, elementsandatt_mappings)
            elif isinstance(v, list):
                for json_obj in v:
                    json_change_type(json_obj, elementsandatt_mappings)
            else:
                if k != "$":
                    type_cast_value = None
                    lookup = None
                    storage = None

                    if k in elementsandatt_mappings:
                        type_cast_value = v
                        lookup = elementsandatt_mappings[k]
                        storage = json_dict[k]
                    elif "$" + k in elementsandatt_mappings:
                        if "$" not in json_dict[k]:
                            json_dict[k]["$"] = ""

                        type_cast_value = json_dict[k]["$"]
                        lookup = elementsandatt_mappings["$" + k]
                        storage = json_dict[k]["$"]

                    if "number" == lookup or "decimal" == lookup or "float" == lookup:
                        type_cast_value = float(type_cast_value)
                    elif "integer" == lookup:
                        type_cast_value = int(type_cast_value)
                    elif "boolean" == lookup:
                        type_cast_value = bool(type_cast_value)
                    elif "base64" == lookup:
                        if not re.match(
                            "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
                            type_cast_value,
                        ):
                            raise Exception("Inline Attachment is not a Base 64 string")
                        type_cast_value = type_cast_value
                    elif "datetime" == lookup:
                        try:
                            dt = isodate.parse_datetime(type_cast_value)
                            type_cast_value = type_cast_value
                        except ValueError as e:
                            raise Exception(
                                "'"
                                + type_cast_value
                                + "' is not a valid ISO date string"
                            )
                    elif "date" == lookup:
                        try:
                            dt = datetime.datetime.strptime(type_cast_value, "%Y-%m-%d")
                            type_cast_value = type_cast_value
                        except ValueError as e:
                            raise Exception(
                                "'" + type_cast_value + "' is not a valid date"
                            )
                    elif "year" == lookup:
                        try:
                            dt = datetime.datetime.strptime(type_cast_value, "%Y")
                            type_cast_value = type_cast_value
                        except ValueError as e:
                            raise Exception(
                                "'" + type_cast_value + "' is not a valid date"
                            )
                    elif "id" == lookup or "idref" == lookup:
                        if not re.match("^[a-zA-Z0-9-_.]+$", type_cast_value):
                            raise Exception(
                                "ID '"
                                + type_cast_value
                                + "' contains forbidden characters"
                            )
                        elif not re.match("^[a-zA-Z_]+$", type_cast_value[:1]):
                            raise Exception(
                                "ID '"
                                + type_cast_value
                                + "' starts with a forbidden character"
                            )
                        type_cast_value = type_cast_value

                        # no point converting string types back to string // use later for dates and complex types
                    if k in elementsandatt_mappings:
                        json_dict[k] = type_cast_value
                    elif "$" + k in elementsandatt_mappings:
                        json_dict[k]["$"] = type_cast_value

    def json_change_occurance(json_dict, unbounded_elements_names):
        for k, v in json_dict.items():
            if isinstance(v, dict):
                json_change_occurance(v, unbounded_elements_names)
                if k in unbounded_elements_names:
                    json_dict[k] = []
                    json_dict[k].append(v)

            elif isinstance(v, list):
                for json_obj in v:
                    json_change_occurance(json_obj, unbounded_elements_names)

    def json_verify_occurance(json_data, xsd_element):

        # Generate a list that has the names of all elements where maxOccurs is greater than 1
        unbounded_elements_names = xsd_element.xpath(
            "//xs:element[@maxOccurs>1 or @maxOccurs='unbounded']/@name", namespaces=ns
        )

        # recursively step through the json message and replace objects with lists that have names in the above list
        json_change_occurance(json_data, unbounded_elements_names)

    bf = BadgerFish(xml_fromstring=False)
    json_object = bf.data(xml_etree)

    # Converts json types from string types to appropriate types specified in XML Schema
    json_verify_types(json_object, xsd_annotated_schema)
    # Converts elements that are single json objects in message (but repeatable in XML schema) to list/arrays
    json_verify_occurance(json_object, xsd_annotated_schema)

    return json_object


def to_json_string(xml_str, xsd_annotated_schema_str):
    """ Converts a Python XML string to JSON string and arranges the result per schema.
    
    Args:
        xml_str (:obj:`str`, required): XML Message string to convert to JSON message.
        xsd_annotated_schema_str (:obj:`str`, required): A LIXI XML Schema string.
    
    Returns:
        A python JSON string message object.
    
    Raises:
        LIXIResouceNotFoundError: If the schema is not found at the schema path.
        LIXIInvalidSyntax: If the schema file is not well formed.
    """

    xml_etree = elemTree.fromstring(xml_str)
    xsd_annotated_schema = elemTree.fromstring(xsd_annotated_schema_str)

    converted_json = to_json(xml_etree, xsd_annotated_schema)
    return json.dumps(converted_json, sort_keys=True, indent=4, ensure_ascii=False)


def to_xml(json_dict, xsd_annotated_schema):
    """ Converts a Python JSON dict to XML etree and arranges the result per schema.
    
    Args:
        json_dict (:obj:`dict`, required): JSON Message string to convert to XML message.
        xsd_annotated_schema (:obj:`lxml.etree`, required): A LIXI XML Schema string.
    
    Returns:
        A python XML Etree object.
    
    Raises:
        LIXIResouceNotFoundError: If the schema is not found at the schema path.
        LIXIInvalidSyntax: If the schema file is not well formed.
    """

    def xml_get_sorted_list(schema_root):
        sorting_elem_list = {}
        sorting_list = {}
        sorting_complex_list = {}

        for elem in schema_root.iter(tag=("{*}element", "{*}complexType")):

            if "element" in elem.tag and elem.attrib.get("name") is not None:
                if elem.attrib.get("type") is None:
                    key_name = (
                        str(
                            elem.xpath(
                                "./xs:annotation/xs:appinfo/lx:path/text()",
                                namespaces=ns,
                            )
                        )
                        .strip("[]'")
                        .replace(".", "/")
                    )

                    if (
                        elem.find(
                            "./xs:complexType/xs:sequence/xs:element", namespaces=ns
                        )
                        is not None
                    ):
                        sorting_elem_list[key_name] = []
                        for child_xsd_element in elem.xpath(
                            "./xs:complexType/xs:sequence/xs:element", namespaces=ns
                        ):
                            sorting_elem_list[key_name].append(
                                child_xsd_element.attrib.get("name")
                            )

                    elif (
                        elem.find(
                            "./xs:complexType/xs:choice/xs:element", namespaces=ns
                        )
                        is not None
                    ):
                        sorting_elem_list[key_name] = []
                        for child_xsd_element in elem.findall(
                            "./xs:complexType/xs:choice/xs:element", namespaces=ns
                        ):
                            sorting_elem_list[key_name].append(
                                child_xsd_element.attrib.get("name")
                            )

                elif elem.attrib.get("type") is not None:
                    key_name = (
                        str(
                            elem.xpath(
                                "./xs:annotation/xs:appinfo/lx:path/text()",
                                namespaces=ns,
                            )
                        )
                        .strip("[]'")
                        .replace(".", "/")
                    )
                    sorting_elem_list[key_name + "/" + elem.attrib.get("type")] = []

            elif "complexType" in elem.tag:
                if elem.attrib.get("name") is not None:
                    key_name = (
                        str(
                            elem.xpath(
                                "./xs:annotation/xs:appinfo/lx:path/text()",
                                namespaces=ns,
                            )
                        )
                        .strip("[]'")
                        .replace(".", "/")
                    )

                    if elem.find("./xs:sequence/xs:element", namespaces=ns) is not None:
                        sorting_complex_list[key_name] = []
                        for child_xsd_element in elem.xpath(
                            "./xs:sequence/xs:element", namespaces=ns
                        ):
                            sorting_complex_list[key_name].append(
                                child_xsd_element.attrib.get("name")
                            )

        for k, v in sorting_complex_list.items():
            for key, value in sorting_elem_list.items():
                if k in key:
                    sorting_list["/" + key.replace("/" + k, "")] = v

        for k, v in sorting_elem_list.items():
            if len(v) > 0:
                sorting_list["/" + k] = v

        return sorting_list

    def xml_sort_message(unsorted_xml, sorting_list):

        tree = elemTree.ElementTree(unsorted_xml)

        for e in unsorted_xml.xpath("//*"):

            keys = e.attrib
            sorted_attrib = OrderedDict(sorted(keys.items()))
            e.attrib.clear()
            e.attrib.update(sorted_attrib)

            elem_path_key = tree.getpath(e).strip("[0123456789]")

            if elem_path_key in sorting_list:
                e[:] = sorted(
                    e, key=lambda elem: get_elem_key(elem, elem_path_key, sorting_list)
                )

        return unsorted_xml

    def get_elem_key(elem, elem_path_key, sorting_list):

        try:
            if sorting_list[elem_path_key].index(elem.tag) is not None:
                return sorting_list[elem_path_key].index(elem.tag)
            else:
                return 0
        except:
            return 0

    bf = BadgerFish()
    unsorted_xml = bf.etree(json_dict)[0]

    sorting_list = xml_get_sorted_list(xsd_annotated_schema)
    converted_sorted_xml = xml_sort_message(unsorted_xml, sorting_list)

    return converted_sorted_xml


def to_xml_string(json_str, xsd_annotated_schema_str):
    """ Converts a Python JSON string to XML string and arranges the result per schema.
    
    Args:
        json_str (:obj:`str`, required): JSON Message string to convert to XML message.
        xsd_annotated_schema_str (:obj:`str`, required): A LIXI XML Schema string.
    
    Returns:
        A python XML string message object.
    
    Raises:
        LIXIResouceNotFoundError: If the schema is not found at the schema path.
        LIXIInvalidSyntax: If the schema file is not well formed.
    """

    json_dict = json.loads(json_str)
    xsd_annotated_schema = elemTree.fromstring(xsd_annotated_schema_str)

    converted_xml = to_xml(json_dict, xsd_annotated_schema)
    return elemTree.tostring(converted_xml, pretty_print=True).decode("utf-8")
