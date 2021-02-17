def clear_none(a_dict):
    return {key: value for key, value in a_dict.items() if value is not None}
