# keep original structure
# so self ids can be found in peace

def structure_rebuilder(path, node):
    """take path and transform it to preserve original document structure

    :return: str
    """
    # generate select =  statement

    dict_path = ".".join([e + ' | ' for e in path.split('.')[:-1]])[3:]
    self_formula = '{}select({}=="{}")'.format(dict_path, "." + path.split('.')[-1:][0], node)


    alsopath = path.split('.')[:-1]
    half_1 = ''
    half_2 = ''
    for element in alsopath:
        if element == '':
            # casue by leading point. ignore
            pass
        elif element == '[]':
            # we'll need an opening
            half_1 += '['
            # and a closer
            half_2 = ']' + half_2
        elif element.endswith('[]'):
            # we've come across a named list!
            half_1 += '{"' + element.replace('[]', '') + '":['
            half_2 = ']}' + half_2
            pass
        else:
            # this must be a dict
            half_1 += '{'
            half_2 = '}' + half_2

    return '{}({}){}'.format(half_1, self_formula, half_2)

# path = [".{}".format(e) if type(e) == type("") else "[]" for e in path]
path =  ".[].Subnets[].VpcId"
node = 'vpc-820adceb'
print(structure_rebuilder(path, node))