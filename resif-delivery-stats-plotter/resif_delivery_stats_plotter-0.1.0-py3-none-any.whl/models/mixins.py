# encoding: utf8
import re
regex_location_code = re.compile("(?:(?P<location>.*)\.)?(?P<band>\w)(?P<instrument>\w)(?P<orientation>\w)")


class LocationCodeMixin:

    @staticmethod
    def extract_location_from_location_code(location_code):
        """
        Extracts the band code from a channel location code

        :param location_code: The channel location code
        :return: The location
        :rtype: str
        """
        matches = regex_location_code.search(location_code)
        return matches.group('location') or None

    @staticmethod
    def extract_band_from_location_code(location_code):
        """
        Extracts the band code from a channel location code

        :param location_code: The channel location code
        :return: The band code
        :rtype: str
        """
        matches = regex_location_code.search(location_code)
        return matches.group('band')

    @staticmethod
    def extract_instrument_from_location_code(location_code):
        """
        Extracts the instrument code from a channel location code

        :param location_code: The channel location code
        :return: The instrument code
        :rtype: str
        """
        matches = regex_location_code.search(location_code)
        return matches.group('instrument')

    @staticmethod
    def extract_orientation_from_location_code(location_code):
        """
        Extracts the orientation code from a channel location code

        :param location_code: The channel location code
        :return: The orientation code
        :rtype: str
        """
        matches = regex_location_code.search(location_code)
        return matches.group('orientation')