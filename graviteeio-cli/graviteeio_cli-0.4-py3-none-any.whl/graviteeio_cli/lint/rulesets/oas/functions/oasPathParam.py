import re

from graviteeio_cli.lint.types.function_result import FunctionResult

pathRegex = "{[a-zA-Z0-9_-]+}"


def oasPathParam(value, **kwargs):
    """
    This function verifies:
    1. Operations must have unique `name` + `in` parameters.
    2. Operation cannot have both `in:body` and `in:formData` parameters
    3. Operation must have only one `in:body` parameter.
    """
    toReturn = []

    if not value["paths"]:
        return toReturn

    uniquePaths = {}
    validOperationKeys = ['get', 'head', 'post', 'put', 'patch', 'delete', 'options', 'trace']

    for path in value["paths"]:

        normalized = re.sub(pathRegex, "{}", path)
        if normalized in uniquePaths:
            toReturn.append(FunctionResult(
                "The operation does not define the parameter [{}] expected by path [{}].".format(uniquePaths[normalized], path),
                path=["paths", path]
            ))
        else:
            uniquePaths[normalized] = path

    if type(value) is not list or len(value) < 0:
        return

    count = {
        "body": [],
        "formdat": []
    }

    list_param = []
    duplicates = []

    for index, param in enumerate(value):
        if type(param) is not dict: continue
        if "$ref" in param: continue

        fingerprint = computeFingerprint(param)
        if fingerprint in list_param:
            duplicates.append(index)
        else:
            list_param.append(fingerprint)

        if param["in"] in count:
            count[param["in"]].append(index)

    if len(duplicates) > 0:
        for i in duplicates:
            toReturn.append(FunctionResult(
                "A parameter in this operation already exposes the same combination of `name` and `in` values."
            ))

    if len(count["body"]) > 0 and len(count["formData"]) > 0:
        toReturn.append(FunctionResult(
                "Operation cannot have both `in:body` and `in:formData` parameters."
        ))

    if len(count["body"]) > 1:
        for index, _ in enumerate(count, start=1):
            toReturn.append(FunctionResult(
                "Operation has already at least one instance of the `in:body` parameter."
            ))

    return toReturn
