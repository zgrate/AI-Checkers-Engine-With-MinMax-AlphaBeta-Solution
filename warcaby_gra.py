from copy import deepcopy

import numpy as np
from numpy import ndarray


class Plansza:
    SIZE_X = 8
    SIZE_Y = 8
    boad: ndarray

    def __init__(self, plansza=None):
        if plansza is None:
            self.board = np.zeros((Plansza.SIZE_X, Plansza.SIZE_Y))
        else:
            self.board = plansza

    def create_start_board(self):
        # biale = -1
        # czarne = 1
        self.board[0][1] = 1
        self.board[0][3] = 1
        self.board[0][5] = 1
        # self.board[0][7] = 1
        self.board[6][5] = 1

        # self.board[1][0] = 1
        self.board[2][1] = 1
        # self.board[1][2] = 1
        self.board[2][3] = 1
        # self.board[1][4] = 1
        self.board[4][5] = 1
        # self.board[1][6] = 1
        self.board[2][5] = 1

        self.board[6][1] = -1
        self.board[6][3] = -1
        # self.board[6][5] = -1
        self.board[5][6] = -1
        self.board[6][7] = -1

        self.board[7][0] = -1
        self.board[7][2] = -1
        # self.board[7][4] = -1
        self.board[4][1] = -1
        # self.board[7][6] = -1
        self.board[4][3] = -2

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

        # if any(x[1] == 1 for x in possible_end_position_with_type):
        #     possible_end_position_with_type = list(filter(lambda possible: possible[1] == 1, possible_end_position_with_type))
        #     if len(possible_end_position_with_type) > 1:
        #         maximal = len(max(possible_end_position_with_type, key=lambda poss: len(poss[0]))[0])
        #         possible_end_position_with_type = list(filter(lambda d: len(d[0]) == maximal, possible_end_position_with_type))
        return possible_end_position_with_type

    # def is_move_legal(self, fromPos: tuple[int, int], toPos: tuple[int, int]) -> bool:
    #     fromY, fromX = fromPos
    #     toY, toX = toPos
    #     if 7 < toY < 0 or 7 < toX < 0:
    #         return False
    #     piece = self.board[fromPos]
    #     if piece == 0:
    #         return False
    #     toPos = self.board[toPos]
    #     if toPos != 0:
    #         return False
    #
    #     if piece == 2 or piece == -2: #damka
    #         pass
    #     else:
    #         if fromX == toX or fromY == toY: #move in straight line
    #             return False
    #         elif abs(fromX - toX) == 2 and abs(fromY - toY) == 2:#He is trying to die the enemy xd
    #             midX = (fromX + toX)/2
    #             midY = (fromY + toY)/2
    #
    #
    #         elif piece == 1 and fromY < toY: #Blacks only forward down, so y -> 8
    #             return False
    #         elif piece == -1 and fromY > toY: #Whites only forward up, so y -> 0
    #             return False

    def score_board_simple_method(self):
        return self.board.sum()

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
                print(y, x, v)

        return sum

    def clone_self(self):
        board = deepcopy(self.board)
        return Plansza(board)

    def move_piece(self, mover_pos, move):
        s = self.clone_self()
        if move[1] == 0:
            p = s.board[mover_pos]
            s.board[mover_pos] = 0
            s.board[move[0]] = p
        elif move[1] == 1:
            p = s.board[mover_pos]
            s.board[mover_pos] = 0
            s.board[move[0][-1][0]] = p
            for target_pos, pawn_to_remove in move[0]:
                s.board[pawn_to_remove] = 0

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


p = Plansza()
p.create_start_board()
print(p)
# pos = (6, 1)
pos = (5, 6)
# p.get_possible_moves_from_position((4, 3))
# print(p.get_possible_moves_from_position((5, 6)))
print(p.score_board_simple_method())
print(p.score_board_weighted_method())
exit(0)
possible = p.get_possible_moves_from_position(pos)
print(possible)
print(possible[0])
p = p.move_piece(pos, possible[0])
print(p)
print(p.score_board_simple_method())
