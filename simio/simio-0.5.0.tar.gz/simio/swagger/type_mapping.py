import trafaret as t

__doc__ = "Module with dict for mapping trafaret types with swagger"


PYTHON_TYPE_TO_SWAGGER = {
    t.ToDate: "string",
    t.ToDateTime: "string",
    t.Date: "string",
    t.DateTime: "string",
    t.String: "string",
    t.Enum: "string",
    t.Any: "string",
    t.ToInt: "integer",
    t.ToBool: "boolean",
    t.ToDecimal: "number",
    t.ToFloat: "number",
    t.Int: "integer",
    t.Bool: "boolean",
    t.Float: "number",
    t.URL: "string",
    t.Email: "string",
    t.IP: "string",
    t.IPv4: "string",
    t.IPv6: "string",
    t.List: "array",
    t.Dict: "object",
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
}
