from functools import cache
from _tabltypes import Table

"""Partition numbers (Euler's table), see also A026820, A000041.

[0] 1
[1] 0, 1
[2] 0, 1, 1
[3] 0, 1, 1, 1
[4] 0, 1, 2, 1, 1
[5] 0, 1, 2, 2, 1, 1
[6] 0, 1, 3, 3, 2, 1, 1
[7] 0, 1, 3, 4, 3, 2, 1, 1
[8] 0, 1, 4, 5, 5, 3, 2, 1, 1
[9] 0, 1, 4, 7, 6, 5, 3, 2, 1, 1
"""


@cache
def part(n: int, k: int) -> int:
    if k < 0 or n < 0:
        return 0
    if k == 0:
        return 1 if n == 0 else 0

    return part(n - 1, k - 1) + part(n - k, k)


@cache
def partition(n: int) -> list[int]:
    return [part(n, k) for k in range(n + 1)]


Partition = Table(
    partition,
    "Partition",
    ["A072233", "A008284", "A058398"],
    "A000000",
    r"T_{n - 1, k - 1} + T_{n - k, k}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Partition)
