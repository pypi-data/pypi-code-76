import random

def gen_param(size):
    fold_fun = list(range(size))
    random.shuffle(fold_fun)
    ops = list(random.choices(range(7),k=size))
    return [fold_fun, ops]
    
def fold(value, new_size, mapping, ops):
    x = bin(value)
    x = x[2:len(x)]
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
    return int(result,2)

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