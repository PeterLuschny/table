from functools import cache
from _tabltypes import Table
from PolyaTreeAcc import polyatreeacc

"""Polya Trees by height
[0] [1]
[1] [0, 1]
[2] [0, 1,  1]
[3] [0, 1,  2,   1]
[4] [0, 1,  4,   3,   1]
[5] [0, 1,  6,   8,   4,   1]
[6] [0, 1, 10,  18,  13,   5,  1]
[7] [0, 1, 14,  38,  36,  19,  6,  1]
[8] [0, 1, 21,  76,  93,  61, 26,  7, 1]
[9] [0, 1, 29, 147, 225, 180, 94, 34, 8, 1]
"""


@cache
def polyatree(n: int) -> list[int]:
    p = polyatreeacc(n)
    return [int(n < 1)] + [p[k] - p[k-1] for k in range(1, n + 1)]


PolyaTree = Table(polyatree, "PolyaTree", 
["A034781"], None,
r"")


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PolyaTree)
