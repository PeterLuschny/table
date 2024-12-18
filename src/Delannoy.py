from functools import cache
from _tabltypes import Table

"""Delannoy triangle.

[0] [1]
[1] [1,  1]
[2] [1,  3,   1]
[3] [1,  5,   5,   1]
[4] [1,  7,  13,   7,   1]
[5] [1,  9,  25,  25,   9,   1]
[6] [1, 11,  41,  63,  41,  11,   1]
[7] [1, 13,  61, 129, 129,  61,  13,   1]
[8] [1, 15,  85, 231, 321, 231,  85,  15,  1]
[9] [1, 17, 113, 377, 681, 681, 377, 113, 17, 1]
"""


@cache
def delannoy(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]

    rov = delannoy(n - 2)
    row = delannoy(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] += row[k - 1] + rov[k - 1]
    return row


Delannoy = Table(
    delannoy,
    "Delannoy",
    ["A008288"],
    "A132372",
    r"\text{Hyper}([-k, k - n], [1], 2)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Delannoy)
