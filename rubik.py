import re
from random import randint as r

FACE_MOVES = ["U", "D", "F", "B", "L", "R"]
SLICE_MOVES = ["M", "E", "S"]
WEDGE_MOVES = ["u", "d", "f", "b", "l", "r", "Uw", "Dw", "Fw", "Bw", "Lw", "Rw"]
ROTATIONS = ["x", "y", "z"]
move_dict = {"U": 0, "L": 1, "F": 2, "R": 3, "B": 4, "D": 5, "E": 0, "M": 1, "S": 2, "x": 0, "y": 1, "z": 2, "u": 0,
             "d": 1, "f": 2, "b": 3, "l": 4, "r": 5}
ALL_MOVES = FACE_MOVES + SLICE_MOVES + WEDGE_MOVES + ROTATIONS
regex_str = "^(" + "|".join(ALL_MOVES) + ")['|2|3]{0,2}$"
##Replaced ? with {0,2}. This is not completely right because it can do U22
MOVE_REGEX = re.compile(regex_str)
FACES = {'U': 0, 'L': 1, 'F': 2, 'R': 3, 'B': 4, 'D': 5}


class Algorithm(object):
    """
    Algorithm objects are created
    """

    def __init__(self, alg):
        assert (valid_alg(alg))
        moves = alg.split()
        self.move_count = 0
        self.moves = []
        for move in moves:
            m = Move(move)
            if m.letter in FACE_MOVES or m.letter in WEDGE_MOVES:
                self.move_count += 1
            elif m.letter in SLICE_MOVES:
                self.move_count += 2
            self.moves.append(m)

    def __repr__(self):
        return " ".join([str(m) for m in self.moves])

    def num_moves(self):
        return self.move_count

    def solution(self, sol):
        c = Cube()
        c.apply_alg(self)
        c.apply_alg(sol)
        return c.solved()

    def invert(self):
        inverse_moves = []
        for m in self.moves[::-1]:
            inverse_moves.append(m.invert())
        return Algorithm(" ".join(inverse_moves))


class Move(object):
    def __init__(self, move):
        if (len(move) == 1):
            self.num = 1
            self.letter = move
        elif (len(move) == 2):
            self.letter = move[:1]
            rest = move[1:]
            if rest == "w":
                self.letter = self.letter.lower()
                self.num = 1
            if rest == "'":
                self.num = 3
            if rest == "2":
                self.num = 2
        elif (len(move) == 3):
            rest = move[1:]
            if rest == '2\'':
                # added by me -Weston
                self.letter = move[:1]
                self.num = 2
            else:
                self.letter = move[:1].lower()
                rest = move[2:]
                if rest == "'":
                    self.num = 3
                if rest == "2":
                    self.num = 2

    def __repr__(self):
        if self.num == 1:
            return self.letter
        if self.num == 2:
            return self.letter + "2"
        if self.num == 3:
            return self.letter + "'"

    def invert(self):
        inverse = ""
        inverse += self.letter
        if self.num == 1:
            inverse += "'"
        elif self.num == 2:
            inverse += "2"
        return inverse


class Cube(object):
    """
    A 3-dimensional array representation of a Rubik's cube. Act on it by calling
    c.apply_alg(alg) where alg is an Algorithm object. Additionally, check if it
    is solved with c.solved().
    """

    def __init__(self):
        self.cube = [[[i for _ in range(3)] for _ in range(3)] for i in range(6)]

    def __repr__(self):
        return str(self.cube)

    def solved(self):
        for face in range(6):
            if len(set(self.cube[face][0]).union(set(self.cube[face][1])).union(set(self.cube[face][2]))) > 1:
                return False
        return True

    ##All the f2L stuff concerns last slot

    def f2l_solved(self):
        if self.slot_corner_solved() and self.slot_edge_solved():
            return True
        return False

    def ll_oriented(self):
        face = FACES['U']
        if len(set(self.cube[face][0]).union(set(self.cube[face][1])).union(set(self.cube[face][2]))) > 1:
            return False
        return True

    def ll_edges_oriented(self):
        face = FACES['U']
        correct_color = self.cube[face][1][1]
        if self.cube[face][0][1] != correct_color:
            return False
        if self.cube[face][1][0] != correct_color:
            return False
        if self.cube[face][1][2] != correct_color:
            return False
        if self.cube[face][2][1] != correct_color:
            return False
        return True

    def last_5_edges_oriented(self):
        if self.ll_edges_oriented():
            return True
        face = FACES['U']
        correct_color = self.cube[face][1][1]
        counter = 0
        if self.cube[face][0][1] == correct_color:
            counter += 1
        if self.cube[face][1][0] == correct_color:
            counter += 1
        if self.cube[face][1][2] == correct_color:
            counter += 1
        if self.cube[face][2][1] == correct_color:
            counter += 1
        if counter == 3 and self.cube[FACES['F']][1][2] == correct_color:
            return True;

        return False

    def slot_corner_solved(self):
        if not self.f2l_minus_1_solved:
            return False
        face = FACES['F']
        if self.cube[face][1][1] != self.cube[face][2][2]:
            return False
        face = FACES['R']
        if self.cube[face][1][1] != self.cube[face][2][0]:
            return False
        face = FACES['D']
        if self.cube[face][1][1] != self.cube[face][0][2]:
            return False
        return True

    def three_move_insert_exists(self):
        if self.join_insert():
            return True
        result = False
        for i in range(4):
            self.apply_alg(Algorithm('R U\' R\''))
            if self.f2l_solved():
                result = True
        self.apply_alg(Algorithm('R U R\' U'))
        return result

    def join_insert(self):
        result = False
        for i in range(4):
            self.apply_alg(Algorithm('R U R\''))
            if self.f2l_solved():
                result = True
            self.apply_alg(Algorithm('R U\' R\' U'))
        return result

    def slot_edge_solved(self):
        if not self.f2l_minus_1_solved():
            return False
        face = FACES['F']
        if self.cube[face][1][1] != self.cube[face][1][2]:
            return False
        face = FACES['R']
        if self.cube[face][1][1] != self.cube[face][1][0]:
            return False
        return True

    def f2l_minus_1_solved(self):

        face = FACES['D']
        correct_color = self.cube[face][1][1]
        if not self.bottom_two_rows_correct_color(face):
            return False
        if self.cube[face][0][0] != correct_color:
            return False
        if self.cube[face][0][1] != correct_color:
            return False
        if not self.bottom_two_rows_correct_color(FACES['B']):
            return False
        if not self.bottom_two_rows_correct_color(FACES['L']):
            return False
        face = FACES['F']
        correct_color = self.cube[face][1][1]
        if self.cube[face][1][0] != correct_color:
            return False
        if self.cube[face][2][0] != correct_color:
            return False
        if self.cube[face][2][1] != correct_color:
            return False
        face = FACES['R']
        correct_color = self.cube[face][1][1]
        if self.cube[face][1][2] != correct_color:
            return False
        if self.cube[face][2][1] != correct_color:
            return False
        if self.cube[face][2][2] != correct_color:
            return False
        return True

    def bottom_two_rows_correct_color(self, face):
        correct_color = self.cube[face][1][1]
        for i in range(3):
            if self.cube[face][1][i] != correct_color:
                return False
        for i in range(3):
            if self.cube[face][2][i] != correct_color:
                return False
        return True

    def dump(self):
        for face in range(6):
            print
            '---'
            print
            self.cube[face]
            print
            '----'

    def _cycle_stickers(self, *args):
        t = self.cube[args[len(args) - 1][0]][args[len(args) - 1][1]][args[len(args) - 1][2]]
        loop = reversed(range(len(args)))
        for i in loop:
            if i > 0:
                self.cube[args[i][0]][args[i][1]][args[i][2]] = self.cube[args[i - 1][0]][args[i - 1][1]][
                    args[i - 1][2]]
        self.cube[args[0][0]][args[0][1]][args[0][2]] = t

    def _cycle_rows(self, *args):
        t = self.cube[args[len(args) - 1][0]][args[len(args) - 1][1]]
        loop = reversed(range(len(args)))
        for i in loop:
            if i > 0:
                self.cube[args[i][0]][args[i][1]] = self.cube[args[i - 1][0]][args[i - 1][1]]
        self.cube[args[0][0]][args[0][1]] = t

    def _rotate_face(self, face):
        # rotate the stickers on the face
        self._cycle_stickers([face, 0, 0], [face, 0, 2], [face, 2, 2], [face, 2, 0])
        self._cycle_stickers([face, 0, 1], [face, 1, 2], [face, 2, 1], [face, 1, 0])

        # U
        if face == 0:
            self._cycle_rows([4, 0], [3, 0], [2, 0], [1, 0])
        # L
        elif face == 1:
            self._cycle_stickers([0, 0, 0], [2, 0, 0], [5, 0, 0], [4, 2, 2])
            self._cycle_stickers([0, 1, 0], [2, 1, 0], [5, 1, 0], [4, 1, 2])
            self._cycle_stickers([0, 2, 0], [2, 2, 0], [5, 2, 0], [4, 0, 2])
        # F
        elif face == 2:
            self._cycle_stickers([0, 2, 0], [3, 0, 0], [5, 0, 2], [1, 2, 2])
            self._cycle_stickers([0, 2, 1], [3, 1, 0], [5, 0, 1], [1, 1, 2])
            self._cycle_stickers([0, 2, 2], [3, 2, 0], [5, 0, 0], [1, 0, 2])
        # R
        elif face == 3:
            self._cycle_stickers([0, 2, 2], [4, 0, 0], [5, 2, 2], [2, 2, 2])
            self._cycle_stickers([0, 1, 2], [4, 1, 0], [5, 1, 2], [2, 1, 2])
            self._cycle_stickers([0, 0, 2], [4, 2, 0], [5, 0, 2], [2, 0, 2])
        # B
        elif face == 4:
            self._cycle_stickers([0, 0, 0], [1, 2, 0], [5, 2, 2], [3, 0, 2])
            self._cycle_stickers([0, 0, 1], [1, 1, 0], [5, 2, 1], [3, 1, 2])
            self._cycle_stickers([0, 0, 2], [1, 0, 0], [5, 2, 0], [3, 2, 2])
        # D
        elif face == 5:
            self._cycle_rows([1, 2], [2, 2], [3, 2], [4, 2])

    def slice(self, axis):
        # E
        if axis == 0:
            self._cycle_rows([1, 1], [2, 1], [3, 1], [4, 1])

        # M
        elif axis == 1:
            self._cycle_stickers([0, 0, 1], [2, 0, 1], [5, 0, 1], [4, 2, 1])
            self._cycle_stickers([0, 1, 1], [2, 1, 1], [5, 1, 1], [4, 1, 1])
            self._cycle_stickers([0, 2, 1], [2, 2, 1], [5, 2, 1], [4, 0, 1])

        # S
        elif axis == 2:
            self._cycle_stickers([0, 1, 0], [1, 2, 1], [5, 1, 2], [3, 0, 1])
            self._cycle_stickers([0, 1, 1], [1, 1, 1], [5, 1, 1], [3, 1, 1])
            self._cycle_stickers([0, 1, 2], [1, 0, 1], [5, 1, 0], [3, 2, 1])

    def rotate(self, axis):
        # x
        if axis == 0:
            self.apply_move(Move("R"))
            self.apply_move(Move("L'"))
            self.apply_move(Move("M'"))
        # y
        elif axis == 1:
            self.apply_move(Move("U"))
            self.apply_move(Move("E'"))
            self.apply_move(Move("D'"))
        # z
        elif axis == 2:
            self.apply_move(Move("B'"))
            self.apply_move(Move("F"))
            self.apply_move(Move("S'"))

    def rotate_wedge(self, face):
        # u / Uw
        if face == 0:
            self.apply_move(Move("U"))
            self.apply_move(Move("E'"))
        # d / Dw
        elif face == 1:
            self.apply_move(Move("D"))
            self.apply_move(Move("E"))
        # f / Fw
        elif face == 2:
            self.apply_move(Move("F"))
            self.apply_move(Move("S'"))
        # b / Bw
        elif face == 3:
            self.apply_move(Move("B"))
            self.apply_move(Move("S"))
        # l / Lw
        elif face == 4:
            self.apply_move(Move("L"))
            self.apply_move(Move("M"))
        # r / Rw
        elif face == 5:
            self.apply_move(Move("R"))
            self.apply_move(Move("M'"))

    def apply_alg(self, alg):
        for move in alg.moves:
            self.apply_move(move)

    def apply_move(self, move):
        if move.letter in FACE_MOVES:
            for _ in range(move.num):
                self._rotate_face(move_dict[move.letter])
        elif move.letter in WEDGE_MOVES:
            for _ in range(move.num):
                self.rotate_wedge(move_dict[move.letter])
        elif move.letter in SLICE_MOVES:
            for _ in range(move.num):
                self.slice(move_dict[move.letter])
        elif move.letter in ROTATIONS:
            for _ in range(move.num):
                self.rotate(move_dict[move.letter])


def valid_alg(alg_str):
    """
    Check if a string is a correctly formed Rubik's cube algorithm written in standard notation
    """

    moves = alg_str.split()
    for move in moves:
        if not MOVE_REGEX.match(move):
            print("{move} does not match regex".format(move=move))
            return False
    return True


# Based on function from http://www.speedsolving.com/forum/showthread.php?25460-My-python-one-liner-scramble-generator/page21
def gen_scramble(num_moves):
    scramble = ""
    m = b = 9
    for u in range(num_moves):
        c = b;
        b = m
        while c + b - 4 and m == c or m == b:
            m = r(0, 5)
        scramble += "URFBLD"[m] + " '2"[r(0, 2)] + " "
    return scramble.replace("  ", " ")[:-1]