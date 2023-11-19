import math
import Warnsdorff

def test(k):
    s = "27 42 37 30 21 14 19 6 1 36 31 28 43 38 7 2 13 18 41 26 33 22 29 20 15 10 5 32 35 24 39 44 3 8 17 12 25 40 45 34 23 16 11 4 9" # 46 63 50 57 54 51 58 55 62 49 64 47 60 53 56 59 52 65 48 61
    num = 9
    s = s.split()
    l = []
    i = 0
    while i < len(l):
        c = s.index(str(i + 1))
        l.append((c // num, c%num))
        i += 1
    print(len(l))
    print(l)
    return l


c5 = [(0, 0), (2, 1), (4, 0), (3, 2), (4, 4), (2, 3), (0, 4), (1, 2), (2, 4), (4, 3), (3, 1), (1, 0), (0, 2), (1, 4), (3, 3), (4, 1), (2, 0), (0, 1), (1, 3), (3, 4), (2, 2), (0, 3), (1, 1), (3, 0), (4, 2)]
t6 = [(0, 5), (1, 3), (0, 1), (2, 0), (4, 1), (5, 3), (4, 5), (2, 4), (0, 3), (1, 5), (3, 4), (2, 2), (1, 0), (0, 2), (1, 4), (3, 5), (5, 4), (4, 2), (5, 0), (3, 1), (4, 3), (5, 1), (3, 0), (1, 1), (2, 3), (0, 4), (2, 5), (4, 4), (3, 2), (4, 0), (2, 1), (0, 0), (1, 2), (3, 3), (5, 2)]
t7 = [(0, 6), (1, 4), (2, 6), (0, 5), (1, 3), (0, 1), (2, 0), (1, 2), (0, 0), (2, 1), (0, 2), (1, 0), (3, 1), (5, 0), (4, 2), (6, 1), (4, 0), (5, 2), (6, 0), (4, 1), (3, 3), (2, 5), (0, 4), (1, 6), (3, 5), (5, 4), (4, 6), (3, 4), (1, 5), (2, 3), (1, 1), (3, 0), (2, 2), (0, 3), (2, 4), (3, 6), (4, 4), (6, 3), (5, 1), (3, 2), (5, 3), (4, 5), (6, 4), (4, 3), (6, 2)]
t8 = [(0, 7), (1, 5), (2, 7), (0, 6), (1, 4), (0, 2), (1, 0), (3, 1), (5, 0), (7, 1), (6, 3), (5, 1), (7, 0), (6, 2), (7, 4), (5, 3), (6, 1), (7, 3), (5, 2), (6, 0), (4, 1), (2, 0), (0, 1), (2, 2), (0, 3), (1, 1), (3, 0), (4, 2), (2, 3), (0, 4), (1, 6), (3, 7), (2, 5), (1, 7), (0, 5), (1, 3), (3, 4), (4, 6), (5, 4), (3, 5), (4, 7), (2, 6), (4, 5), (3, 3), (1, 2), (0, 0), (2, 1), (4, 0), (3, 2), (4, 4), (3, 6), (2, 4), (4, 3), (6, 4), (7, 2)]
t9 = [(0, 8), (1, 6), (3, 5), (4, 7), (2, 8), (0, 7), (1, 5), (3, 6), (4, 8), (2, 7), (4, 6), (3, 8), (1, 7), (0, 5), (2, 6), (4, 5), (3, 7), (1, 8), (0, 6), (2, 5), (0, 4), (2, 3), (4, 4), (3, 2), (4, 0), (2, 1), (0, 0), (1, 2), (2, 4), (0, 3), (1, 1), (3, 0), (2, 2), (4, 3), (3, 1), (1, 0), (0, 2), (1, 4), (3, 3), (4, 1), (2, 0), (0, 1), (1, 3), (3, 4), (4, 2), (5, 0), (7, 1), (8, 3), (6, 4), (5, 2), (6, 0), (8, 1), (7, 3), (5, 4), (6, 2), (7, 4), (5, 3), (6, 1), (8, 0), (7, 2), (8, 4), (6, 3), (5, 1), (7, 0), (8, 2)]

c6 = [(0, 0), (2, 1), (4, 0), (3, 2), (5, 1), (3, 0), (1, 1), (0, 3), (1, 5), (3, 4), (5, 5), (4, 3), (3, 5), (5, 4), (4, 2), (5, 0), (3, 1), (1, 0), (0, 2), (1, 4), (2, 2), (0, 1), (2, 0), (4, 1), (5, 3), (4, 5), (2, 4), (0, 5), (1, 3), (2, 5), (4, 4), (2, 3), (0, 4), (1, 2), (3, 3), (5, 2)]
c7 = [(0, 0), (1, 2), (2, 0), (0, 1), (1, 3), (0, 5), (2, 6), (1, 4), (0, 6), (2, 5), (0, 4), (1, 6), (3, 5), (5, 6), (4, 4), (6, 5), (4, 6), (5, 4), (6, 6), (4, 5), (3, 3), (2, 1), (0, 2), (1, 0), (3, 1), (5, 0), (6, 2), (4, 1), (6, 0), (5, 2), (4, 0), (6, 1), (5, 3), (3, 2), (5, 1), (6, 3), (5, 5), (3, 6), (2, 4), (0, 3), (1, 1), (3, 0), (4, 2), (2, 3), (1, 5), (3, 4), (2, 2), (4, 3), (6, 4)]


def rotate_clockwise(t):
    l = t.copy()
    n = math.ceil(math.sqrt(len(l)))
    for i in range(0, len(l)):
        l[i] = tuple((n - 1 - l[i][1], l[i][0]))
    return l

def transpose(t):
    l = t.copy()
    n = math.ceil(math.sqrt(len(l)))
    for i in range(0, len(l)):
        l[i] = tuple((l[i][1], l[i][0]))
    return l

def shift(t, x, y):
    l = t.copy()
    for i in range(0, len(l)):
        l[i] = tuple((x + l[i][0], y + l[i][1]))
    return l

def divide_and_conquer(n):
    path = solve(n)
    for i in range(1, len(path)):
        if abs(path[i][0] - path[i - 1][0]) == 2 and abs(path[i][1] - path[i - 1][1]) == 1 or abs(path[i][0] - path[i - 1][0]) == 1 and abs(path[i][1] - path[i - 1][1]) == 2:
            pass
        else:
            print(i)
            # return []
    return path

def get_path(m, n):
    assert m == n, "board should be square"
    return divide_and_conquer(m)

m = 0
def solve1(n, t, x=0, y=0, it=0):
    if n <= 9:
        return Warnsdorff.get_path(n, n)
    if it%2 == 0:
        path = []
        for i in range(0, n // 5 - 1):
            path += shift(c5, x, y)
            x += 5
        path += shift(rotate_clockwise(t), x, y)
        x += n%5
        y += n%5 + 5
        for i in range(0, n // 5 - 2):
            path += shift(transpose(c5), x, y)
            y += 5
        path += shift(rotate_clockwise(transpose(c5)), x, y)
        y += 5
        ret = solve1(n - 5, t, x - 5, y - 5, it + 1)
        if n - 5 <= 9:
            path += shift(rotate_clockwise(rotate_clockwise(ret)), x - n + 5, y - n + 5)
        else:
            path += ret
    else:
        path = []
        for i in range(0, n // 5 - 1):
            path += shift(rotate_clockwise(rotate_clockwise(transpose(c5))), x, y)
            y -= 5
        x -= n%5
        y -= n%5
        path += shift(rotate_clockwise(transpose(t)), x, y)
        for i in range(0, n // 5 - 2):
            x -= 5
            path += shift(rotate_clockwise(rotate_clockwise(c5)), x, y)
        x -= 5
        path += shift(rotate_clockwise(c5), x, y)
        ret = solve1(n - 5, t, x, y + 5, it + 1)
        if n - 5 <= 9:
            path += shift(ret, x, y + 5)
        else:
            path += ret
    return path


def solve2(n, x=0, y=0, it=0):
    if n <= 9:
        return Warnsdorff.get_path(n, n)
    if it % 2 == 0:
        path = []
        for i in range(0, n // 5 - 1):
            path += shift(c5, x, y)
            x += 5
        path += shift(transpose(c5), x, y)
        x += n % 5
        y += n % 5 + 5
        for i in range(0, n // 5 - 2):
            path += shift(transpose(c5), x, y)
            y += 5
        path += shift(rotate_clockwise(transpose(c5)), x, y)
        y += 5
        ret = solve2(n - 5, x - 5, y - 5, it + 1)
        if n - 5 <= 9:
            path += shift(rotate_clockwise(rotate_clockwise(ret)), x - n + 5, y - n + 5)
        else:
            path += ret
    else:
        path = []
        for i in range(0, n // 5 - 1):
            path += shift(rotate_clockwise(rotate_clockwise(transpose(c5))), x, y)
            y -= 5
        x -= n % 5
        y -= n % 5
        path += shift(rotate_clockwise(rotate_clockwise(c5)), x, y)
        for i in range(0, n // 5 - 2):
            x -= 5
            path += shift(rotate_clockwise(rotate_clockwise(c5)), x, y)
        x -= 5
        path += shift(rotate_clockwise(c5), x, y)
        ret = solve2(n - 5, x, y + 5, it + 1)
        if n - 5 <= 9:
            path += shift(ret, x, y + 5)
        else:
            path += ret
    return path

def solve(n):
    global m
    m = n
    k = n%5 + 5
    if k == 6:
        return solve1(n, t6)
    elif k == 7:
        return solve1(n, t7)
    elif k == 8:
        return solve1(n, t8)
    elif k == 9:
        return solve1(n, t9)
    return solve2(n)

