from functools import cache
from _tabltypes import Table

"""Stirling cycle numbers, unsigned Stirling numbers of the 1. kind.


[0]  1
[1]  0,     1
[2]  0,     1,      1
[3]  0,     2,      3,      1
[4]  0,     6,     11,      6,     1
[5]  0,    24,     50,     35,    10,     1
[6]  0,   120,    274,    225,    85,    15,    1
[7]  0,   720,   1764,   1624,   735,   175,   21,   1
[8]  0,  5040,  13068,  13132,  6769,  1960,  322,  28,  1
[9]  0, 40320, 109584, 118124, 67284, 22449, 4536, 546, 36, 1
"""


@cache
def stirlingcycle(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = [0] + stirlingcycle(n - 1)
    for k in range(1, n):
        row[k] = row[k] + (n - 1) * row[k + 1]

    return row


StirlingCycle = Table(
    stirlingcycle,
    "StirlingCycle",
    ["A132393", "A008275", "A008276", "A048994", "A054654", "A094638", "A130534"],
    "A000000",
    r"{n \brack k}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingCycle)
