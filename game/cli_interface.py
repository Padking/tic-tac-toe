import argparse
from textwrap import dedent

import config


dialog_messages = {
    'game_start': dedent('''
        Вы играете роль '{}'.
        Начинаем игру!
    '''),
    'game_process_1': 'Введите номер клетки для заполнения: ',
    'game_process_2': 'Компьютер сделал свой ход: клетка № {}',
    'game_process_3': 'Ничья!',
    'game_finish': dedent('''
        Проиграл игрок '{}'
        Игра завершена!
    '''),
    'game_exception_1': 'Клетка с таким значением НЕ найдена!',
    'game_exception_2': 'Клетка с таким значением уже занята!',
}


def create_parser():
    description = dedent('''
        Игра "Обратные крестики-нолики".

    ''')

    parser = argparse.ArgumentParser(description=description)

    help_to_role_argument_tmpl = 'Роль (за кого Вы): {} или {}. По умолчанию: {}'
    help_to_role_argument = (help_to_role_argument_tmpl
                             .format(config.ROLES['1']['name'],
                                     config.ROLES['2']['name'],
                                     config.ROLES['1']['name']))
    parser.add_argument('role',
                        choices=[
                            config.ROLES['1']['name'],
                            config.ROLES['2']['name'],
                        ],
                        default=config.ROLES['1']['name'],
                        help=help_to_role_argument,
                        nargs='?')

    return parser


def change_values_representation(board) -> list:
    board = [[truncate(value) for value in row] for row in board]

    return board


def truncate(val):
    if isinstance(val, float):
        return int(val)
    elif isinstance(val, str):
        cell_value = val[0]
        return str(cell_value)
