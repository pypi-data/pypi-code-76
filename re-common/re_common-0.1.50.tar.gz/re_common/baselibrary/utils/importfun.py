def import_fun(obj, mod, m=[], modename=""):
    """
    这个方法只能在类里面设置属性
    :param obj:
    :param mod:
    :param m:
    :return:
    """
    if m:
        for item in m:
            module = getattr(mod, item)
            setattr(obj, item, module)
    elif modename:
        setattr(obj, modename, mod)
    else:
        raise ValueError("m 和　modename必须存在一个")


def import_to_val(mod, m=[], globals=None, locals=None):
    """
     设置到变量,在你调用的文件中使用
    :param mod: 一个模块对象
    :param m: 一个列表　mod 里面的变量类和函数
    :param globals: 传入　globals()
    :param locals: 传入　locals()
    :return:
    """
    dicts = {}
    for item in m:
        # module = getattr(mod, item)
        exec("{}=getattr(mod, '{}')".format(item, item))
        dicts[item] = eval(item)
        if globals:
            globals.update({item: eval(item)})
        if locals:
            locals.update({item: eval(item)})
    return dicts
