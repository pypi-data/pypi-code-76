def get_annotation_key(json):
    if 'annotations' in json:
        return json['annotations']
    elif 'gold_standard_annotation' in json:
        return json['gold_standard_annotation']
    return []
