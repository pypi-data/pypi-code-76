from palettable.tableau import Tableau_20


def sort_queue(queue):
    int_queue = []

    for item in queue:
        try:
            int_queue.append(int(item))
        except ValueError:
            int_queue.append(item)

    int_queue = sorted(int_queue)
    new_queue = [str(item) for item in int_queue]

    return new_queue


def get_values(entities, key):
    keys = set()
    if entities.get('gold'):
        for entity in entities['gold']:
            keys.add(entity[key])

    if entities.get('computed'):
        for entity in entities['computed']:
            keys.add(entity[key])
    return keys


def get_colors(items):
    colors = {}
    colour_idx = 0
    for sf in items:
        colors[sf] = Tableau_20.hex_colors[colour_idx]
        colour_idx = 0 if colour_idx == 19 else colour_idx + 1
    return colors


def _add_annotation_items(annotation_colors, items):
    if items:
        for item in items:
            if "annotations" in item:
                for annotation in item["annotations"]:
                    if annotation["type"] not in annotation_colors:
                        annotation_colors[annotation["type"]] = set()
                    annotation_colors[annotation["type"]].add(annotation["entity"])


def _replace_with_colors(annotation_colors):
    for annotation_type in annotation_colors.keys():
        annotation_colors[annotation_type] = get_colors(annotation_colors[annotation_type])


def get_annotation_colors(gold_items, computed_items):
    annotation_colors = {}
    _add_annotation_items(annotation_colors, gold_items)
    _add_annotation_items(annotation_colors, computed_items)
    _replace_with_colors(annotation_colors)

    return annotation_colors
