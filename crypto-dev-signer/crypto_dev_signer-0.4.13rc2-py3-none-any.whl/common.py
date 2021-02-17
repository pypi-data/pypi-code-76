def strip_hex_prefix(hx):
    if hx[:2] == '0x':
        return hx[2:]
    return hx

def add_hex_prefix(hx):
    if len(hx) < 2:
        return hx
    if hx[:2] != '0x':
        return '0x' + hx
    return hx
