import os
import platform
import subprocess


class OriginResource:
    """
    Класс содержащий атрибуты исходных данных
    """

    def __init__(self, abs_path, ip):
        self.dir_path = abs_path
        self.ip = ip
        self.ping_status = None
        self.ip_decimal_padding = "".join(list(map(lambda x: x.ljust(10), self.ip.split('.'))))
        self.ip_08b_padding = "".join(list(map(lambda x: x.ljust(10), self.transform_ip(self.ip))))
        self.__resource_preparation()

    @property
    def ping_status(self) -> bool:
        """
        Возвращает статус доступности IP адреса
        """
        return self.ping_status

    @ping_status.setter
    def ping_status(self, value):
        if not value:
            pass
        else:
            self.ping_status = self.ping_host_result(self.ip)

    def __resource_preparation(self):
        """
        Метод подготовки исходного ресурса:
        - создание файла с содержимым подготовленным для теста
        """
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        file = open(os.path.join(self.dir_path, f"{self.ip}.txt"), "w+")
        file.write(self.ip_decimal_padding)
        file.write(os.linesep)
        file.write(self.ip_08b_padding)
        file.close()

    def ping_host_result(self, ip: str) -> bool:
        """
        Метод проверки доступности IP адреса утилитой ping (ICMP) request
        :param ip: IP адрес хоста, доступность которого необходимо проверить
        :return: bool: зузультат троекратного выполнения команды 'ping' для проверяемого IP адреса
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'  # Option for number of packets as a func of OS
        command = ['ping', param, '3', ip]  # Building the command. Ex: "ping -c 1 google.com"

        return subprocess.call(command) == 0

    def transform_ip(self, ip: str) -> list:
        """
        Метод преобразования IP-адреса из dotted decimal в двоичный формат с паддингом до байта
        :param ip: IPv4 адрес в dotted decimal представлении '0.0.0.0'
        :return: list
        """
        ip_08b = [format(int(x), '08b') for x in ip.split('.')]
        return ip_08b
