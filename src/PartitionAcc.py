from functools import cache
from itertools import accumulate
from _tabltypes import Table
from Partition import partition

"""Euler's table, partition numbers at most.

[0] 1
[1] 0, 1
[2] 0, 1, 2
[3] 0, 1, 2,  3
[4] 0, 1, 3,  4,  5
[5] 0, 1, 3,  5,  6,  7
[6] 0, 1, 4,  7,  9, 10, 11
[7] 0, 1, 4,  8, 11, 13, 14, 15
[8] 0, 1, 5, 10, 15, 18, 20, 21, 22
[9] 0, 1, 5, 12, 18, 23, 26, 28, 29, 30
"""


@cache
def partacc(n: int) -> list[int]:
    return list(accumulate(partition(n)))


PartAcc = Table(
    partacc, 
    "PartitionAcc", 
    ["A026820", "A058400"], 
    "",
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PartAcc)
