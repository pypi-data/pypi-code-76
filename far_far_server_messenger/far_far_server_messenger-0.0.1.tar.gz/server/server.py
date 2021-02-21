from common.vars import *

import sys
import os
import argparse
import logging
import configparser
from common.decos import Log
from server.server_core import MessageProcessor
from server.server_database import ServerDataBase
from server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

LOG_SERVER = logging.getLogger('server.app')


# парсинг запуска скрипта
@Log()
def parse_args(default_port, default_address):
    '''Парсер аргументов коммандной строки.'''
    LOG_SERVER.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    # проверяем порт
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    # проверяем адрес
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    port_listen = namespace.p
    address_listen = namespace.a
    gui_flag = namespace.no_gui
    return address_listen, port_listen, gui_flag


@Log()
def config_load():
    '''Парсер конфигурационного ini файла.'''
    config = configparser.ConfigParser()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
    # умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


def main():
    '''Основная функция'''
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = parse_args(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'])

    # Инициализации бд
    database = ServerDataBase(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file'],
        )
    )

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input(f'Введите "exit" для завершения работы сервера')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break
    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False

if __name__ == '__main__':
    main()
