import os
import pytest
import platform  # For getting the OS name
import socket
import subprocess  # For executing a shell command

from Helpers import ASSETS_PATH, IO_PATH
from Helpers.files_methods import purge_local_dir
from Resources import *


@pytest.fixture(scope='class', name='test_data')
def preconditions_teardown():
    """
    Фикстура выполняет следующие действия:
    preconditions:
        - выделяет IP адреса из файла(ов) с данными (построчно)
        - проверяет валидность IP адресов
        - формирует пул корректных IP адресов для теста
    teardown:
        -
    """
    _teardown_params = []

    def _preconditions_teardown(test_dir):
        assets_dir_path = os.path.join(ASSETS_PATH, test_dir)
        work_dir_path = os.path.join(IO_PATH, test_dir)
        linesep = os.linesep

        purge_local_dir(os.path.join(IO_PATH)) if os.path.exists(IO_PATH) else os.mkdir(IO_PATH)
        os.mkdir(work_dir_path)

        ip_pool = create_ip_pool(assets_dir_path)
        origin_objects = create_origin_objects(work_dir_path, ip_pool)

        _teardown_params.append(origin_objects)

        return {
            'ip_pool': ip_pool,
            'linesep': linesep,
            'origin_objects': origin_objects
        }

    yield _preconditions_teardown

    for teardown_param in _teardown_params:
        remove_temp_objects(teardown_param)


@pytest.fixture(scope='class')
def print_ip_decimal():
    """ Фикстура печати IP-адреса в десятичном формате """

    def _print_ip_decimal(ip):
        print(os.linesep, f'IP: {ip}')
        print("".join(list(map(lambda x: x.ljust(10), ip.split('.')))))

    return _print_ip_decimal


@pytest.fixture(scope='class')
def print_ip_08b():
    """ Фикстура печати IP-адреса в двоичном формате """

    def _print_ip_08b(ip):
        print("".join(list(map(lambda x: x.ljust(10), transform_ip(ip)))))
    return _print_ip_08b


@pytest.fixture(scope='class')
def is_ip_accessible():
    """ Фикстура проверки доступности IP-адреса """

    def _is_ip_accessible(ip):
        return ping_host_result(ip)

    return _is_ip_accessible


def ping_host_result(ip: str) -> bool:
    """
    Метод проверки доступности IP адреса утилитой ping (ICMP) request
    :param ip: IP адрес хоста, доступность которого необходимо проверить
    :return: bool: зузультат троекратного выполнения команды 'ping' для проверяемого IP адреса
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'  # Option for the number of packets as a func of OS
    command = ['ping', param, '3', ip]  # Building the command. Ex: "ping -c 1 google.com"

    return subprocess.call(command) == 0


def create_ip_pool(assets_dir_path: str) -> list:
    """
    Метод создания списка исходных IP адресов
    :param assets_dir_path: абсолютный путь к директории с тестовыми файлами
    :return: ip_pool: список валидных IP адресов - исходных данных для теста
    """
    ip_pool = []
    for file_name in os.listdir(assets_dir_path):
        file_path = os.path.join(assets_dir_path, file_name)
        ip_pool.append(read_ip_pool(file_path))
    return flatten(ip_pool)


def read_ip_pool(filename: str) -> list:
    """
    Метод чтения содержимого файла построчно с выдачей содержимого списком
    :type filename: str
    :param filename: имя файла с тестовыми данными в UTF-8
    :return: list
    """
    lines = ip_pool = []
    try:
        with open(filename, "rt", encoding="utf-8") as file:
            lines = file.read().splitlines()
    except UnicodeDecodeError:
        pass
    for line in lines:
        if is_valid_ipv4_address(line.rstrip()):
            ip_pool.append(line)
    return ip_pool


def is_valid_ipv4_address(address: str) -> bool:
    """
    Метод проверки валидности синтаксиса IPv4 адреса
    :param address: IPv4 адрес в dotted decimal представлении '0.0.0.0'
    :return: bool
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True


def transform_ip(ip: str) -> list:
    """
    Метод преобразования IP-адреса из dotted decimal в двоичный формат с паддингом до байта
    :param ip: IPv4 адрес в dotted decimal представлении '0.0.0.0'
    :return: list
    """
    ip_08b = [format(int(x), '08b') for x in ip.split('.')]
    return ip_08b


def flatten(list_of_lists: list) -> list:
    """
    Метод слияния списка списков
    :param list_of_lists: любой список
    :return: плоский список значений
    """
    flattened = []
    for lst in list_of_lists:
        flattened.extend(lst)
    return flattened


def create_origin_objects(work_dir_path: str, ip_pool: list):
    """
    Метод создания исходных объектов с необходимыми для тестов атрибутами
    :param work_dir_path: абсолютный путь к директории с файлами объектов
    :param ip_pool: абсолютный путь к директори
    :return: origin_objects: list список объектов c исходными данными после их предварительной подготовки
    """
    origin_objects = []
    for ip in ip_pool:
        origin_objects.append(OriginResource(work_dir_path, ip))

    return origin_objects


def remove_temp_objects(objects):
    """
    Метод очищения ресурсов, созданных в тестовой сессии
        -
    :param objects: список объектов для удаления
    """
    pass
