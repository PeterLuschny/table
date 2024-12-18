from functools import cache
from _tabltypes import Table

"""Lah numbers (unsigned).


[0]  1
[1]  0       1
[2]  0       2        1
[3]  0       6        6        1
[4]  0      24       36       12        1
[5]  0     120      240      120       20       1
[6]  0     720     1800     1200      300      30      1
[7]  0    5040    15120    12600     4200     630     42     1
[8]  0   40320   141120   141120    58800   11760   1176    56    1
[9]  0  362880  1451520  1693440   846720  211680  28224  2016   72   1
"""


@cache
def lah(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = lah(n - 1) + [1]
    row[0] = 0
    for k in range(n - 1, 0, -1):
        row[k] = row[k] * (n + k - 1) + row[k - 1]
    return row


Lah = Table(
    lah,
    "Lah",
    ["A271703", "A008297", "A066667", "A089231", "A105278", "A111596"],
    "A111596",
    r"\binom{n}{k} \text{FallingFactorial}(n-1, n-k)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Lah)
