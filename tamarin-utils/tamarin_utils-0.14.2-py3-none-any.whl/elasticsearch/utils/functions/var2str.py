import inspect


def var2str(data):
    data_type = type(data)
    if inspect.getmro(data_type).__contains__(dict):
        snake_data = {}
        for key in data:
            snake_data.update({
                str(key): var2str(
                    data.get(key)
                )
            })
    elif inspect.getmro(data_type).__contains__(list):
        snake_data = []
        for item in data:
            snake_data.append(var2str(item))
    elif inspect.getmro(data_type).__contains__(set):
        snake_data = set()
        for item in data:
            snake_data.add(var2str(item))
    else:
        snake_data = str(data)
    return snake_data
