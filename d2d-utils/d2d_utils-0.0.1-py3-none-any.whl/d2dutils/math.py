########################################################################
def clamp(value, minimum=0.0, maximum=1.0):
    return min(maximum, max(minimum, value))
