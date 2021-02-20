
def ansible_get_line_kwargs(kwargs):
    """
    把dict转换成 -e key=value 这种格式
    Args:
        kwargs (dict): 需要转化的参数
    Returns:
        str: eg `-e name=hello -e port=8000`
    """
    assert isinstance(kwargs, dict)
    li = []
    for key, value in kwargs.items():
        li.append("-e {}={}".format(key, value))
    return " ".join(li)
