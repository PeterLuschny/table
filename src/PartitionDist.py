from functools import cache
from math import sqrt
from _tabltypes import Table

"""Partitions of n having k distinct parts.

[0]  [1]
[1]  [0, 1]
[2]  [0, 1, 0]
[3]  [0, 1, 1, 0]
[4]  [0, 1, 1, 0, 0]
[5]  [0, 1, 2, 0, 0, 0]
[6]  [0, 1, 2, 1, 0, 0, 0]
[7]  [0, 1, 3, 1, 0, 0, 0, 0]
[8]  [0, 1, 3, 2, 0, 0, 0, 0, 0]
[9]  [0, 1, 4, 3, 0, 0, 0, 0, 0, 0]
[10] [0, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0]

"""


@cache
def _partdist(n: int, k: int) -> int:
    if k < 1 or n < k:
        return 0
    if n == 1:
        return 1

    return _partdist(n - k, k) + _partdist(n - k, k - 1)


@cache
def partdist(n: int) -> list[int]:
    if n == 0:
        return [1]

    f = (sqrt(1 + 8*n) - 1) // 2
    return [_partdist(n, k) if k <= f else 0 for k in range(n + 1)]


PartDist = Table(
    partdist, 
    "PartitionDist", 
    ["A008289"], 
    "",
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PartDist)
