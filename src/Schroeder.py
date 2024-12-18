from functools import cache
from _tabltypes import Table

"""Schroeder triangle.

[0] [1]
[1] [0,     1]
[2] [0,     2,     1]
[3] [0,     6,     4,     1]
[4] [0,    22,    16,     6,    1]
[5] [0,    90,    68,    30,    8,    1]
[6] [0,   394,   304,   146,   48,   10,   1]
[7] [0,  1806,  1412,   714,  264,   70,  12,   1]
[8] [0,  8558,  6752,  3534, 1408,  430,  96,  14,  1]
[9] [0, 41586, 33028, 17718, 7432, 2490, 652, 126, 16, 1]
"""


@cache
def schroeder(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = schroeder(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] += row[k - 1] + row[k + 1]

    return row


Schroeder = Table(
    schroeder,
    "Schroeder",
    ["A122538", "A033877", "A080245", "A080247", "A106579"],
    "A000000",
    r"is(k = 0)\ ? \ 0^{n} : T(n-1,k-1)+T(n-1,k)+T(n,k+1)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Schroeder)
