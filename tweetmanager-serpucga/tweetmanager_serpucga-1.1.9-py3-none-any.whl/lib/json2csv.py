import os
import re
import json

from .format_csv import format_RFC4180

#############################
#     LIBRARY FUNCTIONS     #
#############################


def split_collection(filename, output_dir):
    """
    This function receives a filename as argument. For this function to
    perform correctly, the file should be a collection of JSON objects,
    for example a large group of tweets.
    The function will split and write as separate files each one of
    these JSON objects.

    Return the root dir for the collection of split files
    """

    newfile_counter = 0

    # Open and read the collection
    with open(filename) as json_object:
        json_text = json_object.read()

    # Call an algorithm to identify all the points that separate the
    # individual JSON objects in the text
    opening_braces, closing_braces = identify_split_points(json_text)

    # Write every single tweet to a new, isolated JSON file
    while opening_braces:
        beginfile = opening_braces.pop(0)
        endfile = closing_braces.pop(0) + 1

        with open(
            output_dir + os.path.sep + str(newfile_counter) + ".json", "w"
        ) as newfile:

            newfile.write(json_text[beginfile:endfile])

        newfile_counter += 1

    return output_dir


def flatten_file(filename, output_dir, is_collection=False):
    """
    Given a single filename for a JSON file, flatten it.
    This basically adds input/output management to the
    "flatten" function.

    Returns the path for the flattened file
    """

    # Use regex to check that file is JSON and get its basename and ext
    matchObj = re.search(r".*[/\\](.*)(\.json)$", filename)
    if not matchObj:
        raise WrongFiletypeException("File selected is not JSON")

    with open(filename) as json_file:
        text_json_file = json.load(json_file)

    # Use the algorithm to build a flattened JSON
    flat_json = {}
    flatten("", text_json_file, flat_json)

    # Create the necessary directories to make a by-date classification
    # Apply only if treating with a collection and not a single file
    if is_collection:

        # Use regex to capture the elements (day, month, year) of the date
        # when the tweet was created
        matchObj_dates = re.search(
            r"'created_at(?:\.\$date)?': '(\d{4})-(\d{2})-(\d{2})", str(flat_json)
        )

        date = None
        # If file is a tweet and has a date create the date structure
        if matchObj is not None:
            year = matchObj_dates.group(1)
            month = matchObj_dates.group(2)
            day = matchObj_dates.group(3)
            date = (year, month, day)
        else:
            pass

        output_dir_date = mkdir_tweet_date(date, output_dir)
        newname = matchObj.group(1) + matchObj.group(2)
    else:
        output_dir_date = output_dir
        newname = matchObj.group(1) + "_flat" + matchObj.group(2)

    # Write a new JSON file
    output_path = os.path.join(output_dir_date, newname)
    with open(output_path, "w") as output_file:
        json.dump(flat_json, output_file)

    return output_path


def flatten_dir_files(directory, output_dir):
    """
    Given the name of a directory which contains one or more JSON files,
    flatten all of them.

    Returns the root dir for the collection of flattened files
    """

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            flatten_file(file_path, output_dir, True)

    return output_dir


def convert_json2csv(
    flattened_json,
    output_path,
    array_compression,
    compression_depth,
    remove_dollars,
    include_list=[],
    exclude_list=[],
):
    """
    This function will convert from a JSON object to a CSV one. However,
    this was thought for JSONs that have been previously flattened and
    are thus just a dictionary of key-value pairs.
    Returns the resulting CSV in String form.
    The optional include and exclude lists act as filters.

    Returns the path to the new CSV file.
    """

    # Check file is JSON and get the basename
    matchObj = re.search(r".*/(.*).json$", flattened_json)
    if not matchObj:
        raise WrongFiletypeException("File selected is not JSON")

    # Remove the string "_flat" if that was added and compose new name
    matchObj2 = re.search(r"(.*)_flat$", matchObj.group(1))
    if matchObj2:
        newname = matchObj2.group(1) + ".csv"
    else:
        newname = matchObj.group(1) + ".csv"

    # Load the flattened JSON to make it ready to use
    with open(flattened_json) as json_object:
        json_file = json.load(json_object)

    # Apply the conversion algorithm
    csv_file = json2csv(
        json_file,
        array_compression,
        compression_depth,
        remove_dollars,
        include_list,
        exclude_list,
    )

    # Finally write the contents to a newfile
    output_path = os.path.join(output_path, newname)
    if os.path.isfile(output_path):
        raise OSError(output_path)
    else:
        with open(output_path, "w") as output_file:
            output_file.write(csv_file)

    return output_path


def convert_dir_json2csv(
    input_dir,
    output_dir,
    array_compression,
    compression_depth,
    remove_dollars,
    include_list=[],
    exclude_list=[],
    first_call=True,
):
    """
    Given the name of a directory which contains one or more JSON files,
    recursively access all of them and call the converter for each file

    Returns the root directory of the new collection of files
    """

    # Copy the current directory. In case it already exists, simply
    # ignore it (don't overwrite) and proceed with execution
    if not first_call:
        input_dir = os.path.normpath(input_dir)
        newdir_name = os.path.split(input_dir)[1]
        output_dir = os.path.join(output_dir, newdir_name)
        try:
            os.mkdir(output_dir)
        except OSError:
            pass

    # Apply recursively to all the subdirectories
    for element in os.listdir(input_dir):
        nextelement = os.path.join(input_dir, element)
        if os.path.isdir(nextelement):
            convert_dir_json2csv(
                nextelement,
                output_dir,
                array_compression,
                compression_depth,
                remove_dollars,
                include_list,
                exclude_list,
                False,
            )

        elif os.path.isfile(nextelement):
            try:
                convert_json2csv(
                    nextelement,
                    output_dir,
                    array_compression,
                    compression_depth,
                    remove_dollars,
                    include_list,
                    exclude_list,
                )

            except WrongFiletypeException as e:
                raise type(e)(output_dir)
            except NotFlattenedException as e:
                raise type(e)(output_dir)

    return output_dir


def flatten_dictionary(dict_object):
    """
    This definition is simply a wrapper for the 'flatten' function, which
    contains the real algorithm. However, flatten requires a string and a
    dictionary as arguments, which are usually empty in the original function
    call but are required nonetheless because of its recursive nature.
    Furthermore, the flatten function doesn't return the flattened json, but
    instead it is stored in the originally empty dictionary passed as argument.

    This 'flatten_dictionary' function offers a more straightforward and clean
    call: just pass a JSON dictionary as argument and get the flattened version
    with a return.
    """

    flat_dictionary = {}
    name = ""

    flatten(name, dict_object, flat_dictionary)

    return flat_dictionary


#############################
#        ALGORITHMS         #
#############################


def identify_split_points(json_collection):
    """
    Given a collection of JSON objects, return a list with the position
    of all the initial and ending braces to permit an easy splitting
    """

    brace_level = 0
    char_counter = 0
    escaped = False
    quoted_single = False
    quoted_double = False
    open_braces = []
    close_braces = []

    # Go over every character of the text
    for line in json_collection:
        for char in line:
            # If character is marked as escaped ignore it
            if escaped:
                escaped = False
            else:
                # Backslash escapes next char
                if char == "\\":
                    escaped = True
                else:
                    # Non-escaped quotes mean quoted text
                    if (char == '"') and (not quoted_single):
                        quoted_double = not quoted_double
                    elif (char == "'") and (not quoted_double):
                        quoted_single = not quoted_single

                    # Outside quoted or escaped text, count braces and
                    # add the position of those not nested
                    elif (quoted_single or quoted_double) is False:
                        if char == "{":
                            if brace_level == 0:
                                open_braces.append(char_counter)
                            brace_level += 1
                        elif char == "}":
                            brace_level -= 1
                            if brace_level == 0:
                                close_braces.append(char_counter)

            char_counter += 1

    if len(open_braces) != len(close_braces):
        raise SyntaxError("Opening and closing braces should match in number.")

    return (open_braces, close_braces)


def flatten(name, json_object, flat_json):
    """
    This algorithm takes 2 arguments: a name and a JSON structure (which
    must be composed of key-value pairs where the value may be a
    dictionary, an array or a single elements) and a flattened JSON
    structure, which is what we want to complete.

    The algorithm descends recursively through the nested tree structure
    or the original json_object, and in each recursion it passes a new
    name (composed of the base name + the path to the current subtree)
    and the remaining subtree.

    Once the leaves of the tree (that is, the key-value pairs where the
    value is a single element) are found, a new key-value pair is added
    to the flattened JSON structure. The new key will be the complex
    name composed of a dot-notation path to the element, and the value
    will be the single value found.

    Dictionary elements follow the dot notation and array elements are
    ordered by subindexes: a[0], a[1]...

    A random example of new key-value pair would be:
        city.neighborhoood.house[3].owner = "John Smith"
    """
    # If item is a dictionary add the keys with point notation and pass
    # the values recursively
    if type(json_object) is dict:
        for key, value in json_object.items():
            if name == "":
                subname = key
            else:
                subname = name + "." + key
            flatten(subname, value, flat_json)

    # If item is array add the subitems with [i] notation and pass the
    # contents recursively
    elif type(json_object) is list:
        i = 0
        for item in json_object:
            subname = name + "[" + str(i) + "]"
            i += 1
            flatten(subname, item, flat_json)

    # If item is a simple value, add key-value pair to the dictionary
    else:
        flat_json[name] = json_object


def json2csv(
    json_file,
    array_compression,
    compression_depth,
    remove_dollars,
    include_list=[],
    exclude_list=[],
    check_flat=True,
):
    """
    Loop through all the items of the JSON file. For each one add the
    key to the header and the value to the body, and add a comma to
    separate it from the next one.
    In the case of the items part of an array, group them in lists
    If include_list is non-empty, apply the filter to only include
    matched elements. Else, if exclude_list is non-empty, exclude the
    matches. If both are empty, just apply full conversion.
    """

    header = ""
    body = ""
    csv_file = ""
    buffer_keys = []
    buffer_values = []

    # If there is a non-empty include list, ignore the exclude list and
    # write just the key-value pairs that appear in the include list
    if include_list:
        for key, value in json_file.items():

            if remove_dollars:
                key = remove_dollarsign(key)
            # For each key-value that matches the filter
            if any(regex.search(str(key)) for regex in include_list):

                # Make the value RFC4180 compliant
                if check_flat:
                    check_flattened(value)
                formatted_value = format_RFC4180(value)

                # Check if key belongs to array in array compression mode
                matchObj = re.search(r"^(.*)\[\d+\]((?:.(?!\[\d+\]))*)$", str(key))
                if (array_compression) and (matchObj is not None):
                    buffer_keys.append(key)
                    buffer_values.append('"' + formatted_value + '"')

                # If the key is a single value, just add to the CSV
                else:
                    header, body = add_key_value_pair(
                        key, formatted_value, header, body
                    )

    # If there isn't a include list, write all the key-value pairs
    # excepting those that appear in the exclude list
    # If the exclude list were empty too, simply all the elements would
    # be written
    else:
        for key, value in json_file.items():
            if remove_dollars:
                key = remove_dollarsign(key)

            if not any(regex.search(str(key)) for regex in exclude_list):
                if check_flat:
                    check_flattened(value)
                formatted_value = format_RFC4180(value)
                matchObj = re.search(r"^(.*)\[\d+\]((?:.(?!\[\d+\]))*)$", str(key))
                if (array_compression) and (matchObj is not None):
                    buffer_keys.append(key)
                    buffer_values.append('"' + formatted_value + '"')
                else:
                    header, body = add_key_value_pair(
                        key, formatted_value, header, body
                    )

    if array_compression:
        key_value_pairs = sorted(
            list(zip(buffer_keys, buffer_values)), key=lambda pair: pair[0]
        )
        for i in range(compression_depth):
            key_value_pairs, header, body = compress_array(
                key_value_pairs, header, body
            )

        for i in range(len(key_value_pairs)):
            header, body = add_key_value_pair(
                key_value_pairs[i][0], '"' + key_value_pairs[i][1] + '"', header, body
            )

    # Remove the last comma from header and body and separate both with
    # a newline. Then compose the CSV
    header = header[:-1] + "\n"
    body = body[:-1]
    csv_file = header + body

    return csv_file


#############################
#      LOCAL FUNCTIONS      #
#############################


def mkdir_tweet_date(date, output_dir):
    """
    Given a tweet (an already flattened JSON) find the date of that
    tweet and create an adequate path in order to locate the new
    flattened file
    """

    # If file is a tweet and has a date create the date structure
    if date is not None:
        year = date[0]
        month = date[1]
        day = date[2]

        try:
            os.mkdir(os.path.join(output_dir, year))
        except OSError:
            pass
        try:
            os.mkdir(os.path.join(output_dir, year, month))
        except OSError:
            pass
        try:
            os.mkdir(os.path.join(output_dir, year, month, day))
        except OSError:
            pass

        filepath = os.path.join(output_dir, year, month, day)

    else:
        filepath = output_dir

    return filepath


def remove_dollarsign(key):
    """
    Remove the $like additions introduced by Mongo, as in
    "created_at.$date".
    This is an abnormality, and should not be activated in
    normal working mode.
    """

    matchObj = re.search(r"^(.*)(\.\$.*)$", str(key))
    if matchObj is not None:
        key = matchObj.group(1)

    return key


def add_key_value_pair(key, value, header, body):
    """
    Given a key and a value, add them to the header and the body of the
    new CSV object
    """

    header += str(key) + ","
    body += str(value) + ","

    return (header, body)


def check_flattened(value):
    """
    Check if any value contains a nested dictionary, matching the
    following pattern (discarding whitespaces and with single or
    double quotes accepted):
    {'key':'value'}
    """

    nested_dictionary = re.compile(r'^\s*\{\s*[\'"].*[\'"]\s*:\s*[\'"].*[\'"]\s*\}')

    if nested_dictionary.search(str(value)):
        raise NotFlattenedException("Seems like this file has not been flattened")


def compress_array(key_value_pairs, header, body):
    """
    Management of the array-form elements. The keys with the pattern 'name[0]'
    are flattened so the bracket part disappears and the values are compressed
    in a single list
    """

    array_keys = []
    array_values = []
    index = 0

    for i in range(len(key_value_pairs)):
        matchObj = re.search(
            r"^(.*)\[\d+\]((?:.(?!\[\d+\]))*)$", str(key_value_pairs[i][0])
        )

        if matchObj is not None:
            new_key = str(matchObj.group(1)) + str(matchObj.group(2))
            if new_key not in array_keys:
                array_keys.append(new_key)
                array_values.append("[" + key_value_pairs[i][1])
            elif new_key in array_keys:
                index = array_keys.index(new_key)
                array_values[index] += ", " + key_value_pairs[i][1]

        else:
            header, body = add_key_value_pair(
                key_value_pairs[i][0], '"' + key_value_pairs[i][1] + '"', header, body
            )

    for i in range(len(array_values)):
        array_values[i] += "]"

    return (list(zip(array_keys, array_values)), header, body)


class WrongFiletypeException(Exception):
    pass


class NotFlattenedException(Exception):
    pass
