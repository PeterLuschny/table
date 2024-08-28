from functools import cache
from _tabltypes import Table

"""Euclid's triangle.

[ 0] [0]
[ 1] [1, 1]
[ 2] [0, 1, 0]
[ 3] [0, 1, 1, 0]
[ 4] [0, 1, 0, 1, 0]
[ 5] [0, 1, 1, 1, 1, 0]
[ 6] [0, 1, 0, 0, 0, 1, 0]
[ 7] [0, 1, 1, 1, 1, 1, 1, 0]
[ 8] [0, 1, 0, 1, 0, 1, 0, 1, 0]
[ 9] [0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
[10] [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
[11] [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
"""


@cache
def _euclid(n: int, k: int) -> int:
    while k != 0:
        t = k
        k = n % k
        n = t
    return 1 if n == 1 else 0


@cache
def euclid(n: int) -> list[int]:
    return [_euclid(i, n) for i in range(n + 1)]


Euclid = Table(euclid, "Euclid", ["A217831"], False)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Euclid, 12)
