import csv
import json
from typing import Any


def open_file(
        path: str,  mode: str = 'r', encoding: str = 'utf-8',
        newline: str | None = None, data: Any | None = None
):
    '''
    Чтение и запись файлов только mode: r(read), w(write), a(append).
    Для расширений файлов .csv, .txt, .html, .json

    :param path: путь до файла c расширением
    :param mode: способ взаимодействия с файлом, чтение/запись/дозапись
    :param encoding: кодировка файла
    :param newline: перенос на новую строку, важен для .csv файлов
    :param data: данные которые нужно добавить в файл, только в режимах запись/дозапись
    '''
    head, tail = split_file_path(path)
    if mode == 'r':
        with open(f'{head}.{tail}', mode=mode, encoding=encoding, newline=newline) as file:
            if tail == 'html' or tail == 'txt':
                res = file.read()
            elif tail == 'json':
                res = json.load(file)
            elif tail == 'csv':
                pass
        return res

    elif mode == 'a' or mode == 'w':
        with open(f'{head}.{tail}', mode=mode, encoding=encoding, newline=newline) as file:
            if tail == 'html' or tail == 'txt':
                file.write(data)
            elif tail == 'json':
                json.dump(data, file, indent=4, ensure_ascii=False)
            elif tail == 'csv':
                writer = csv.writer(file)
                writer.writerow(
                    tuple(data.values())
                )
    else:
        raise ValueError("Неподдерживаемый mode записи файла")


def split_file_path(file_path: str) -> (str, str):
    '''
    Функция разделяет путь к файлу на имя файла и расширение
    :param file_path: путь к файлу
    :return: название файла, расширение файла
    '''

    if file_path.endswith('.html') or file_path.endswith('.json'):
        head = file_path[:-5]
        tail = file_path[-4:]
        return head, tail
    elif file_path.endswith('.csv') or file_path.endswith('.txt'):
        head = file_path[:-4]
        tail = file_path[-3:]
    else:
        raise ValueError("Неподдерживаемый формат расширения файла")
    return head, tail


def normalize_name(string) -> str:
    '''
    Функция заменяет лишние символы в строке на нижнее подчеркивание
    :param string:
    :return: возвращает измененныую строку
    '''

    rep = {ord(','): '_', ord(' '): '_', ord('-'): '_', ord('\''): '_'}
    new_string = string.translate(rep)
    return new_string
