from monkey_vision.app.math.utils import calc_distance, calc_center_of_shape
from monkey_vision.app.math.union_find import union, find, connected

"""
Disjoint Set Union (Union Find)
--------------------------------------------------------------------------------
"""

# --------------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------------
MAX_DISTANCE_FROM_GROUP_CENTER = 100
ACCEPTED_DISTANCE = 30

# Step 1
# construct a bijection (a mapping) between the coordinates and integers in range [0, n).
# this will allow an array based union find, easy to work with.
# Assume data_set contains the provided coordinates in order.
# for this array lets create an index based bijection using the following array.
# data[i] points to the parent of i, if data[i] = i then i is a root node
data = []


# structure of an item {root: _index_, center: _coordinate_, items: [ _coordinate1_, _coordinate2_ ] }
groups = []

# --------------------------------------------------------------------------------

# Build prerequisites of grouping data_set points


def build_prerequisites(data_set):
    global data
    data_set_length = len(data_set)
    data = [None] * data_set_length
    for index, value in enumerate(data_set):
        data[index] = index


# --------------------------------------------------------------------------------
# HELPER METHODS
# --------------------------------------------------------------------------------


def get_nearby_groups(index, data_set):
    """
    Get indexes of the groups that complete the MAX_DISTANCE_FROM_GROUP_CENTER criteria.
    """
    nearby = []
    for i in range(0, len(groups)):
        g_center = groups[i]["center"]
        coord = data_set[index]
        if calc_distance(coord, g_center) <= MAX_DISTANCE_FROM_GROUP_CENTER:
            nearby.append(i)
    return nearby


def can_unify_with_group(coordinate, group):
    groupItems = group["items"]
    for item in groupItems:
        if calc_distance(coordinate, item) <= ACCEPTED_DISTANCE:
            return True


# --------------------------------------------------------------------------------

# Connection criteria.
# Loop through all the available coordinates in the data_set.
# For each group of coordinates keep a record of the center location of the entire group,
# calculated by the cartesian center of the connected coordinates.
# If a coordinate is closer than a disstance X from the center of the group,
# try to find the closest coodinate, and if a coordinate is found within the accepted range of the coordinates beeing part of the same interface  unit,
# then this coordinate is connected to the group. Consider the fact that a coordinate can be close enough multiple groups


def group_coordinates(data_set):
    global data, groups
    build_prerequisites(data_set)
    for item in data:
        nearby_group_indexes = get_nearby_groups(item, data_set)
        # coordinate from the original data_set
        coordinate = data_set[item]
        if len(nearby_group_indexes) == 0:
            # create new group
            groups.append(
                {"root": item, "center": coordinate, "items": [coordinate]}
            )
            continue  # go to next loop

        for group_index in nearby_group_indexes:
            focused_group = groups[group_index]
            if can_unify_with_group(coordinate, focused_group):
                union(data, focused_group["root"], item)
                updated_group_items = focused_group["items"]
                updated_group_items.append(coordinate)
                groups[group_index] = {
                    "root": focused_group["root"],
                    "center": calc_center_of_shape(updated_group_items),
                    "items": updated_group_items,
                }

    return groups
