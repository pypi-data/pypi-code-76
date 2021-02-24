def calculate_etaa(dataframe, et, eta):
    result = (1 - (abs(dataframe[str(et)] - dataframe[str(eta)])
                   / dataframe[str(et)])) * 100.0
    result[result < 0] = 0
    return result
