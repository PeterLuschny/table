from functools import cache
from _tabltypes import Table
from EytzingerOrder import eytzingerorder

""" 
    Let T(n) denote the triangular numbers. Set, for n >= 0, 
    I(n) = [T(n), T(n+1)), lower bound included, upper bound excluded. 
    Applying the Eytzinger ordering to I(n) gives 
    E(n) = [eytzingerorder(n + 1, k + 1) + T(n) - 1 for k in 0..n]. 
    Joining E(0), E(1), E(2), ... gives a permutation of the nonnegative integers. 

    [0] [ 0]
    [1] [ 2,  1]
    [2] [ 4,  3,  5]
    [3] [ 8,  7,  9, 6]
    [4] [13, 11, 14, 10, 12]
    [5] [18, 16, 20, 15, 17, 19]
    [6] [24, 22, 26, 21, 23, 25, 27]
    [7] [32, 30, 34, 29, 31, 33, 35, 28]
    [8] [41, 39, 43, 37, 40, 42, 44, 36, 38]
    [9] [51, 48, 53, 46, 50, 52, 54, 45, 47, 49]
"""

@cache
def eytzingerpermutation(n: int) -> list[int]:
    t = n * (n + 1) // 2
    return [eytzingerorder(n)[k] + t for k in range(n + 1)]


EytzingerPermutation = Table(eytzingerpermutation, "EytzingerPerm", ["A375469"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(EytzingerPermutation)
