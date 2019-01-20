import rubik

x = rubik.Algorithm('x')
y = rubik.Algorithm('y')
z = rubik.Algorithm('z')

def square_solved(c):
    if c.cube[0][1][0] == c.cube[0][1][1] == c.cube[0][2][0] == c.cube[0][2][1]:
        return True
    else:
        return False

def twobytwosolved(c):
    good = 0
    rot_count = 0
    for j in range(3):
        if not square_solved(c):
            while rot_count < 3:
                c.apply_alg(z)
                c.apply_alg(y)
                rot_count = rot_count + 1
            break
        c.apply_alg(z)
        c.apply_alg(y)
        good = good + 1
        rot_count = rot_count + 1
    if good == 3:
        return True
    else:
        return False

