
def encode_parameters(param):
    return list(param.items())


def decode_parameters(param):
    return {k: v for k, v in param}
