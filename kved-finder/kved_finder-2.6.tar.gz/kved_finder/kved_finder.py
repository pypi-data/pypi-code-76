import json
import argparse
import requests


def read_file(file_path) -> dict:
    '''
    Reads json file and returns it parsed
    '''
    with open(file_path) as f:
        return json.load(f)


def get_kved_data():
    response = requests.request(
        'GET',
        url='https://data.gov.ua/dataset/f8a741b9-af17-48e2-8178-8e161c244549/resource/878a36b5-31af-4c36-86e6-5dbf432e9331/download/kved.json')
    return response.json()


def find(func, values):
    '''
    Returns first value in values that matches a criterion
    '''
    for value in values:
        if func(value):
            return value


def parse_kved(classCode: str, kved_obj=None):
    '''
    Parses kved tree and writes results to kved_result.json
    '''
    divisionCode = classCode.split('.')[0]
    groupCode = classCode[:-1]

    if not kved_obj:
        kved_obj = get_kved_data()
    for section in kved_obj['sections'][0]:
        divisions = section['divisions']
        division = find(lambda i: i['divisionCode'] == divisionCode, divisions)

        if not division:
            continue

        groups = division['groups']
        group = find(lambda i: i['groupCode'] == groupCode, groups)

        if not group:
            continue

        classes = group['classes']
        class_name = find(lambda i: i['classCode'] == classCode, classes)['className']

        if class_name:
            break

    result = {
        "name": class_name,
        "type": "class",
        "parent": {
            "name": group['groupName'],
            "type": "group",
            "num_children": len(group['classes']),
            "parent": {
                "name": division['divisionName'],
                "type": "division",
                "num_children": len(division['groups']),
                "parent": {
                    "name": section['sectionName'],
                    "type": "section",
                    "num_children": len(section['divisions'])
                }
            }
        }
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kved', help='kved you want to find (example: 01.11)', type=str)
    parser.add_argument('-s', '--source_file', help='Where your kved.json is located', type=str, action='store')
    parser.add_argument('-d', '--destination_file',
                        help='Where should the results be written to', type=str, action="store")
    args = vars(parser.parse_args())

    kved_obj = None
    if args['source_file']:
        kved_obj = read_file(args['source_file'])

    result = parse_kved(args['kved'], kved_obj)

    destination_file = 'kved_result.json'
    if args['destination_file']:
        destination_file = args['destination_file']

    with open(destination_file, 'w') as file:
        json.dump(result, file, indent=2, ensure_ascii=False)
