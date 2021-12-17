import pytest


@pytest.mark.ip_presentation
class Test2:
    TEST_DIR = 'check_ips'  # имя директории внутри ASSETS в которой находятся файл(ы) с тестовыми данными этого класса

    @pytest.fixture(scope='class')
    def current_test_data(self, test_data):
        """
        Фикстура подготовки и очищения окружения для тестов данного класса
        :param test_data: базовая фикстура подготовки и очищения окружения
        :return: параметризированный результат выполнения базовой фикстуры
        """
        return test_data(self.TEST_DIR)

    def test_check_ip_addresses(self, current_test_data, is_ip_accessible):
        """
        Тест проверяет доступность IP-адресов в тестовых данных и выводит результат в виде списков:
            - список #1: доступных IP-адресов
            - список #2: недоступных IP-адресов
        """
        ip_pool = current_test_data['ip_pool']
        linesep = current_test_data['linesep']
        accessible_ips, un_accessible_ips = [], []
        for ip in ip_pool:
            accessible_ips.append(ip) if is_ip_accessible(ip) else un_accessible_ips.append(ip)

        print(f'{linesep}СПИСОК №1: {linesep}Доступные IP-адреса:', accessible_ips)
        print(f'{linesep}СПИСОК №2: {linesep}Недоступные IP-адреса:', un_accessible_ips)
