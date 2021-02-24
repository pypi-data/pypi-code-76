import random

def gen_param(size):
    mapping = list(range(size))
    random.shuffle(mapping)
    ops = list(random.choices(range(7),k=size))
    return {"mapping":mapping, "ops":ops}
    
def fold(value, new_size, mapping, ops):
    assert type(value) == str, "value must be string"
    assert len(mapping) == len(ops), "mapping and ops must have same value"
    value_int = 0
    value_rev = value[::-1]
    for i in range(len(value)):
        value_int = value_int * 256
        value_int += ord(value_rev[i])
    x = bin(value_int)
    x = x[2:len(x)]
    assert len(x) >= new_size, "new_size is too large for provided value"
    assert len(mapping) >= len(x), "mapping and ops lists are too small for provided value"
    if len(x) < len(mapping):
        x = "0"*(len(mapping)-len(x))+x
    result = ""
    for i in range(new_size):
        next_bit = int(x[i])
        j = 1
        while j*new_size+i < len(x):
            next_bit = transform(next_bit, int(x[j*new_size+i]), ops[j*new_size+i])
            j += 1
        result += str(next_bit)
    result_int = int(result,2)
    result_str = ""
    while result_int > 0:
        result_str += chr(result_int % 256)
        result_int = result_int // 256
    return result_str

def transform(bit1, bit2, op):
    if op == 0:
        return bit1
    elif op == 1:
        return bit2
    elif op == 2:
        return bit1 and bit2
    elif op == 3:
        return bit1 or bit2
    elif op == 4:
        return bit1^bit2
    elif op == 5:
        return (bit1^bit2) and bit1
    elif op == 6:
        return (bit1^bit2) and bit2