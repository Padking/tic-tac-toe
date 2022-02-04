from tabulate import tabulate

from cli_interface import (
    change_values_representation,
    create_parser,
    dialog_messages,
)

from logic import (
    determine_loser,
    get_cell_coords,
    get_role_alias,
    get_start_game_board,
    make_gamer_move,
    update_cell_value,
)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    role = args.role

    game_start_tmpl = dialog_messages['game_start']
    game_start_msg = game_start_tmpl.format(role)
    print(game_start_msg)
    board = get_start_game_board()
    tabulated_board = tabulate(board, tablefmt='grid')
    print(tabulated_board)

    while True:
        cell_value = input(dialog_messages['game_process_1'])
        try:
            x, y = get_cell_coords(board, cell_value)
        except ValueError:
            print(dialog_messages['game_exception_1'])
            continue
        except IndexError:
            print(dialog_messages['game_exception_2'])
            continue

        update_cell_value(x, y, board, get_role_alias(role))

        loser_role_name = determine_loser(board)
        if loser_role_name:
            game_finish_tmpl = dialog_messages['game_finish']
            game_finish_msg = game_finish_tmpl.format(loser_role_name)
            print(game_finish_msg)
            break

        filled_cell_value = make_gamer_move(board, role)
        if filled_cell_value:
            game_process_tmpl = dialog_messages['game_process_2']
            game_process_msg = game_process_tmpl.format(filled_cell_value)
            print(game_process_msg)
            prepared_board = change_values_representation(board)
            tabulated_board = tabulate(prepared_board, tablefmt='grid')
            print(tabulated_board)
        else:
            game_process_msg = dialog_messages['game_process_3']
            print(game_process_msg)
            break

        loser_role_name = determine_loser(board)
        if loser_role_name:
            game_finish_tmpl = dialog_messages['game_finish']
            game_finish_msg = game_finish_tmpl.format(loser_role_name)
            print(game_finish_msg)
            break
