import html
import re

from lxml import etree


class BaseField:
    """base field"""

    def __init__(self, many=False, default=None):
        self.default = default
        self.many = many

    def extract(self, *args, **kwargs):
        raise NotImplementedError("extract is not implemented.")


class _LXMLElementField(BaseField):
    """usage TextField Attribute """

    def __init__(self, css_select=None, many=False, default=None):
        super(_LXMLElementField, self).__init__(many, default)
        self.css_select = css_select
        self.many = many

    def _get_elements(self, *, html_etree):
        if self.css_select:
            elements = html_etree.cssselect(self.css_select)
        else:
            raise ValueError(f"{self.__class__.__name__} field css_select is expected")
        return elements

    def _parser_element(self, element):
        raise NotImplementedError

    def extract(self, html_etree):
        elements = self._get_elements(html_etree=html_etree)
        if elements:
            result = [self._parser_element(element) for element in elements]
        else:
            result = []
        return result


class TextField(_LXMLElementField):
    """text filed"""

    def __init__(self, css_select=None, many=False, default=None):
        super(TextField, self).__init__(css_select, many, default)

    def _parser_element(self, element):
        strings = [node.strip() for node in element.itertext()]
        string = "".join(strings)
        return string if string else self.default


class AttrField(_LXMLElementField):
    """attribute field"""

    def __init__(self, css_select=None, attr=None, many=False, default=None):
        super(AttrField, self).__init__(css_select, many, default)
        assert attr, "excepted attr"
        self.attr = attr

    def _parser_element(self, element):
        return element.get(self.attr, self.default)


class RegexField(BaseField):
    def __init__(self, pattern=None, re_flags=0, many=False, default=None, encoding='utf-8'):
        super(RegexField, self).__init__(many, default)
        self.encoding = encoding
        self.pattern = pattern
        self._re_object = re.compile(pattern, flags=re_flags)

    def _parse_match(self, match):
        if not match:
            if self.default is None:
                raise ValueError(
                    f"""Extract `{self.pattern}` error, "please check selector or set parameter named `default`""")
            return self.default

        string = match.group()
        groups = match.groups()
        group_dict = match.groupdict()
        if group_dict:
            return group_dict
        if groups:
            return groups[0] if len(groups) == 1 else groups
        return string

    def extract(self, html_etree):
        html_data = etree.tostring(html_etree).decode(encoding=self.encoding)
        html_data = self.decode_html(html_data)

        if self.many:
            matches = self._re_object.finditer(html_data)
            return [self._parse_match(match) for match in matches]
        else:
            match = self._re_object.search(html_data)
            return self._parse_match(match)

    @staticmethod
    def decode_html(html_data):
        s = html.unescape(html_data)
        return s
