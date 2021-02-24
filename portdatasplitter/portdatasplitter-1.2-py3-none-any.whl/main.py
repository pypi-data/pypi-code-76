import socket
import threading
from serial import Serial
import serial.tools.list_ports


class PortDataSplitter:
    """ Сервер для прослушивания порта port_name (USB, COM),
     и переотправки данных подключенным к нему клиентам (Clients)."""
    def __init__(self, ip, port, port_name='/dev/ttyUSB0', debug=False, device_name='unknown'):
        self.device_name = device_name
        self.debug = debug
        self.port_name = port_name
        self.create_server(ip, port)
        self.subscribers = []

    def get_all_connected_devices(self):
        # Показать все подключенные к этому компьютеру устройства
        ports = serial.tools.list_ports.comports()
        self.show_print('\nAll connected devices:')
        for port in ports:
            self.show_print('\t', port)
        return ports

    def get_device_name(self):
        # Вернуть заданный этому устройству имя
        return self.device_name

    def start(self):
        """ Запустить работу PortDataSplitter"""
        # Запустить параллельный поток, который будет принимать клиентов
        threading.Thread(target=self.connection_reciever_loop, args=()).start()
        # Запустить основной поток, слушаюший заданный порт и отправляющий эти данные клиентам
        self._mainloop()

    def create_server(self, ip, port):
        """ Создать сервер"""
        self.show_print('Creating PortDataSplitter server')
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind((ip, port))
        self.serv.listen(10)

    def connection_reciever_loop(self):
        # Отдельный поток, принимающий подключения и добавляющий их в список self.subscribers для дальнейшней
        # работы
        while True:
            self.show_print('\nWaiting for client...')
            conn, addr = self.serv.accept()
            self.subscribers.append(conn)
            self.show_print('\tGot new client! From IP:', conn.getpeername()[0])

    def _mainloop(self):
        # Основной цикл работы программы, слушает порт и передает данные клиентам
        self.show_print('\nMain loop has been started')
        ser = Serial(self.port_name, bytesize=8, parity='N', stopbits=1, timeout=1, baudrate=9600)
        while True:
            # Получить данные
            data = ser.readline()
            # Отправить данные
            self.send_data(data)

    def send_data(self, data, *args, **kwargs):
        # Отправить данные по клиентам
        for conn in self.subscribers:
            try:
                conn.send(data)
            except:
                # Если данные отправить клиенту не удалось, удалить клиента из списка подписчиков
                self.show_print('\tFailed to send data to client')
                self.subscribers.remove(conn)

    def make_str_tuple(self, msg):
        # Перед отправкой данных в стандартный поток вывывода форматировать
        return ' '.join(map(str, msg))

    def show_print(self, *msg, debug=False):
        # Отправка данных в стандартный поток выводы
        msg = self.make_str_tuple(msg)
        if debug and self.debug:
            print(msg)
        elif not debug:
            print(msg)
