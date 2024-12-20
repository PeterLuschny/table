from functools import cache
from PolyaTreeAcc import polyatreeacc
from _tabltypes import Table

"""
[ 0] 0
[ 1] 0, 1
[ 2] 0, 0, 1
[ 3] 0, 0, 1,  1
[ 4] 0, 0, 1,  2,  1
[ 5] 0, 0, 1,  4,  3,    1
[ 6] 0, 0, 1,  6,  8,    4,   1
[ 7] 0, 0, 1, 10,  18,  13,   5,  1
[ 8] 0, 0, 1, 14,  38,  36,  19,  6,  1
[ 9] 0, 0, 1, 21,  76,  93,  61, 26,  7, 1
"""


@cache
def rootedtree(n: int) -> list[int]:
    p = polyatreeacc(n)
    return [0] + [p[k + 1] - p[k] for k in range(n)]


RootedTree = Table(
    rootedtree,
    "RootedTree",
    ["A034781"],
    "",
    r"A375467(n, k) - A375467(n, k - 1)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(RootedTree)
