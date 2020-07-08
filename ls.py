import argparse
import os
import logging


NAME = 'ls emulation'
DESCRIPTION = '''This is a program that are able to show content of directory'''
EPILOG = '(c) Sergey Martynov 2020'
VERSION = '0.0.1'


# Функция вывода в строку
def print_string(path, args):
    """Печатает содержание папки в строку. Если передан параметр а, печатет и скрытые папки и файлы,
    если передан параметр d, печатает только папки, если передан параметр s, выводит размеры файлов и папок.
    :type path: str
    """
    items_raw = os.listdir(path)
    # Очищаем список элементов директории в зависимости от переданных параметров а и d.
    items = []
    for item in items_raw:
        if 'd' in args and os.path.isdir(path+os.sep+item) is True:
            items.append(item)
        elif 'd' not in args:
            items.append(item)

    for item in items:
        if 'a' not in args and item[0] == '.':
            items.remove(item)

    # Функция печати элемента
    def print_item(item):
        descr = '<Dir>' if os.path.isdir(path+os.sep+item) else '<File>'
        if 's' in args:
            print(f'{item}  {descr} {os.path.getsize(path+os.sep+item)} bites', end='    ')
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
    :type path: str

    """
    for root, directories, files in os.walk(path):  # Перебирает все уровни дерева каталога папок
        level = root.count(os.sep)  # определяем уровень папки
        otst = ' ' * 4 * level  # считаем какой нужно делать отступ
        print(
            f'{otst}[{root.split(os.sep)[-1]}]   {os.path.getsize(root)} bites')  # Печатаем название папки с отступом, соответствующим уровню папки.
        for file in files:
            print(f'{otst}    {file}   {os.path.getsize(root+os.sep+file)} bites')  # Печатаем названия файлов в папке


# Логгер.
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()


if __name__ == '__main__':
    # Считываем значения аргументов
    p = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION, epilog=EPILOG, add_help=False)
    p.add_argument('-a', action='store_true', help='Option to show hidden objects')
    p.add_argument('-d', action='store_true', help='Option to show only directories')
    p.add_argument('-s', action='store_true', help='Option to show sizes objects')
    p.add_argument('-t', action='store_true', help='Option to show complete tree of directory')
    p.add_argument('path', type=str, default='.', nargs='?', help='Path to directory to be processed')
    p.add_argument('--help', '-h', action='help', help='Help message')
    p.add_argument('--version', '-v', action='version', help='Version', version='%(prog)s {}'.format(VERSION))
    args = p.parse_args()

    params = []
    if args.a:
        params.append('a')
    if args.d:
        params.append('d')
    if args.s:
        params.append('s')
    if args.t:
        params.append('t')

    logger.info('Параметры введены')

    # Основной процесс обработки
    print_string(args.path, params)
    if 't' in params:
        folder_tree(args.path)

    logger.info('Работа программы завершена')