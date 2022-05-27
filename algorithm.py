import time
from typing import Optional


# Alpha Beta prunning
# Alfa - wskazuje na najlepszą alternatywną ścieżkę dla funkcji MIN
# Beta - wskazuje na najlepszą alternatywną ścieżkę dla funkcji MAX
#   MAX(s, A, B)
#    - Znajdzmy v' = MIN(A, B)
#    - Jezeli v' > v , v = v'
#    - Jezeli v' >= B, return v <- Tutaj oznacza, ze w innej odnodze znaleziono lepsza wersje
#    Zakladajac Uklad MIN -> MAX -> MIN => Jeżeli 1 Max zwrócił 8, a drugi Max zwrócił w pierwszej odnodze 9, to nie ma to sensu, bo funkcja wyżej (min) i tak weźmie 8
#    - Jezeli V' > A, A = V'
#   return V
#
#   MIN(s, A, B)
#   - Znajdzmy v' = MAX(A, B)
#   - Jezeli v' < v, v = v'
#   - Jezeli v' <= A, return v
#   Zakladajac Uklad MAX - MIN - MAX, Jezeli 1 max zwrocil 8, a drugi MAx zwrocil w pierwszej odnodze 4, to nie ma sensu dalej spawdzac, bo funkcja wyzej (max) i tak wezmie 8
#   - Jezeli V' < B, B = V'
#  return v
#

# Max for player1
# Min for player2
class TreeNode:
    def __init__(self, entry_plansza_state, whitesTurn: bool, alpha_beta_method: bool, alpha: Optional[int] = None,
                 beta: Optional[int] = None, level=0, max_level=2, method="simple", maximise_pass=True):
        self.alpha_beta_method = alpha_beta_method
        self.method = method
        self.whitesTurn = whitesTurn
        self.max_level = max_level
        self.level = level
        self.beta = beta
        self.alpha = alpha
        self.plansza = entry_plansza_state
        self.maximise_pass = maximise_pass

    def getValue(self):
        if self.level == self.max_level:
            # Do here final return

            if self.maximise_pass:  # max
                v = None
                m = None
                moves = get_all_the_permissable_moves(self.plansza, self.whitesTurn)
                if len(moves) == 0:
                    return 100000, None
                for move in moves:
                    v_prime = get_score(self.plansza, move, self.method, self.whitesTurn)
                    if v_prime is None:
                        print("None")
                    if v is None or v_prime > v:
                        v = v_prime
                        m = move
                    if self.alpha_beta_method:
                        if self.beta is not None and v_prime >= self.beta:
                            break
                        if self.alpha is None or v_prime > self.alpha:
                            self.alpha = v_prime
                return v, m
            else:  # min
                v = None
                m = None
                moves = get_all_the_permissable_moves(self.plansza, self.whitesTurn)
                if len(moves) == 0:
                    return -100000, None
                for move in moves:
                    v_prime = get_score(self.plansza, move, self.method, self.whitesTurn)
                    if v is None or v_prime < v:
                        v = v_prime
                        m = move
                    if self.alpha_beta_method:
                        if self.alpha is not None and v_prime <= self.alpha:
                            break
                        if self.beta is None or v_prime < self.beta:
                            self.beta = v_prime
                return v, m
        else:
            # CALCULATE NEXT LEVEL
            if self.maximise_pass:  # max
                v = None
                m = None
                moves = get_all_the_permissable_moves(self.plansza, self.whitesTurn)
                if len(moves) == 0:
                    return 100000, None
                for move in moves:
                    piece, what = move
                    entry = self.plansza.move_piece(piece, what)
                    node = TreeNode(entry, self.whitesTurn, self.alpha_beta_method, self.alpha, self.beta,
                                    self.level + 1, self.max_level, self.method, not self.maximise_pass)
                    v_prime, m_prime = node.getValue()
                    if v is None or v_prime < v:
                        v = v_prime
                        m = move
                    if self.alpha_beta_method:
                        if self.alpha is not None and v_prime <= self.alpha:
                            break
                        if self.beta is None or v_prime < self.beta:
                            self.beta = v_prime
                return v, m
            else:  # min
                v = None
                m = None
                moves = get_all_the_permissable_moves(self.plansza, not self.whitesTurn)
                if len(moves) == 0:
                    return -100000, None
                for move in moves:
                    piece, what = move
                    entry = self.plansza.move_piece(piece, what)
                    node = TreeNode(entry, self.whitesTurn, self.alpha_beta_method, self.alpha, self.beta,
                                    self.level + 1, self.max_level, self.method, not self.maximise_pass)
                    v_prime, m_prime = node.getValue()
                    if v_prime is None:
                        continue
                    if v is None or v_prime > v:
                        v = v_prime
                        m = m_prime
                    if self.alpha_beta_method:

                        if self.beta is not None and v_prime >= self.beta:
                            break
                        if self.alpha is None or v_prime > self.alpha:
                            self.alpha = v_prime
                return v, m
            pass


def evaluate_best_move(current_state, whiteMove, levels, alpha_beta, method, debug=False):
    if debug:
        print(f"Evaluating the board, with alpha beta={alpha_beta} and method={method} for player white={whiteMove}")
        start_time = time.time()
    n = TreeNode(current_state, whiteMove, alpha_beta, method=method, max_level=levels)
    v, move = n.getValue()
    # print(v, move)
    if debug:
        delta_time = time.time() - start_time
        print(f"Operation took {delta_time}")
    return move


def get_score(plansza, move, method, negate_score=False):
    piece, what = move
    # target, typ = what
    t = plansza.move_piece(piece, what)

    if method == "simple":
        score = t.score_board_simple_method()
    elif method == "weighted":
        score = t.score_board_weighted_method()
    elif method == "simple_moveable":
        score = t.score_board_simple_method() + t.score_board_moveable()
    elif method == "simple_safe":
        score = t.score_board_simple_method() + t.score_safe_pawns()

    if negate_score:
        return -1 * score
    return score


def get_pos_of_all(plansza, white):
    poses = []
    for y in range(0, 8):
        for x in range(0, 8):
            if white and plansza.board[y, x] < 0:
                poses.append((y, x))
            elif not white and plansza.board[y, x] > 0:
                poses.append((y, x))
    return poses


# list of tuple[pos, move, final_board]
def get_all_the_permissable_moves(plansza, im_white):
    moves = []
    for pos in get_pos_of_all(plansza, im_white):
        l = plansza.get_possible_moves_from_position(pos)
        for move in l:
            moves.append((pos, move))

    if any(x[1][1] == 1 for x in moves):
        moves = list(filter(lambda d: d[1][1] == 1, moves))
        maxLen = len(max(moves, key=lambda d: len(d[1][0]))[1][0])
        moves = list(filter(lambda d: len(d[1][0]) == maxLen, moves))

    return moves

# # algorithm assumes it's max turn first
# def min_max(plansza: Plansza, steps: int, im_white: bool, score_method: str = "simple"):
#     current_boards = [plansza]
#     for i in range(steps):
#         for pl in current_boards:
#             evaluation = evaluate_all_moves(pl, im_white, score_method)
