from functools import cache
from math import sqrt
from _tabltypes import Table

"""Partitions of n having exactly k distinct part sizes, A365676.

[0] 1;
[1] 0, 1;
[2] 0, 2,  0;
[3] 0, 2,  1,  0;
[4] 0, 3,  2,  0, 0;
[5] 0, 2,  5,  0, 0, 0;
[6] 0, 4,  6,  1, 0, 0, 0;
[7] 0, 2, 11,  2, 0, 0, 0, 0;
[8] 0, 4, 13,  5, 0, 0, 0, 0, 0;
[9] 0, 3, 17, 10, 0, 0, 0, 0, 0, 0;

[6, 1] -> [[1, 1, 1, 1, 1, 1], [2, 2, 2], [3, 3], [6]]
[6, 2] -> [[1, 1, 1, 1, 2], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 4], [2, 4], [1, 5]]
[6, 3] -> [[1, 2, 3]]
"""


@cache
def _partdistsize(n: int, k: int, r: int) -> int:
    if n == 0:
        return 1 if k == 0 else 0
    if k == 0 or r == 0:
        return 0
    if k > n // 2 + 1: return 0
    return (sum(_partdistsize(n - r * j, k - 1, r - 1) 
            for j in range(1, n // r + 1))
           + _partdistsize(n, k, r - 1))


@cache
def partdistsize(n: int) -> list[int]:
    f = (sqrt(1 + 8*n) - 1) // 2
    return [_partdistsize(n, k, n) if k <= f else 0 for k in range(n + 1)]


PartDistSize = Table(partdistsize, "PartitionDistSize", 
["A365676", "A116608", "A060177"], False,
r"")


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PartDistSize)

