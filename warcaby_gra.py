import os
import random
import time
from copy import deepcopy
from datetime import datetime

import numpy as np
from numpy import ndarray

from algorithm import get_pos_of_all, get_all_the_permissable_moves, evaluate_best_move


class Plansza:
    SIZE_X = 8
    SIZE_Y = 8
    boad: ndarray

    def __init__(self, plansza=None):
        if plansza is None:
            self.board = np.zeros((Plansza.SIZE_X, Plansza.SIZE_Y))
            self.create_start_board()
        else:
            self.board = plansza

    def create_start_board(self):
        # biale = -1
        # czarne = 1
        self.board[0][1] = 1
        self.board[0][3] = 1
        self.board[0][5] = 1
        self.board[0][7] = 1
        # self.board[6][5] = 1

        self.board[1][0] = 1
        # self.board[2][1] = 1
        self.board[1][2] = 1
        # self.board[2][3] = 1
        self.board[1][4] = 1
        # self.board[4][5] = 1
        self.board[1][6] = 1
        # self.board[2][5] = 1

        self.board[6][1] = -1
        self.board[6][3] = -1
        self.board[6][5] = -1
        # self.board[5][6] = -1
        self.board[6][7] = -1

        self.board[7][0] = -1
        self.board[7][2] = -1
        self.board[7][4] = -1
        # self.board[4][1] = -1
        self.board[7][6] = -1
        # self.board[4][3] = -2

    def is_empty(self, pos_y, pos_x) -> bool:
        return self.board[pos_y][pos_x] == 0

    def is_damka(self, pos_y, pos_x):
        return abs(self.board[pos_y][pos_x]) == 2

    def is_pawn(self, pos_y, pos_x):
        return abs(self.board[pos_y][pos_x]) == 1

    def is_white(self, pos_y, pos_x):
        return self.board[pos_y][pos_x] < 0

    def is_forward_direction(self, from_pos_y, to_pos_y, is_white):
        if is_white:
            return from_pos_y - to_pos_y > 0
        else:
            return from_pos_y - to_pos_y < 0

    @staticmethod
    def is_in_bounds(pos_y, pos_x):
        return 0 <= pos_y <= 7 and 0 <= pos_x <= 7

    def recurrent_check_passing(self, list_pos, current_pos, im_white, is_pawn, ignore_pos_list):
        posY, posX = current_pos
        positions_to_check = self.get_possible_positions(posY, posX, is_pawn, im_white, True)
        for possible in positions_to_check:
            possible_y, possible_x = possible
            if possible not in ignore_pos_list and not self.is_empty(possible_y, possible_x) and self.is_white(
                    possible_y, possible_x) != im_white:
                vector_y, vector_x = self.get_vector_direction(current_pos, possible)
                final_pos_y = possible_y + vector_y
                final_pos_x = possible_x + vector_x

                if self.is_in_bounds(final_pos_y, final_pos_x) and self.is_empty(final_pos_y, final_pos_x):
                    lister = []
                    list_pos.append(((final_pos_y, final_pos_x), (possible_y, possible_x), lister))
                    ignore_pos_list.append((possible_y, possible_x))
                    self.recurrent_check_passing(lister, (final_pos_y, final_pos_x), im_white, is_pawn, ignore_pos_list)

    @staticmethod
    def get_vector_direction(pos1, pos2):
        pos1Y, pos1X = pos1
        pos2Y, pos2X = pos2

        if pos2Y > pos1Y:
            y_direction = 1
        elif pos2Y < pos1Y:
            y_direction = -1
        else:
            y_direction = 0

        if pos2X > pos1X:
            x_direction = 1
        elif pos2X < pos1X:
            x_direction = -1
        else:
            x_direction = 0

        return y_direction, x_direction

    def get_possible_positions(self, posY, posX, is_pawn, is_white, ignore_forward=False):
        positions_to_check = []
        if is_pawn:
            if posY != 0 and (ignore_forward or self.is_forward_direction(posY, posY - 1, is_white)):
                if posX != 0:
                    positions_to_check.append((posY - 1, posX - 1))
                if posX != 7:
                    positions_to_check.append((posY - 1, posX + 1))
            if posY != 7 and (ignore_forward or self.is_forward_direction(posY, posY + 1, is_white)):
                if posX != 0:
                    positions_to_check.append((posY + 1, posX - 1))
                if posX != 7:
                    positions_to_check.append((posY + 1, posX + 1))
        else:
            for y in range(1, 8):
                if self.is_in_bounds(y + posY, posX):
                    positions_to_check.append((posY + y, posX))
                    if not self.is_empty(y + posY, posX):
                        break

            for y in range(1, 8):
                if self.is_in_bounds(posY - y, posX):
                    positions_to_check.append((posY - y, posX))
                    if not self.is_empty(posY - y, posX):
                        break
            for x in range(1, 8):
                if self.is_in_bounds(posY, posX + x):
                    positions_to_check.append((posY, posX + x))
                    if not self.is_empty(posY, posX + x):
                        break
            for x in range(1, 8):
                if self.is_in_bounds(posY, posX - x):
                    positions_to_check.append((posY, posX - x))
                    if not self.is_empty(posY, posX - x):
                        break

            for i in range(1, 8):
                if self.is_in_bounds(posY + i, posX + i):
                    positions_to_check.append((posY + i, posX + i))
                    if not self.is_empty(posY + i, posX + i):
                        break
            for i in range(1, 8):
                if self.is_in_bounds(posY - i, posX + i):
                    positions_to_check.append((posY - i, posX + i))
                    if not self.is_empty(posY - i, posX + i):
                        break
            for i in range(1, 8):
                if self.is_in_bounds(posY - i, posX - i):
                    positions_to_check.append((posY - i, posX - i))
                    if not self.is_empty(posY - i, posX - i):
                        break
            for i in range(1, 8):
                if self.is_in_bounds(posY + i, posX - i):
                    positions_to_check.append((posY + i, posX - i))
                    if not self.is_empty(posY + i, posX - i):
                        break
        return (positions_to_check)

    def build_hit_roads(self, list_hits):
        roads = []
        for hit in list_hits:
            road = []
            target_pos, pawn_to_hit, inner_list = hit
            road.append((target_pos, pawn_to_hit))
            if len(inner_list) != 0:
                inner_roads = self.build_hit_roads(inner_list)
                for inner_road_list in inner_roads:
                    copy = list(road)
                    copy += inner_road_list
                    roads.append(copy)
            else:
                roads.append(road)
        return roads

    def get_hit_longest(self, list_of_roads):
        maximal = len(max(list_of_roads, key=lambda x: len(x)))
        return list(filter(lambda road: len(road) == maximal, list_of_roads))

    def get_possible_moves_from_position(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        posY, posX = pos
        # 0 - movement
        # 1 - hit
        possible_end_position_with_type = []
        positions_to_check = self.get_possible_positions(posY, posX, self.is_pawn(posY, posX),
                                                         self.is_white(posY, posX))
        for possible_pos in positions_to_check:
            possible_y, possible_x = possible_pos
            if self.is_empty(possible_y, possible_x):
                # if self.is_forward_direction(posY, posY-1, self.is_white(posY, posX)):
                possible_end_position_with_type.append((possible_pos, 0))

        # We can check for zbicie
        li = []
        self.recurrent_check_passing(li, pos, self.is_white(posY, posX), self.is_pawn(posY, posX), [])
        if len(li) != 0:
            final = self.build_hit_roads(li)
            longest = self.get_hit_longest(final)
            hits = list(map(lambda road: (road, 1), longest))
            possible_end_position_with_type = hits
        return possible_end_position_with_type

    def score_board_simple_method(self):
        return self.board.sum()

    def score_board_moveable(self):
        whites = 0

        def count(pos):
            posY, posX = pos
            c = 0
            # 0 - movement
            # 1 - hit
            possible_end_position_with_type = []
            positions_to_check = self.get_possible_positions(posY, posX, self.is_pawn(posY, posX),
                                                             self.is_white(posY, posX))
            for possible_pos in positions_to_check:
                possible_y, possible_x = possible_pos
                if self.is_empty(possible_y, possible_x):
                    c += 1
                    # if self.is_forward_direction(posY, posY-1, self.is_white(posY, posX)):
                    # possible_end_position_with_type.append((possible_pos, 0))
            return c

        for pos in get_pos_of_all(self, True):
            whites -= count(pos)
        for pos in get_pos_of_all(self, False):
            whites += count(pos)
        return whites

    def score_safe_pawns(self):
        c = 0
        for posY, posX in get_pos_of_all(self, True):
            if posX == 7 or posX == 0:
                c -= 1
        for posY, posX in get_pos_of_all(self, False):
            if posX == 7 or posX == 0:
                c += 1
        return c

    def score_board_weighted_method(self):
        sum = 0
        for y in range(0, 8):
            for x in range(0, 8):
                v = self.board[y, x]

                if 1 < y < 6 and 1 < x < 6:
                    v *= 3
                elif 0 < y < 7 and 0 < x < 7:
                    v *= 2
                sum += v
        return sum

    def clone_self(self):
        board = deepcopy(self.board)
        return Plansza(board)

    def move_piece(self, mover_pos, move):
        s = self.clone_self()

        if move[1] == 0:
            target = move[0]
            p = s.board[mover_pos]
            s.board[mover_pos] = 0
            s.board[target] = p

        elif move[1] == 1:
            target = move[0][-1][0]
            p = s.board[mover_pos]
            s.board[mover_pos] = 0
            s.board[target] = p
            for target_pos, pawn_to_remove in move[0]:
                s.board[pawn_to_remove] = 0
        else:
            raise Exception("Illegal move")
        if s.board[target] == -1 and target[0] == 0:
            s.board[target] = -2
        elif s.board[target] == 1 and target[0] == 7:
            s.board[target] = 2

        return s

    def __str__(self):
        b = "# 0 1 2 3 4 5 6 7\n"
        for y in range(0, 8):
            b += f"{y} "
            for x in range(0, 8):
                match self.board[y][x]:
                    case 1:
                        b += "X"
                    case -1:
                        b += "O"
                    case -2:
                        b += "L"
                    case 2:
                        b += "K"
                    case _:
                        b += "_"
                b += " "
            b += "\n"
        return b


class Game:
    GAME_IN_PROGRESS = "game_in_progress"
    GAME_WON_WHITE = "whites_won"
    GAME_WON_BLACK = "black_won"
    GAME_DRAW = "draw"

    def __init__(self, levels=5, alpha_beta=True, method="simple"):
        self.method = method
        self.alpha_beta = alpha_beta
        self.levels = levels
        self.whitesTurn = True
        self.turn = 0
        self.plansza = Plansza()
        self.turns_only_queen = 0

    def ai_turn(self):
        self.executeTurn(self.whitesTurn)
        self.turn += 1
        self.whitesTurn = not self.whitesTurn

    def player1Turn(self):
        if self.player1TurnNow:
            self.player1TurnNow = not self.player1TurnNow
            self.turn += 1
            self.executeTurn(self.player1White)
        else:
            raise Exception()

    def player2Turn(self):
        if not self.player1TurnNow:
            self.player1TurnNow = not self.player1TurnNow
            self.turn += 1
            self.executeTurn(not self.player1White)
        else:
            raise Exception()

    def executeTurn(self, whiteMove: bool):
        move = evaluate_best_move(self.plansza, whiteMove=whiteMove, levels=self.levels, alpha_beta=self.alpha_beta,
                                  method=self.method)
        # print(move)
        # print(len(get_all_the_permissable_moves(self.plansza, True)), len(get_all_the_permissable_moves(self.plansza, False)))
        if self.plansza.is_pawn(move[0][0], move[0][1]):
            self.turns_only_queen = 0
        else:
            self.turns_only_queen += 1
        self.plansza = self.plansza.move_piece(move[0], move[1])

    def random_move(self, whites):
        move = random.choice(get_all_the_permissable_moves(self.plansza, whites))
        self.plansza = self.plansza.move_piece(move[0], move[1])

    def get_game_status(self):
        whites_len = len(get_all_the_permissable_moves(self.plansza, True))
        black_len = len(get_all_the_permissable_moves(self.plansza, False))
        if len(get_pos_of_all(self.plansza, True)) == 0 or len(get_all_the_permissable_moves(self.plansza, True)) == 0:
            return self.GAME_WON_BLACK
        elif len(get_pos_of_all(self.plansza, False)) == 0 or len(
                get_all_the_permissable_moves(self.plansza, False)) == 0:
            return self.GAME_WON_WHITE
        elif self.turns_only_queen == 28 or (whites_len == 0 and black_len == 0):
            return self.GAME_DRAW
        return self.GAME_IN_PROGRESS


def execute_game(levels=5, alpha_beta=True, method="simple", folder="output", game_details=False, repeat_game=1):
    with open(os.path.join(folder,
                           f"{levels}_{alpha_beta}_{method}_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S_%f')}.txt"),
              "w",
              encoding="utf-8") as output:
        for i in range(repeat_game):
            print(f"Run {i}/{repeat_game} for {levels} {alpha_beta} {method}")
            game = Game(levels, alpha_beta, method)
            start_time = time.time()
            output.write(f"{i} {repeat_game} {datetime.now()} {start_time} {levels} {alpha_beta} {method}\n")

            game.random_move(True)
            game.random_move(False)
            if game_details:
                output.write(str(game.plansza))
                output.write("\n\n")
                output.write(f"$ {datetime.now()} {time.time() - start_time} {game.turn} {game.whitesTurn}\n")
            while game.get_game_status() == Game.GAME_IN_PROGRESS:
                game.ai_turn()
                if game_details:
                    output.write(str(game.plansza))
                    output.write("\n\n")
                    output.flush()

            output.write(f"END {datetime.now()} {time.time() - start_time} {game.turn} {game.get_game_status()}\n")
            output.flush()
            print(f"WON: {game.get_game_status()}")
