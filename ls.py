import logging
import os
import sys


NAME = 'ls emulation'
DESCRIPTION = '''This is a program that are able to show content of directory'''
EPILOG = '(c) Sergey Martynov 2020'
VERSION = '0.0.1'


# Функция вывода в строку
def print_string(path, args):
    """Печатает содержание папки в строку. Если передан параметр а, печатет и скрытые папки и файлы,
    если передан параметр d, печатает только папки, если передан параметр s, выводит размеры файлов и папок.
    :type path: str
    :type args: str
    """
    items_raw = os.listdir(path)
    # Очищаем список элементов директории в зависимости от переданных параметров а и d.
    items = []
    for item in items_raw:
        if 'd' in args and os.path.isdir(path + os.sep + item) is True:
            items.append(item)
        elif 'd' not in args:
            items.append(item)

    for item in items:
        if 'a' not in args and item[0] == '.':
            items.remove(item)

    # Функция печати элемента
    def print_item(item):
        descr = '<Dir>' if os.path.isdir(path + os.sep + item) else '<File>'
        if 's' in args:
            print(f'{item}  {descr} {os.path.getsize(path + os.sep + item)} bites', end='    ')
        else:
            print(f'{item}  {descr}', end='    ')

    for item in items:
        print_item(item)
    print(' ')


# Функция вывода дерева директории
def folder_tree(path):
    """
    Выводит дерево директории (каталога). Папка, файлы, вложенная папака, файлы и папки в ней и т.д.

    :param folder: Название папки, у которой нужно вывести дерево папок и фалов.
    :type a: str

    """
    for root, directories, files in os.walk(path):  # Перебирает все уровни дерева каталога папок
        level = root.count(os.sep)  # определяем уровень папки
        otst = ' ' * 4 * level  # считаем какой нужно делать отступ
        print(
            f'{otst}[{root.split(os.sep)[-1]}]   {os.path.getsize(root)} bites')  # Печатаем название папки с отступом, соответствующим уровню папки.
        for file in files:
            print(
                f'{otst}    {file}   {os.path.getsize(root + os.sep + file)} bites')  # Печатаем названия файлов в папке


# Логгер.
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()

if __name__ == '__main__':
    # Считываем значения аргументов
    if len(sys.argv) > 3:
        print('Неправильный формат ввода')
        sys.exit(-1)

    if len(sys.argv) == 1:
        path = '.'
        params = '-'

    if len(sys.argv) == 2:
        if sys.argv[1][0] == '-':
            path = '.'
            params = sys.argv[1]
        else:
            path = sys.argv[1]
            params = '-'
    if len(sys.argv) == 3:
        path = sys.argv[2]
        params = sys.argv[1]

    logger.info('Параметры введены')

    # Проверяем правильность введения параметров
    if len(params) > 6:
        print('Неправильный размер ключа')
        sys.exit(-1)
    if params[0] != '-':
        print('Неверный формат ключа')
        sys.exit(-1)
    for param in params[1:]:
        if param not in ['a', 'd', 's', 't']:
            print('Неправильный элемент в ключе')
            sys.exit(-1)

    logger.info('Параметры проверены')
    # Основной процесс обработки
    print_string(path, params)
    if 't' in params:
        folder_tree(path)

    logger.info('Работа программы завершена')