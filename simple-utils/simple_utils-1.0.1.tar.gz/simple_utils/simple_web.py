import json
import base64


def python_vars_to_javascript(python_vars: dict, without_script_tag=False):
    script = ""
    if not without_script_tag:
        script += "<script>"
    script_piece = ""
    for var_name in python_vars:
        value = python_vars[var_name]

        value = json.dumps(value, ensure_ascii=False, default=str)
        encoded_value = base64.b64encode(value.encode("utf-8"))

        script_piece += "var %s = b64DecodeUnicode('%s');\n" % (
            var_name, encoded_value.decode())

        script_piece += "%s = JSON.parse(%s);\n" % (var_name, var_name)

    script += """
        function b64DecodeUnicode(str) {
            return decodeURIComponent(atob(str).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
        }
    """
    script += script_piece
    if not without_script_tag:
        script += "</script>"

    return script

