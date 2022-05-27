import warcaby_gra


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    warcaby_gra.execute_game(4, 1, "simple", "", True, 1)
    # p = warcaby_gra.Plansza()
    # p.create_start_board()
    # print(p)
    # with Pool(processes=4) as pool:
    #     for levels in range(1, 6):
    #         for method in ["simple_safe", "simple_moveable"]:
    #             for alpha_beta in [False, True]:
    #                 pool.apply_async(warcaby_gra.execute_game, [levels, alpha_beta, method, "output2", False, 50])
    #     for levels in range(6, 10):
    #         for method in ["simple_safe", "simple_moveable"]:
    #             pool.apply_async(warcaby_gra.execute_game, [levels, True, method, "output2", False, 50])
    #
    #     pool.close()
    #     pool.join()

    # print(get_all_the_permissable_moves(p, True))
    # print(evaluate_best_move(p, iAmWhite=True, levels=7, alpha_beta=True, method="simple", ))
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
