def sortTextAreas(text_areas):
    """
    Method to sort provided text areas by using the quick sort algorithm.
    Sorting is based on the Y coordinate of the starting point of each text area.
    :param text_areas: Array of rectangle objects representing text areas
    :return:
    """
    if text_areas is None:
        return []
    less = []
    equal = []
    greater = []
    if len(text_areas) > 1:
        pivot = text_areas[0]
        for x in text_areas:
            if x["start"][1] < pivot["start"][1]:
                less.append(x)
            elif x["start"][1] == pivot["start"][1]:
                equal.append(x)
            elif x["start"][1] > pivot["start"][1]:
                greater.append(x)
        # Just use the + operator to join lists
        return sortTextAreas(less) + equal + sortTextAreas(greater)
    # Note that you want equal not pivot
    else:
        # handle the part at the end of the recursion -
        # when you only have one element in your array, just return the array.
        return text_areas
