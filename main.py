import warcaby_gra


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # p = warcaby_gra.Plansza()
    # p.create_start_board()
    # print(p)
    for levels in range(1, 6):
        for method in ["simple", "weighted"]:
            for alpha_beta in [False, True]:
                warcaby_gra.execute_game(levels=levels, alpha_beta=alpha_beta, method="simple", folder="output",
                                         repeat_game=10)

    # print(get_all_the_permissable_moves(p, True))
    # print(evaluate_best_move(p, iAmWhite=True, levels=7, alpha_beta=True, method="simple"))
    # pos = (6, 1)
    # pos = (5, 6)
    # # p.get_possible_moves_from_position((4, 3))
    # # print(p.get_possible_moves_from_position((5, 6)))
    # print(p.score_board_simple_method())
    # print(p.score_board_weighted_method())
    # possible = p.get_possible_moves_from_position(pos)
    # print(possible)
    # print(possible[0])
    # p = p.move_piece(pos, possible[0])
    # print(p)
    # print(p.score_board_simple_method())
    # print(p.score_board_weighted_method())

    # algorithm.min_max(p, 1, True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
