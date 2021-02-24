import re
import string
import sys

from bs4 import BeautifulSoup
from google.cloud import bigtable
from google.cloud.bigtable import row_filters


class BigTable(object):
    def __init__(self, project, instance_id, table_id):
        self.project = project
        self.instance_id = instance_id
        self.table_id = table_id
        self.table = None
        self._instantiate_table()

    def _instantiate_table(self):
        if not self.table:
            # Create a Cloud Bigtable client.
            client = bigtable.Client(project=self.project)
            # Connect to an existing Cloud Bigtable instance.
            instance = client.instance(instance_id=self.instance_id)
            # Open an existing table.
            self.table = instance.table(table_id=self.table_id)
        return self.table


class DocumentBigTable(BigTable):
    def __init__(self, project, instance_id, table_id, column_family_id, column_qualifier):
        super().__init__(project, instance_id, table_id)
        self.column_family_id = column_family_id
        self.column_qualifier = column_qualifier

    def fetch_document_content(self, document_id, organization_id):
        # Create a filter to only retrieve the most recent version of the cell for each column accross entire row.
        row_filter = row_filters.CellsColumnLimitFilter(1)

        row_key = str(document_id)[::-1] + '_' + str(organization_id)
        row = self._instantiate_table().read_row(row_key.encode('utf-8'), row_filter)

        if row:
            column_id = self.column_qualifier.encode('utf-8')
            return row.cells[self.column_family_id][column_id][0].value.decode('utf-8')
        else:
            return None

    def fetch_document_text(self, document_id, organization_id):
        content_html = self.fetch_document_content(document_id, organization_id)
        if content_html:
            # strip html code
            soup = BeautifulSoup(content_html, 'lxml')
            return soup.get_text(' ', True)
        else:
            return None


class ExtensionBigTable(BigTable):
    def __init__(self, project, instance_id, table_id, column_family_id, column_qualifier):
        super().__init__(project, instance_id, table_id)
        self.column_family_id = column_family_id
        self.column_qualifier = column_qualifier

    @staticmethod
    def _to_string(number, radix):
        """
        Returns a string representation of the first argument in the radix specified by the second argument
        :param number: to be converted to a string.
        :param radix: the radix to use in the string representation.
        :return:
        """
        if not 2 <= radix <= 36:
            radix = 10

        if radix == 10:
            return str(number)

        buf = ['' for i in range(0, 33)]
        char_pos = 32
        negative = (number < 0)

        if not negative:
            number = -number

        digits = string.digits + string.ascii_lowercase
        while number <= -radix:
            buf[char_pos] = digits[int(abs(number) % radix)]
            number = int(number / radix)
            char_pos -= 1
        buf[char_pos] = digits[int(-number)]

        if negative:
            char_pos -= 1
            buf[char_pos] = '-'

        return ''.join(buf[char_pos:33])

    @staticmethod
    def _complement(key: str, length: int):
        """
        pad the key with zeros to the specified length
        :param key: the key to complement
        :param length: the full length
        :return: padded string with zeros of the specified length
        """
        return key.rjust(length, '0')

    @staticmethod
    def _reverse(key: str):
        """
        reverse key characters, e.g. 12345 becomes 54321
        :param key: the key to reverse
        :return: reversed key
        """
        return key[::-1]

    @staticmethod
    def _long_key_formatter(key):
        """
        format a key to 14 characters
        the first character represent the number sign, 0 for negative, 1 for positive
        the second part is a 36 radix representation of the key
        then pad the concatenation of those two parts to 14 characters
        :param key: the key to format
        :return: formatted key
        """
        length = 14
        return '0' + ExtensionBigTable._complement(ExtensionBigTable._to_string(sys.maxsize + key + 1, 36),
                                                   length - 1) if key < 0 else '1' + ExtensionBigTable._complement(
            ExtensionBigTable._to_string(key, 36), length - 1)

    @staticmethod
    def _twisted_long_key_formatter(key):
        """
        reverse the result of `~qai.ExtensionBigTable._long_key_formatter`
        :param key: the key to format
        :return: formatted key
        """
        return ExtensionBigTable._reverse(ExtensionBigTable._long_key_formatter(key))

    @staticmethod
    def _max_length_string_key_formatter(key: str, length: int = 100):
        """
        pad the specified key to the specified length
        :param key: the key to pad
        :param length: the length to pad to
        :return: padded key to the specified length
        """
        return ExtensionBigTable._complement(key, length)

    @staticmethod
    def _generate_key(document_id, organization_id, workspace_id, persona_id):
        """
        generate key for bigtable extension table, format agreed with extensions back-end
        :param document_id: the document id
        :param organization_id: the organization id
        :param workspace_id: the workspace id
        :param persona_id: the persona id
        :return: formatted key
        """
        return '|'.join([
            ExtensionBigTable._twisted_long_key_formatter(organization_id),
            ExtensionBigTable._twisted_long_key_formatter(workspace_id),
            ExtensionBigTable._max_length_string_key_formatter(document_id),
            ExtensionBigTable._long_key_formatter(persona_id)
        ])

    def fetch_document_content(self, document_id, organization_id, workspace_id, persona_id):
        # Create a filter to only retrieve the most recent version of the cell for each column accross entire row.
        row_filter = row_filters.CellsColumnLimitFilter(1)

        row_key = ExtensionBigTable._generate_key(document_id, organization_id, workspace_id, persona_id)
        row = self._instantiate_table().read_row(row_key.encode('utf-8'), row_filter)

        if row:
            column_id = self.column_qualifier.encode('utf-8')
            return row.cells[self.column_family_id][column_id][0].value.decode('utf-8')
        else:
            return None

    def fetch_document_text(self, document_id, organization_id, workspace_id, persona_id):
        content = self.fetch_document_content(document_id, organization_id, workspace_id, persona_id)
        if content:
            # strip new lines
            return re.sub('\\n+', ' ', content)
        else:
            return None
