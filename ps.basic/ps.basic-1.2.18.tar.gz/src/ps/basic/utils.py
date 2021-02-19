def get_html_string(var_p: dict):
    """[summary]

    Return html table structure for a dictionaries structure. Makes it easy
    to display dictionaries in log output messages.

    :param var_p: [description]
    :type var_p: dict
    :return: [str]
    :rtype: [type]

    >>> get_html_string({"A":"B"})
    '<table><tr><td>A</td><td>B</td></tr></table>'
    """
    html_string = "<table>"
    for name, value in var_p.items():
        if type(value) is dict:
            html_string += "<tr><td>%s</td><td>%s</td></tr>" % (
                str(name),
                get_html_string(value),
            )
        else:
            html_string += "<tr><td>%s</td><td>%s</td></tr>" % (
                str(name),
                str(value),
            )

    html_string += "</table>"
    return html_string


def hms_string(sec_elapsed: int):
    """[summary]

    Return the hour:minute:seconds for a period in seconds.

    :param sec_elapsed: [description]
    :type sec_elapsed: int
    :return: [description]
    :rtype: [type]

    >>> hms_string(600)
    '00:10:00'

    """
    h = int(sec_elapsed / (60 * 60))
    m = int(sec_elapsed % (60 * 60) / 60)
    s = sec_elapsed % 60
    return "%02d:%02d:%02d" % (h, m, s)
