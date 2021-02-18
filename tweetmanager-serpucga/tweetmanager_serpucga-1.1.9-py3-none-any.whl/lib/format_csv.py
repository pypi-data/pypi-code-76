import math

from . import format_csv


def list_of_pairs_format_csv(csv_file):
    """
    Prints the contents of a CSV file composed of a header and several lines,
    each representing an object instance of the header fields, in a more
    readable manner.
    The display consists in a pretty visual representation of the name
    of each field as it appears on the header followed by an ordered list of
    the specific value of that field in each document. This kind of display is
    useful to see in a quick glance if the CSV collection is being built
    correctly (each value in its column), which kind of results prevail in a
    field, etc.
    """

    with open(csv_file, 'r') as csv_object:
        header = csv_object.readline()
        body = csv_object.readlines()

    header_fields = split_csv_line(header)
    documents = []

    for body_line in body:
        documents.append(split_csv_line(body_line))

    for index, field in enumerate(header_fields):
        print("=" * (len(field) + 8))
        print("||  " + field + "  ||")
        print("=" * (len(field) + 8))
        print("\n\n" + str([documents[j][index]
              for j in range(len(documents))]) + "\n")


def table_format_csv(csv_file):
    """
    Receives an arg pointing to a CSV file. Open it and format as a table
    adding "||" and "="
    """

    SPACING = 2
    formatted_text = ""
    with open(csv_file, 'r') as csv_object:

        # First calculate the lengths necessary to build a table
        fields_max_length = None
        line_max_length = 0

        for line in csv_object:

            line_words = split_csv_line(line)

            # Initialize lengths array with 0s
            if not fields_max_length:
                fields_max_length = []
                for i in range(len(line_words)):
                    fields_max_length.append(0)

            # Find the longest word for every field
            j = 0
            for word in line_words:
                if (len(word) + SPACING) > fields_max_length[j]:
                    fields_max_length[j] = len(word) + SPACING
                j += 1

    line_max_length =\
        sum(fields_max_length) + (2 * (len(fields_max_length) - 1))
    separator_line = '=' * line_max_length

    with open(csv_file, 'r') as csv_object:
        # And now let's build the table
        for line in csv_object:
            line_words = split_csv_line(line)

            # Generate a formatted line with filling spaces
            formatted_line = ""
            i = 0
            for word in line_words:
                num_spaces = fields_max_length[i] - len(word)
                formatted_line +=\
                    (math.floor(num_spaces / 2) * " ") + word +\
                    (math.ceil(num_spaces / 2) * " ") + "||"
                i += 1

            formatted_text +=\
                "||" + formatted_line + "\n" + "||" + separator_line + "||\n"

    return formatted_text


def split_csv_line(line):
    """
    This function splits a single CSV-RFC4180 line and returns a list with the
    values of each of the comma separated fields.
    """

    literal = False
    preceding_quotes = False
    current_field = ""
    fields = []

    for char in list(line):
        if literal:
            if (char == '"') and (preceding_quotes is True):
                current_field += char
                preceding_quotes = False
            elif (char == '"') and (preceding_quotes is False):
                preceding_quotes = True
            elif (char != '"') and (preceding_quotes is True):
                literal = False
                preceding_quotes = False
            elif (char != '"') and (preceding_quotes is False):
                current_field += char

        if not literal:
            if char == '"':
                literal = True
            elif char == ',':
                fields.append(current_field)
                current_field = ""
            else:
                current_field += char

    if current_field.endswith("\n"):
        current_field = current_field[:-1]
    fields.append(current_field)

    return fields


def csvify_list(list):
    """
    Given a list as an argument, convert it into a CSV line. The list given as
    an argument should be well formatted (the strings should be quoted),
    otherwise, this might end up producing an ambiguous string because of the
    commas
    """

    csv_line = ""

    for item in list:
        csv_line = csv_line + item + ","

    csv_line = csv_line[:-1]

    return csv_line


def get_csv_line(header, csv_file, header_typing=None):
    """
    The program gets a CSV file (header + body) and another header. The
    code compares every field in the separated header (one by one, in order)
    with the data in CSV. If the data appears in the CSV file, it is appended
    in the corresponding order to a line filled with comma-separated values. If
    the information about that field doesn't appear in the file, a blank
    field is appended to the line.
    This way, a line is built with all the interesting information (defined by
    the header) from the CSV file and in an order coherent with the one
    defined at the header.
    This is very useful to generate lines that are appendable to CSVs defined
    by a CSV header.
    """

    file_header, file_body = csv_file.strip().split("\n")

    header_fields = format_csv.split_csv_line(header)
    file_header_fields = format_csv.split_csv_line(file_header)
    file_body_fields = format_csv.split_csv_line(file_body)
    new_csv_line = ""

    for header_field in header_fields:
        match = False
        for file_header_field in file_header_fields:
            if header_field == file_header_field:
                pos = file_header_fields.index(file_header_field)
                new_csv_line += format_RFC4180(file_body_fields[pos]) + ','
                match = True

        if not match:
            if header_typing is not None and header_typing[header_field] == "bool":
                new_csv_line += '"False",'
            else:
                new_csv_line += '"",'

    new_csv_line = new_csv_line[:-1]

    return new_csv_line


def format_RFC4180(original_value):
    """
    Transform the value from the key-value pairs of a flattened JSON in
    RFC4180-compliant. This is, remove "None" values and duplicate inner
    double quotes.
    Added removal of newlines and carriage returns, which are really
    troublesome in CSVs
    """

    new_value = str(original_value).strip().replace('"', '""')
    new_value = new_value.replace("\n", " ")
    new_value = new_value.replace("\r", " ")
    new_value = new_value.replace("None", "")
    new_value = '"' + new_value + '"'

    return new_value
