""" Функции для терминала CAS"""


def get_parsed_input_data(data):
    # Парсер для весового терминала CAS
    data = str(data)  # .decode()
    try:
        data_els = data.split(',')
        data_kg = data_els[3]
        data_kg_els = data_kg.split(' ')
        kg = data_kg_els[7]
        return kg
    except:
        return False


def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    data = str(data)
    if 'x00' in data:
        return True