def is_two_string_array_equal(array1, array2):
    array1.sort()
    array2.sort()
    return len(array1) == len(array2) and \
        all(item in array1 for item in array2)
