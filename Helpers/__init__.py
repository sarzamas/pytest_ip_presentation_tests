from os import mkdir, path
from typing import Union

LOCAL_DIR_PATH = path.split(path.dirname(__file__))[0]  # type: Union[str, bytes] # Рабочая директория проекта
IO_PATH = path.join(LOCAL_DIR_PATH, 'share')  # Директория для получения и выкладки объектов
ASSETS_PATH = path.join(LOCAL_DIR_PATH, 'assets')  # Директория с исходными данными

if not path.exists(IO_PATH):
    mkdir(IO_PATH)
