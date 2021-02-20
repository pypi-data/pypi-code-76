def fix_python_code(python_text):
    """Reformats Python source to correct some formatting issues.

    Python code copied & pasted or extracted from HTML page may be incorrectly formatted.
    This function attempts to fix the following:

      - proper indentation of the whole code
      - removes double quote characters on both ends of the text
    """
    python_text.replace('\t', ' ').strip('"')
    lines = python_text.split("\n")
    i = 0
    while lines[i].find("import") == -1: i += 1
    n_spaces = len(lines[i]) - len(lines[i].lstrip())
    out = ""
    for l in lines:
        out += l[n_spaces:] + "\n"
    return out


def consecutive_find(string, shortest_accepted=2, allowed_chars=[]):
    """Detects ranges of identical characters in a given string

    :param string: input string
    :param shortest_accepted: shortest substring accepted
    :param allowed_chars: list of allowed characters: the returned list will hold a given block if and only if
    its character is on the list; when the list is empty, all characters are allowed
    :return: a list of segments defining substrings of identical characters
    """

    current = 0
    next = 0
    i_start = 0
    list_of_blocks = []
    while True:
        next += 1
        while next != len(string) and string[current] == string[next]:
            current += 1
            next += 1

        if current - i_start + 1 >= shortest_accepted:
            if len(allowed_chars) == 0 or string[current] in allowed_chars:
                list_of_blocks.append([i_start,current,string[current]])
        current += 1
        i_start = current

        if next == len(string):
          return list_of_blocks


def substitute_template(template, subst_dict):
    """Simple text template replacement utility

    :param template: a template string
    :param subst_dict: dictionary of template_key:replacement pairs
    :return: result of all substitutions
    """
    for key, val in subst_dict.items():
        template = template.replace(key, str(val))

    return template


def from_string(text, first, last, default):
    """ Simple text extractor with a default value.

    Extracts a substring of a given string and trims white characters from the extracted part. If the result
    is an empty string (i.e. there were no meaningful characters in the given region), the default value is returned

    :param text: (``string``) a source string
    :param first: (``int``) the index of the first character to be extracted
    :param last:  (``int``) the index of the position behind the last character to be extracted
    :param default: a value returned when an empty string is extracted
    :return: a substring or the given default
    """
    s = text[first:last].strip()
    return s if len(s) > 0 else default


def detect_blocks(secondary_str,allowed_characters=['H','E','C','L']):
        """Detects secondary structure blocks (segments)

        Returns three lists, that contain helices, strands and loops (H, E and C elements)
        :param allowed_characters: defines what to be detected, e.g. ``['H','E']`` detects only helices and strands
        (``E`` for extended)

        :param which_seq: (``int``) index of the sequence where secondary structure blocks will be detected (from 1!)
        :param allowed_characters: characters that denote a secondary structure element
        :return: three list of SSEs: for H, E and C, respectively. Each list of SSEs comprises (from, to) two-tuple
            of integer indexes to define an SSE location in the given secondary structure string
        """
        
        H, E, C = [], [], []
        for block in consecutive_find(secondary_str, 2, allowed_characters):
            if block[2] == 'H': H.append([block[0], block[1]])
            elif block[2] == 'E': E.append([block[0], block[1]])
            elif block[2] == 'C' or block[2] == 'L' : C.append([block[0], block[1]])

        return {'H':H, "E":E,"C": C}
