

def mod_record_map(mod,
                   input_list,
                   field,
                   input_field=None):
    """
    一般用于表的关联查询,生成一个map
    比如user的detail信息 根据user_list, 提取用户id,也就是用户表的主键id, 然后在detail表里面找到user_id={user_id}的记录，然后做成一个map
        上面这个例子, mod:是Detail, input_list: userlist, input_field: id, field: user_id, 返回的是dict, key是field, value是mod的类型

    """
    if not input_list:
        return dict()
    if not isinstance(input_list[0], (str, int, float, bytes)):
        assert input_field is not None, "input_field should not be None when input_list[0] is instance of {}".format(type(input_list[0]))
        if isinstance(input_list[0], dict):
            input_list = [e[input_field] for e in input_list]
        else:
            input_list = [getattr(e, input_field) for e in input_list]
    query_set = mod.select().where([getattr(mod, field).in_ == input_list])
    return {getattr(e, field): e for e in query_set}


def mod_get_in_db_set(mod,
                      input_list,
                      field,
                      format=None):
    """
    找到input_list在数据库中存在的数据
    一般用于prepare_data里面
    用来替代:
        for name in input_name:
            if mod.get_or_none(name__eq=name):
                continue
        把多条sql转成一条

    """
    if not input_list:
        return set()

    def default_format(x):
        return getattr(x, field)
    if format is None:
        format = default_format
    query_set = mod.select().where([getattr(mod, field).in_ == input_list])
    return {format(x) for x in query_set}


def mod_record_cursor_id_between(mod, from_id, to_id,
                                 base_exression_list=None,
                                 page_size=10):
    """
    这个功能一般用户导出excel，可能要导入上w的数据，
    不使用这个的话，query_result.iterator() 第一个数据会卡住
    Args:
        from_id (int): >= from_id
        to_id (int): < to_id
        base_expression_list (list): expression_list
    """
    local_max_id = to_id
    if base_exression_list is None:
        base_exression_list = []
    while 1:
        new_query_result = mod.select().where(
            [getattr(mod, 'id') < local_max_id,
             getattr(mod, 'id') >= from_id,
             *base_exression_list]
        ).order_by(getattr(mod, 'id').desc()).paginate(0, page_size)

        if new_query_result.count() == 0:
            break

        for ele in new_query_result.iterator():
            yield ele
            local_max_id = min(local_max_id, ele.id)
