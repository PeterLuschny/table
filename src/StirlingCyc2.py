from functools import cache
from _tabltypes import Table

"""Stirling cycle numbers of second order.

[0]  1
[1]  0,     0
[2]  0,     1,     0
[3]  0,     2,     0,     0
[4]  0,     6,     3,     0,    0
[5]  0,    24,    20,     0,    0, 0
[6]  0,   120,   130,    15,    0, 0, 0
[7]  0,   720,   924,   210,    0, 0, 0, 0
[8]  0,  5040,  7308,  2380,  105, 0, 0, 0, 0
[9]  0, 40320, 64224, 26432, 2520, 0, 0, 0, 0, 0
"""


@cache
def stirlingcycle2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 0]

    rov = stirlingcycle2(n - 2)
    row = stirlingcycle2(n - 1) + [0]
    for k in range(1, n // 2 + 1):
        row[k] = (n - 1) * (rov[k - 1] + row[k])
    return row


StirlingCycle2 = Table(
    stirlingcycle2,
    "StirlingCyc2",
    ["A358622", "A008306", "A106828"],
    "",
    r"n! [z^k][t^n] (\exp(t) (1 - t))^{-z}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingCycle2)
