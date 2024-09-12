from functools import cache
from typing import Callable

@cache
def Divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]

def Euler2Transform(T: Callable[[int, int], int]) -> Callable[[int, int], int]:
    @cache
    def H(n: int, k: int) -> int:
        return sum(d * T(d, k) for d in Divisors(n) if k <= d)

    @cache
    def S(n: int, k: int) -> int:
        if k == 0: return int(n == 0)
        if n == 1: return int(k > 0)
        s = sum(S(j, k) * H(n - j, k - 1) for j in range(1, n))
        return s // (n - 1)

    def U(n:int, k:int)->int:
        if n == 0: return 1
        return S(n + 1, k + 1)

    return U


if __name__ == "__main__":

    from math import comb
    from _tabltypes import Table

    def binomial(n:int, k:int) -> int: 
        if n < 0 or k < 0: return 0
        return comb(n, k)

    print("Binomial")
    T = Euler2Transform(binomial)

    for n in range(9): 
        print([T(n, k) for k in range(n + 1)], 
              sum([T(n, k) for k in range(n + 1)]))

    from Lah import Lah                           # type: ignore
    from One import One                           # type: ignore
    from Fubini import Fubini                     # type: ignore
    from StirlingSet import StirlingSet           # type: ignore
    from StirlingCycle import StirlingCycle       # type: ignore
    from FallingFactorial import FallingFactorial # type: ignore
    from RisingFactorial import RisingFactorial   # type: ignore

    R: list[Table] = [One, Lah, Fubini, StirlingSet, StirlingCycle,
         FallingFactorial, RisingFactorial]

    for r in R:
        t = Euler2Transform(r.val)
        print(r.id, r.sim)
        for n in range(9): 
            row = [t(n, k) for k in range(n + 1)]
            print([n], row, "sum", sum(row))

"""
Binomial
[1] 1
[1, 1] 2
[2, 3, 1] 6
[3, 6, 3, 1] 13
[5, 13, 7, 4, 1] 30
[7, 24, 13, 10, 5, 1] 60
[11, 48, 28, 21, 15, 6, 1] 130
[15, 86, 52, 39, 35, 21, 7, 1] 256
[22, 160, 107, 76, 71, 56, 28, 8, 1] 529
One
[0] [1] sum 1
[1] [1, 1] sum 2
[2] [2, 2, 1] sum 5
[3] [3, 3, 1, 1] sum 8
[4] [5, 5, 2, 1, 1] sum 14
[5] [7, 7, 2, 1, 1, 1] sum 19
[6] [11, 11, 4, 2, 1, 1, 1] sum 31
[7] [15, 15, 4, 2, 1, 1, 1, 1] sum 40
[8] [22, 22, 7, 3, 2, 1, 1, 1, 1] sum 60
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
