from functools import cache
from _tabltypes import Table

"""Ordered cycle numbers.

[0] [1]
[1] [0,    1]
[2] [0,    1,     2]
[3] [0,    2,     6,     6]
[4] [0,    6,    22,    36,     24]
[5] [0,   24,   100,   210,    240,    120]
[6] [0,  120,   548,  1350,   2040,   1800,    720]
[7] [0,  720,  3528,  9744,  17640,  21000,  15120,   5040]
[8] [0, 5040, 26136, 78792, 162456, 235200, 231840, 141120, 40320]
"""


@cache
def orderedcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = orderedcycle(n - 1) + [0]
    row[n] = row[n] * n
    for k in range(n, 0, -1):
        row[k] = (n - 1) * row[k] + k * row[k - 1]
    return row


OrderedCycle = Table(
    orderedcycle,
    "OrderedCycle",
    ["A225479", "A048594", "A075181"],
    "",
    r"k! {n \brack k}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(OrderedCycle)
