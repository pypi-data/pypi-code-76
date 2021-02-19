__all__ = ["print_variables"]


def print_variables(sep=', ', association=" = ", *args, **kwargs):
    r""" Easy function to visualise variables in development

    Usage:

    .. code-block:: python

        x = 5
        y = 10
        string_pos = "({}, {})".format(x, y)
        print_variables(x=x, y=y, location=string_pos) # Output -> 'X = 5, Y = 10, Location = (5, 10)'

    Args:
        sep: How to separate different parameters e.g ", " -> "v1=1, v2=2" or "\\n" -> r"v1=1\\nv2=2"
        association: The link between variable names and values, default is equality (" = ") e.g v1_name = v1_value
        *args: Optional Arguments to pass to the print function
        **kwargs: The keyword value list passed to the print variable function

    """
    print_string = sep.join(["{}{}{}".format(
        ' '.join(map(lambda x: x[0].upper() + x[1:].lower(), k.split('_'))), association, v)
        for k, v in kwargs.items()])
    print(print_string, *args)
