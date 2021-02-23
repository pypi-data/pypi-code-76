from paramga.encoding import decode_parameters, encode_parameters
import random


def combine_param_state(param_a, param_b):
    encoded_param_a = encode_parameters(param_a)
    encoded_param_b = encode_parameters(param_b)
    number_of_params = len(encoded_param_a)
    k1 = random.randint(0, number_of_params-1)
    k2 = random.randint(0, number_of_params-1)

    pa = encoded_param_a[0:k1] if k1 < k2 else encoded_param_b[0:k2]
    pb = encoded_param_a[k1:k2] if k1 < k2 else encoded_param_b[k2: k1]
    pc = encoded_param_a[k2:] if k1 < k2 else encoded_param_b[k1:]

    new_encoded_param = pa + pb + pc
    new_param = decode_parameters(new_encoded_param)
    return new_param
