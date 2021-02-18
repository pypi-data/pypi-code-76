import os


def clean(path):
    cache = list()
    with open(path, 'r') as f:
        for i in f.readlines():
            if '@debug' in i or 'd_print' in i:
                continue
            else:
                cache.append(i)
    result = ''.join(cache)
    directory, file_name = os.path.split(path)
    new_name = f'cleaned_{file_name}'
    new_path = f'{directory}\\{new_name}'
    with open(new_path, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    clean('.\\cache.py')
