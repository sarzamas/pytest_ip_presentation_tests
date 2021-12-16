import os
from typing import Union

LOCAL_DIR_PATH = os.path.split(os.path.dirname(__file__))[0]  # type: Union[str, bytes] # Рабочая директория проекта
IO_PATH = os.path.join(LOCAL_DIR_PATH, 'share')  # Директория для получения и выкладки объектов
ASSETS_PATH = os.path.join(LOCAL_DIR_PATH, 'assets')  # Директория с исходными данными

if not os.path.exists(IO_PATH):
    os.mkdir(IO_PATH)
