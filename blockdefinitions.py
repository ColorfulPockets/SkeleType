import rubik

x = rubik.Algorithm('x')
y = rubik.Algorithm('y')
z = rubik.Algorithm('z')

moves = ["R", "R'", "R2", "U", "U'", "U2", "F", "F'", "F2", "L", "L'", "L2", "D", "D'", "D2", "B", "B'", "B2"]
moves_open_paren = ["(" + move for move in moves]
moves_closed_paren = [move + ")" for move in moves]
moves_both_paren = ["(" + move + ")" for move in moves]

movesprime = [move + "'" for move in rubik.FACE_MOVES]
movestwo = [move + "2" for move in rubik.FACE_MOVES]

# checks if UFL square is solved
def square_solved(c):
    if not (c.cube[0][1][0] == c.cube[0][1][1] == c.cube[0][2][0] == c.cube[0][2][1]):
        return False

    c.apply_alg(z)
    if not c.cube[0][1][2] == c.cube[0][2][2]:
        c.apply_alg(rubik.Algorithm("z'"))
        return False

    c.apply_alg(x)
    if c.cube[0][0][2] == c.cube[0][1][2]:
        c.apply_alg(rubik.Algorithm('y z z x'))
        return True
    else:
        c.apply_alg(rubik.Algorithm('y z z x'))
        return False


# checks if UFL 2x2x2 is solved
def twobytwosolved(c):
    is_solved = True
    for i in range(3):
        c.apply_alg(z)
        c.apply_alg(y)
        if not square_solved(c):
            is_solved = False
    return is_solved


# checks if UF 2x2x3 is solved
def twobytwobythreesolved(c):
    if not twobytwosolved(c):
        return False

    c.apply_alg(y)
    if not square_solved(c):
        c.apply_alg(rubik.Algorithm("y'"))
        return False

    c.apply_alg(rubik.Algorithm("x y'"))
    if square_solved(c):
        c.apply_alg(z)
        return True
    else:
        c.apply_alg(z)
        return False


# checks if UF roux block is solved
def rouxsolved(c):
    if not square_solved(c):
        return False
    c.apply_alg(y)
    if square_solved(c):
        c.apply_alg(rubik.Algorithm("y'"))
        return True
    else:
        c.apply_alg(rubik.Algorithm("y'"))
        return False

# checks if diamond on UFL and UBR corners is solved
def diamondsolved(c):
    if not twobytwosolved(c):
        return False
    c.apply_alg(rubik.Algorithm("y2"))
    if twobytwosolved(c):
        c.apply_alg(rubik.Algorithm("y2"))
        return True
    else:
        c.apply_alg(rubik.Algorithm("y2"))
        return False


# checks if F2L on U missing BL pair is solved
def f2lminus1solved(c):
    if not twobytwosolved(c):
        return False
    c.apply_alg(y)
    if not twobytwosolved(c):
        c.apply_alg(rubik.Algorithm("y'"))
        return False
    c.apply_alg(y)
    if twobytwosolved(c):
        c.apply_alg(rubik.Algorithm("y2"))
        return True
    else:
        c.apply_alg(rubik.Algorithm("y2"))
        return False


# checks F2L on U
def f2lsolved(c):
    if not twobytwobythreesolved(c):
        return False
    c.apply_alg(rubik.Algorithm("y2"))
    if twobytwobythreesolved(c):
        c.apply_alg(rubik.Algorithm("y2"))
        return True
    else:
        c.apply_alg(rubik.Algorithm("y2"))
        print("false")
        return False


# checks cross on U
def cross_solved(c):
    if not c.cube[0][0][1] == c.cube[0][1][0] == c.cube[0][1][2] == c.cube[0][2][1] == c.cube[0][1][1]:
        return False
    c.apply_alg(x)
    is_solved = True
    for i in range(4):
        c.apply_alg(z)
        if not c.cube[0][0][1] == c.cube[0][1][1]:
            is_solved = False
    c.apply_alg(rubik.Algorithm("x'"))
    return is_solved


# checks if F front EO is done
def eosolved(c):
    up = c.cube[0][1][1]
    c.apply_alg(z)
    left = c.cube[0][1][1]
    c.apply_alg(z)
    down = c.cube[0][1][1]
    c.apply_alg(z)
    right = c.cube[0][1][1]

    if c.cube[0][0][1] == up or c.cube[0][1][0] == up or c.cube[0][1][2] == up or c.cube[0][2][1] == up or (
      c.cube[0][0][1]) == down or c.cube[0][1][0] == down or c.cube[0][1][2] == down or c.cube[0][2][1] == down:
        c.apply_alg(z)
        return False

    c.apply_alg(rubik.Algorithm("z2"))

    if c.cube[0][0][1] == up or c.cube[0][1][0] == up or c.cube[0][1][2] == up or c.cube[0][2][1] == up or (
      c.cube[0][0][1]) == down or c.cube[0][1][0] == down or c.cube[0][1][2] == down or c.cube[0][2][1] == down:
        c.apply_alg(rubik.Algorithm("z'"))
        return False

    c.apply_alg(z)

    if c.cube[0][0][1] == left or c.cube[0][1][0] == left or c.cube[0][1][2] == left or c.cube[0][2][1] == left or (
      c.cube[0][0][1]) == right or c.cube[0][1][0] == right or c.cube[0][1][2] == right or c.cube[0][2][1] == right:
        c.apply_alg(rubik.Algorithm("z2"))
        return False

    c.apply_alg(rubik.Algorithm("z2"))

    if c.cube[0][0][1] == left or c.cube[0][1][0] == left or c.cube[0][1][2] == left or c.cube[0][2][1] == left or (
      c.cube[0][0][1]) == right or c.cube[0][1][0] == right or c.cube[0][1][2] == right or c.cube[0][2][1] == right:
        return False

    c.apply_alg(x)

    if c.cube[0][1][0] == left or c.cube[0][1][2] == left or c.cube[0][1][0] == right or c.cube[0][1][2] == right:
        c.apply_alg(rubik.Algorithm("x'"))
        return False

    c.apply_alg(rubik.Algorithm("x2"))

    if c.cube[0][1][0] == left or c.cube[0][1][2] == left or c.cube[0][1][0] == right or c.cube[0][1][2] == right:
        c.apply_alg(x)
        return False

    c.apply_alg(y)

    if c.cube[0][1][0] == up or c.cube[0][1][2] == up or c.cube[0][1][0] == down or c.cube[0][1][2] == down:
        c.apply_alg(rubik.Algorithm("y' x'"))
        return False

    c.apply_alg(rubik.Algorithm("x2"))

    if c.cube[0][1][0] == up or c.cube[0][1][2] == up or c.cube[0][1][0] == down or c.cube[0][1][2] == down:
        c.apply_alg(rubik.Algorithm("y x'"))
        return False

    c.apply_alg(rubik.Algorithm("y x'"))
    return True


# checks if pdr with EO on F and R is done
def pdrsolved(c):
    if not eosolved(c):
        return False
    c.apply_alg(y)

    if not eosolved(c):
        c.apply_alg(rubik.Algorithm("y'"))
        return False
    c.apply_alg(rubik.Algorithm("y'"))

    return True


# TODO: The logic here is wrong, doesn't check EO for E-Layer, and can be tricked if the U/D faces have just two colors,
#  but they're not the DR colors. I couldn't get DR detection to work, though, so this will suffice for now.
def dominosolved(c):
    is_solved = True

    c.apply_alg(rubik.Algorithm("z2"))

    if not c.ll_oriented:
        is_solved = False

    c.apply_alg(rubik.Algorithm("z2"))

    if not c.ll_oriented:
        is_solved = False

    return is_solved


def check24positions(func, c):
    for i in range(24):
        if i == 4 or i == 8 or i == 12:
            c.apply_alg(z)
        if i == 16:
            c.apply_alg(x)
        if i == 20:
            c.apply_alg(rubik.Algorithm('x2'))
        if func(c):
            return True
        c.apply_alg(y)
    return False


def check12positions(func, c):
    for i in range(12):
        if i == 4:
            c.apply_alg(y)
        if i == 8:
            c.apply_alg(z)
        if func(c):
            return True
        c.apply_alg(x)
    return False


def check8positions(func, c):
    for i in range(8):
        c.apply_alg(y)
        if i == 4:
            c.apply_alg(rubik.Algorithm("x2"))

        if func(c):
            return True
    return False


def check6positions(func, c):
    for i in range(4):
        c.apply_alg(x)
        if func(c):
            return True
    c.apply_alg(z)
    if func(c):
        return True
    c.apply_alg(rubik.Algorithm("z2"))
    if func(c):
        return True
    return False
