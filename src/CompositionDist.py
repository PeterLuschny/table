from functools import cache
from math import sqrt
from _tabltypes import Table

"""Compositions of n into k distinct parts.

[ 0] [1]
[ 1] [0, 1]
[ 2] [0, 1,  0]
[ 3] [0, 1,  2,  0]
[ 4] [0, 1,  2,  0,  0]
[ 5] [0, 1,  4,  0,  0, 0]
[ 6] [0, 1,  4,  6,  0, 0, 0]
[ 7] [0, 1,  6,  6,  0, 0, 0, 0]
[ 8] [0, 1,  6, 12,  0, 0, 0, 0, 0]
[ 9] [0, 1,  8, 18,  0, 0, 0, 0, 0, 0]
[10] [0, 1,  8, 24, 24, 0, 0, 0, 0, 0, 0]
[11] [0, 1, 10, 30, 24, 0, 0, 0, 0, 0, 0, 0]
[12] [0, 1, 10, 42, 48, 0, 0, 0, 0, 0, 0, 0, 0]
"""

@cache
def _compodist(n: int, k: int) -> int:
    if k < 0 or n < 0:
        return 0
    if k == 0:
        if n == 0:
            return 1
        else:
            return 0
    return _compodist(n - k, k) + k * _compodist(n - k, k - 1)


@cache
def compodist(n: int) -> list[int]:
    f = (sqrt(1 + 8*n) - 1) // 2
    return [_compodist(n, k) if k <= f else 0 for k in range(n + 1)]


CompoDist = Table(compodist, "CompositionDist", ["A072574", "A216652"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(CompoDist)
