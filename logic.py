from random import choice

import numpy as np

from cli_interface import truncate

import config


def get_start_game_board(rows_count=config.ROWS_COUNT,
                         cols_count=config.COLUMNS_COUNT) -> np.ndarray:

    cell_values = rows_count * cols_count
    board = (np.linspace(1, cell_values, cell_values, dtype=object)
             .reshape(rows_count, cols_count))

    return board


def get_cell_coords(board, cell_value) -> tuple:
    dimension_arrays = np.where(board == float(cell_value))
    x_array, y_array = dimension_arrays
    coords = (x_array[0], y_array[0])

    return coords


def get_role_alias(role_name, roles=config.ROLES, inverse_role=False):
    for role in roles:
        role_ = roles[role]
        if not inverse_role and role_['name'] == role_name:
            return role_['alias']
        elif inverse_role and role_['name'] != role_name:
            return role_['alias']


def update_cell_value(x, y, board, cell_value_alias):
    board[x, y] = cell_value_alias


def make_gamer_move(board, human_role_name) -> int:

    free_cells_values = [int(cell_value) for cell_value in board.flat
                         if isinstance(truncate(cell_value), int)]

    if not free_cells_values:  # Игрок заполнил последнюю клетку
        return

    free_cell_value = choice(free_cells_values)
    x, y = get_cell_coords(board, free_cell_value)

    update_cell_value(x, y, board, get_role_alias(human_role_name,
                                                  inverse_role=True))

    return free_cell_value


def get_sublist(line, size=config.CONSECUTIVE_ROLES):
    i = 0
    length = len(line)
    while i <= length - size:
        yield line[i:i + size]
        i += 1


def get_lines(board, size=config.CONSECUTIVE_ROLES, column=True):

    if size > board.shape[column]:
        exception_msg = (
            f'Кол-во подряд идущих меток (ролей) равно {size} и '
            f'превышает размерность карты {board.shape}.'
        )
        raise ValueError(exception_msg)

    if column:
        board = board.T

    for line in board:
        yield from get_sublist(line, size)


def get_diags(board, size=config.CONSECUTIVE_ROLES):

    if size > board.shape[0]:
        exception_msg = (
            f'Кол-во подряд идущих меток (ролей) равно {size} и '
            f'превышает размерность карты {board.shape}.'
        )
        raise ValueError(exception_msg)

    for d in range(-size, size + 1):
        yield from get_sublist(np.diag(board, d), size)

    board = np.fliplr(board)
    for d in range(-size, size + 1):
        yield from get_sublist(np.diag(board, d), size)


def determine_loser(board):

    columns = get_lines(board)
    rows = get_lines(board, column=False)
    diagonals = get_diags(board)

    board_parts = (columns, rows, diagonals, )
    for board_part in board_parts:
        for b_part in board_part:
            b_part_ = set(b_part)
            if len(b_part_) == 1:
                cell_value_alias = b_part_.pop()
                role_name = cell_value_alias[0]

                return role_name


if __name__ == '__main__':
    board = get_start_game_board()
    # print(board)

    # x, y = get_cell_coords(board, 15)
    # update_cell_value(x, y, board, 'x.0')
    # print(board)

    # board = change_values_representation(board)
    # print(board)

    # print(get_role_alias('o'))
