from functools import cache
from typing import Callable
from _tabltypes import Table


@cache
def Divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]


@cache
def H(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in Divisors(n) if k <= d)


@cache
def e(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in Divisors(n) if k == d)


def Euler1Transform(a: Callable[[int], int]) -> Callable[[int], int]:

    @cache
    def s(n: int) -> int:
        return sum(d * a(d) for d in Divisors(n))

    @cache
    def p(n: int) -> int:
        if n == 0:
            return 1
        return sum(s(j) * p(n - j) for j in range(1, n + 1)) // n
    return p


def Euler1Generator(T: Table, rows: int, size: int) -> list[list[int]]:
    L: list[list[int]] = []
    for j in range(rows):
        c = T.col(j, size)
        b = Euler1Transform(lambda n: c[n])
        L.append([b(n) for n in range(size)])
    return L


def Euler2Transform(T: Callable[[int, int], int]) -> Callable[[int, int], int]:
    @cache
    def s(n: int, k: int) -> int:
        return sum(d * T(d, k) for d in Divisors(n) if k <= d)

    @cache
    def p(n: int, k: int) -> int:
        if k == 0:
            return int(n == 0)
        if n == 1:
            return int(k > 0)
        r = sum(p(j, k) * s(n - j, k - 1) for j in range(1, n))
        return r // (n - 1)

    def u(n: int, k: int) -> int:
        if n == 0:
            return 1
        return p(n + 1, k + 1)

    return u


def Euler2Generator(T: Table) -> Table:
    H = Euler2Transform(T.val)

    def gen(n: int) -> list[int]:
        return [H(n, k) for k in range(n + 1)]
    return Table(gen, "Euler2Trans of " + T.id)


if __name__ == "__main__":

    from math import comb
    from Tables import Tables
    from One import One

    def binomial(n: int, k: int) -> int:
        return comb(n, k)

    print("The Euler transform of the binomial.")
    T = Euler2Transform(binomial)
    for n in range(9):
        print([T(n, k) for k in range(n + 1)])

    print("\nThe Euler transform of ONE.")
    print("dim1")
    o = Euler1Transform(lambda n: 1)
    print([o(n) for n in range(12)])

    print("dim2")
    O = Euler2Generator(One)
    O.show(9)

    def CheckE2T(T: Table) -> None:
        ET = Euler2Generator(T)
        print()
        print(ET.id)
        ET.show(10)
        print("Row sums", ET.sum(10))

        print("Euler1Trans")
        L = Euler1Generator(T, 4, 8)
        for l in L: print(l)

        input("Hit Return/Enter here > ")

    for t in Tables:
        CheckE2T(t)  # type: ignore


"""
Euler2Trans of One
[0] [1]
[1] [1, 1]
[2] [2, 2, 1]
[3] [3, 3, 1, 1]
[4] [5, 5, 2, 1, 1]
[5] [7, 7, 2, 1, 1, 1]
[6] [11, 11, 4, 2, 1, 1, 1]
[7] [15, 15, 4, 2, 1, 1, 1, 1]
[8] [22, 22, 7, 3, 2, 1, 1, 1, 1]
[9] [30, 30, 8, 4, 2, 1, 1, 1, 1, 1]
Row sums [1, 2, 5, 8, 14, 19, 31, 40, 60, 79]
Euler1Trans
[1, 1, 2, 3, 5, 7, 11, 15]
[1, 1, 2, 3, 5, 7, 11, 15]
[1, 1, 2, 3, 5, 7, 11, 15]
[1, 1, 2, 3, 5, 7, 11, 15]

Euler2Trans of Binomial
[0] [1]
[1] [1, 1]
[2] [2, 3, 1]
[3] [3, 6, 3, 1]
[4] [5, 13, 7, 4, 1]
[5] [7, 24, 13, 10, 5, 1]
[6] [11, 48, 28, 21, 15, 6, 1]
[7] [15, 86, 52, 39, 35, 21, 7, 1]
[8] [22, 160, 107, 76, 71, 56, 28, 8, 1]
[9] [30, 282, 203, 145, 131, 126, 84, 36, 9, 1]
Row sums [1, 2, 6, 13, 30, 60, 130, 256, 529, 1047]
Euler1Trans
[1, 1, 2, 3, 5, 7, 11, 15]
[1, 2, 6, 14, 33, 70, 149, 298]
[1, 3, 12, 38, 117, 330, 906, 2367]
[1, 4, 20, 80, 305, 1072, 3622, 11676]

Lah
[0] [1] sum 1
[1] [0, 1] sum 1
[2] [0, 3, 1] sum 4
[3] [0, 9, 6, 1] sum 16
[4] [0, 36, 37, 12, 1] sum 86
[5] [0, 168, 246, 120, 20, 1] sum 555
[6] [0, 961, 1858, 1201, 300, 30, 1] sum 4351
[7] [0, 6403, 15582, 12612, 4200, 630, 42, 1] sum 39470
[8] [0, 49302, 145084, 141318, 58801, 11760, 1176, 56, 1] sum 407498
Belll
[0] [1]
[1] [1, 2]
[2] [3, 6, 5]
[3] [8, 17, 10, 15]
[4] [26, 54, 42, 37, 52]
[5] [88, 179, 137, 114, 151, 203]
[6] [340, 657, 547, 529, 523, 674, 877]
[7] [1411, 2598, 2190, 2212, 2066, 2589, 3263, 4140]
[8] [6417, 11219, 9705, 9845, 10467, 11155, 13744, 17007, 21147]
Fubini
[0] [1] sum 1
[1] [0, 1] sum 1
[2] [0, 2, 2] sum 4
[3] [0, 3, 6, 6] sum 15
[4] [0, 5, 17, 36, 24] sum 82
[5] [0, 7, 42, 150, 240, 120] sum 559
[6] [0, 11, 115, 561, 1560, 1800, 720] sum 4767
[7] [0, 15, 288, 2022, 8400, 16800, 15120, 5040] sum 47685
[8] [0, 22, 752, 7362, 41124, 126000, 191520, 141120, 40320] sum 548220
StirlingSet
[0] [1] sum 1
[1] [0, 1] sum 1
[2] [0, 2, 1] sum 3
[3] [0, 3, 3, 1] sum 7
[4] [0, 5, 8, 6, 1] sum 20
[5] [0, 7, 18, 25, 10, 1] sum 61
[6] [0, 11, 45, 91, 65, 15, 1] sum 228
[7] [0, 15, 102, 307, 350, 140, 21, 1] sum 936
[8] [0, 22, 245, 1012, 1702, 1050, 266, 28, 1] sum 4326
StirlingCycle
[0] [1] sum 1
[1] [0, 1] sum 1
[2] [0, 2, 1] sum 3
[3] [0, 4, 3, 1] sum 8
[4] [0, 11, 12, 6, 1] sum 30
[5] [0, 37, 53, 35, 10, 1] sum 136
[6] [0, 167, 292, 226, 85, 15, 1] sum 786
[7] [0, 925, 1850, 1630, 735, 175, 21, 1] sum 5337
[8] [0, 6164, 13576, 13188, 6770, 1960, 322, 28, 1] sum 42009
FallingFact
[0] [1] sum 1
[1] [1, 1] sum 2
[2] [2, 3, 2] sum 7
[3] [3, 6, 6, 6] sum 21
[4] [5, 13, 15, 24, 24] sum 81
[5] [7, 24, 32, 60, 120, 120] sum 363
[6] [11, 48, 79, 141, 360, 720, 720] sum 2079
[7] [15, 86, 172, 354, 840, 2520, 5040, 5040] sum 14067
[8] [22, 160, 397, 996, 1980, 6720, 20160, 40320, 40320] sum 111075
RisingFact
[0] [1] sum 1
[1] [1, 1] sum 2
[2] [2, 3, 6] sum 11
[3] [3, 6, 12, 60] sum 81
[4] [5, 13, 41, 120, 840] sum 1019
[5] [7, 24, 102, 210, 1680, 15120] sum 17143
[6] [11, 48, 296, 2166, 3024, 30240, 332640] sum 368425
[7] [15, 86, 728, 7704, 5040, 55440, 665280, 8648640] sum 9382933
[8] [22, 160, 1908, 20580, 361140, 95040, 1235520, 17297280, 259459200] sum 278470850
"""
