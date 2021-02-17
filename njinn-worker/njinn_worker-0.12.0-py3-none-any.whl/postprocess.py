import re
from io import BytesIO
from tokenize import tokenize, ENCODING, STRING, OP, NEWLINE, ENDMARKER
from ast import literal_eval

SET_VARIABLE = "^\\s*SET_VARIABLE\\((.*)\\)\\s*$"


def to_dict(key, value):
    """
    Creates a dict from a dot-separated path-style key and a value.

    Examples:
    "foo", "bar" => "baz"
    "foo.bar", "baz" => {"foo"{"bar":"baz}}
    """
    key_parts = key.split(".")
    result = {}
    current = result
    # create path to result
    for key_part in key_parts[:-1]:
        current = current.setdefault(key_part, {})
    # set value
    current[key_parts[-1]] = value
    return result


def postproces_output(output):
    """
    Postprocess output to extract variable declarations, allowing path style keys.

    Examples for legal variable declarations
    SET_VARIABLE('foo','bar')
    SET_VARIABLE("bar","bar bar")
    SET_VARIABLE("baz.baz","baz baz")
    """
    result = {}
    for match in re.findall(SET_VARIABLE, output, flags=re.MULTILINE):
        expr = match.strip()
        try:
            # Use python tokenizer for robust parsing including escapes
            tokens = list(tokenize(BytesIO(expr.encode("utf-8")).readline))
            toknums = [toknum for (toknum, _, _, _, _) in tokens]
            # this is how python parses '"k", "v"', or "'k', 'v'"
            if toknums != [ENCODING, STRING, OP, STRING, NEWLINE, ENDMARKER]:
                continue
            [k, op, v] = [
                tokval for (toknum, tokval, _, _, _) in tokens if toknum in [STRING, OP]
            ]
            if op != ",":
                continue
            # Strings are quoted and escaped - literal_eval takes care of that
            key = literal_eval(k)
            value = literal_eval(v)
            result.update(to_dict(key, value))
        except:
            continue
    return result
