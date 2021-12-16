import pytest


@pytest.mark.ip_presentation
class Test1:
    TEST_DIR = 'print_ips'  # имя директории внутри ASSETS в которой находятся файл(ы) с тестовыми данными этого класса

    @pytest.fixture(scope='class')
    def current_test_data(self, test_data):
        """
        Фикстура подготовки и очищения окружения для тестов данного класса
        :param test_data: базовая фикстура подготовки и очищения окружения
        :return: параметризированный результат выполнения базовой фикстуры
        """
        return test_data(self.TEST_DIR)


    def test_print_ip_addresses(self, current_test_data, print_ip_decimal, print_ip_08b):
        """
        Тест преобразования IP-адреса в двоичный формат и вывода результата
            1. Вывод по строкам:
                - первой строкой - десятичные значения байтов адреса
                - второй строкой - двоичные значения байтов адреса
            2. Вывод по столбцам:
                - ширина столбца 10 символов
            Пример вывода для адреса 10.1.1.1:
            10        1         1         1
            00001010  00000001  00000001  00000001
        """
        ip_pool = current_test_data['ip_pool']
        for ip in ip_pool:
            print_ip_decimal(ip)
            print_ip_08b(ip)
