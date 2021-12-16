import os

from typing import Union

def remove_local_dir(dir_path: Union[str, bytes]):
    """
    Метод рекурсивного удаления директории на локальном хосте
        - если путь к директории существует, то директория удаляется с содержимым
        - если такой путь не существует, ошибка не генерируется
    :param dir_path: абсолютный путь к директории
    :return: None
    """
    if os.path.exists(dir_path):
        listdir = os.listdir(dir_path)

        if not listdir:
            os.rmdir(dir_path)
            return

        for elem in listdir:
            abs_path = os.path.join(dir_path, elem)
            try:
                os.remove(abs_path)  # remove file
            except (IsADirectoryError, PermissionError):
                remove_local_dir(abs_path)  # recursive call

        os.rmdir(dir_path)  # remove directory


def purge_local_dir(dir_path: Union[str, bytes]):
    """
    Метод для рекурсивного удаления содержимого директории на локальном хосте
        - если путь к директории существует, то содержимое директории удаляется и она остается пустой
        - если такой путь не существует, ошибка не генерируется
    :param dir_path: абсолютный путь к директории
    :return: None
    """
    if os.path.exists(dir_path):
        listdir = os.listdir(dir_path)

        for elem in listdir:
            abs_path = os.path.join(dir_path, elem)
            try:
                os.remove(abs_path)  # remove file
            except (IsADirectoryError, PermissionError):
                purge_local_dir(abs_path)  # recursive call
                os.rmdir(abs_path)  # remove directory
