from gerridae.field import BaseField
from lxml import etree


class ItemMeta(type):
    def __new__(cls, name, bases, attrs):
        __fields = {
            field_name: attrs.pop(field_name)
            for field_name, obj in list(attrs.items())
            if isinstance(obj, BaseField)
        }
        attrs["__fields"] = __fields

        return type.__new__(cls, name, bases, attrs)


class Item(metaclass=ItemMeta):
    def __init__(self):
        self.result = {}

    def __repr__(self):
        return f"<{self.__class__.__name__}> {self.result}"

    @staticmethod
    def _get_html(html, **kwargs):
        """获取 etree.HTML obj"""
        if html:
            return etree.HTML(html)
        raise ValueError("html or url is expected")

    @classmethod
    def _parser_html(cls, *, html_etree):
        if html_etree is None:
            return ValueError("html_etree is expected")
        item_ins = cls()

        fields = getattr(item_ins, "__fields", {})
        for field_name, field_value in fields.items():
            clean_method = getattr(item_ins, f"clean_{field_name}", None)
            value = field_value.extract(html_etree)

            # check the many to get the current
            many = getattr(field_value, "many", False)
            if not many:
                value = value if len(value) == 0 or isinstance(value, str) else value[0]

            if clean_method and callable(clean_method):
                assert value, f"{field_name} value is {value}"
                value = clean_method(value)

            # default value for field
            if not value:
                default_value = getattr(field_value, "default", False)
                value = default_value

            # setattr for Item class
            setattr(item_ins, field_name, value)
            item_ins.result[field_name] = value
        return item_ins

    @classmethod
    def get_item(cls, html=None):
        if html:
            html_etree = cls._get_html(html)
            return cls._parser_html(html_etree=html_etree)
        raise ValueError("html or url is excepted")

    @classmethod
    def get_items(cls, html=None, url=None):
        pass
